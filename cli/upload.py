import base64
import subprocess
import re
import json
from io import open
from pathlib import Path

import requests
import click
import options
from datetime import datetime
from os import listdir
from os.path import isfile, isdir, join


def image_upload(stedr, path, replace, dedup, opts: options.Options, progress):
    # Start populating request data
    data = {'replace': replace}

    # Get all files to upload
    if isdir(path):
        if opts.verbose > 1:
            click.echo('Uploading images from %s' % path)
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        with click.progressbar(onlyfiles, label='Uploading images') as allfiles:
            for f in allfiles:
                if not progress_already_contains_file(progress, f):
                    fullfile = join(path, f)
                    populate_from_exif(fullfile, data)
                    populate_64base(fullfile, data)
                    post_request(stedr, data, opts)
                    update_progress_file(progress, f)
    else:
        if opts.verbose > 1:
            click.echo('Uploading image %s' % path)
        if not progress_already_contains_file(progress, path):
            populate_from_exif(path, data)
            populate_64base(path, data)
            post_request(stedr, data, opts)
            update_progress_file(progress, path)


def progress_already_contains_file(progress_file, file):
    if progress_file is None:
        return False

    if not isfile(progress_file):
        Path(progress_file).touch()

    file_content = open(progress_file, 'r+').read()
    if file in file_content:
        return True

    return False

def update_progress_file(progress_file, file):
    if progress_file is None:
        return False

    with open(progress_file, 'a+') as out:
        out.write(file + '\n', )

def post_request(stedr, data, opts: options.Options):
    # Construct URL
    payload = json.dumps(data)
    url = f'http://{opts.endpoint}/api/snap/{stedr}'
    headers = {'Authentication': f'key {opts.apikey}, uid {opts.uid}'}

    if opts.verbose > 1:
        click.echo(f'Url: {url}')
        click.echo(f'Header: {headers}')
        data_copy = data.copy()
        data_copy['image'] = 'removed'
        payload_copy = json.dumps(data_copy)
        click.echo(f'Payload {payload_copy}')

    if opts.dryrun:
        return

    response = requests.post(
        url,
        headers=headers,
        data=payload)

    if opts.verbose > 0:
        click.echo(response.headers)
        click.echo(response.content)

def populate_64base(fullfile, data):
    with open(fullfile, "rb") as f:
        data['image'] = base64.b64encode(f.read()).decode('ascii')


def populate_from_exif(fullfile, data):
    metadata = subprocess.check_output(['identify', '-verbose', fullfile])
    for line in metadata.decode("utf-8").splitlines():
        # Extract time
        datematch = re.search('.*exif:DateTime: (.*)', line)
        if datematch:
            data['date'] = int(datetime.strptime(datematch.group(1), "%Y:%m:%d %H:%M:%S").strftime('%s'))

        # Extract format
        mimematch = re.search('Mime type: image/(.*)', line)
        if (mimematch):
            data['format'] = mimematch.group(1)

    return data