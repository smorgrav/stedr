import subprocess
import re
from common import post, encode
from io import open
from pathlib import Path
import click
import options
from datetime import datetime
from os import listdir
from os.path import isfile, isdir, join


def image_download(stedr, id, targetPath, opts):


def image_upload(stedr, path, reprocess, backfill, opts: options.Options, date, progress):
    # Start populating request data
    # TODO proper options for backfill and reprocess
    data = {'reprocess': reprocess}

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
                    adjustdate(data, date)
                    data['image'] = encode(fullfile)
                    post(f'snap/{stedr}', None, data, opts)
                    update_progress_file(progress, f)
    else:
        if opts.verbose > 1:
            click.echo('Uploading image %s' % path)
        if not progress_already_contains_file(progress, path):
            populate_from_exif(path, data)
            adjustdate(data, date)
            data['image'] = encode(path)
            post(f'snap/{stedr}', None, data, opts)
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


def adjustdate(data, dateoption):
    if dateoption == 'now':
        data['date'] = int(datetime.now().strftime('%s'))
    elif dateoption != 'exif':
        data['date'] = int(datetime.strptime(dateoption).strftime('%s'))


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