import subprocess
import re
from common import post, encode, get_file, get
from io import open
from pathlib import Path
import click
import options
from datetime import datetime
from os import listdir
from os.path import isfile, isdir, join


def image_list(stedr, imagelist, opts):
    get(f'snap/{stedr}/list', imagelist, None, opts)


def image_predict(stedr, snap, opts):
    post(f'snap/{stedr}/{snap}/ml', None, None, opts);


def image_upload_from_source(stedr, backfill, count, opts):
    params = {"count": count}
    if backfill:
        params["backfill"] = ''
    post(f'cron/{stedr}/source', params, {}, opts)


def image_download(stedr, imageid, progress, imagelist, savedir, opts: options.Options):
    success = 0
    failures = 0

    if imageid is not None:
        try:
            get_file(f'snap/{stedr}/{imageid}/image', None, savedir, opts)
        except:
            click.echo("Unable to download file")

    else:
        if imagelist is None:
            click.echo("You must specify either imageid or imagelist")
            return False
        if not isfile(imagelist):
            click.echo("imagelist must be a regular file with ids separated by newline")
        if not progress:
            progress = imagelist + ".progress"
        with open(imagelist) as f:
            all_lines = f.readlines();
            with click.progressbar(all_lines, label='Downloading images') as allIds:
                for imgid in allIds:
                    if not progress_already_contains_item(progress, imgid):
                        try:
                            get_file(f'snap/{stedr}/{imgid.rstrip()}/image', None, savedir, opts)
                            update_progress_file(progress, imgid, True)
                            success += 1
                        except:
                            update_progress_file(progress, imgid, False)
                            failures += 1

    click.echo(f'Successfully downloaded all {success} images')
    if failures > 0:
        click.echo(f'Failed downloaded {failures} images - see {progress} for details')


def image_upload(stedr, path, reprocess, backfill, date, progress, opts: options.Options):
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
                if not progress_already_contains_item(progress, f):
                    fullfile = join(path, f)
                    populate_from_exif(fullfile, data)
                    adjustdate(data, date)
                    data['image'] = encode(fullfile)
                    post(f'snap/{stedr}', None, data, opts)
                    update_progress_file(progress, f)
    else:
        if opts.verbose > 1:
            click.echo('Uploading image %s' % path)
        if not progress_already_contains_item(progress, path):
            populate_from_exif(path, data)
            adjustdate(data, date)
            data['image'] = encode(path)
            post(f'snap/{stedr}', None, data, opts)
            update_progress_file(progress, path)


def progress_already_contains_item(progress_file, file):
    if progress_file is None:
        return False

    if not isfile(progress_file):
        Path(progress_file).touch()

    file_content = open(progress_file, 'r+').read()
    if file in file_content:
        return True

    return False


def update_progress_file(progress_file, file, success):
    if progress_file is None:
        return False

    with open(progress_file, 'a+') as out:
        out.write(str.strip(file) + '\t' + str(success) + '\n', )


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