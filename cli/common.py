import json
import base64
import click
import requests
import options
from io import open
import os


def get(restpath, target_file, params, opts: options.Options):
    url = f'http://{opts.endpoint}/api/{restpath}'
    headers = {'Authentication': f'key {opts.apikey}, uid {opts.uid}'}

    if opts.verbose > 1:
        click.echo(f'Url: {url}')
        click.echo(f'Header: {headers}')
        click.echo(f'Params: {params}')

    response = requests.get(url, headers=headers, params=params)

    if opts.verbose > 0:
        click.echo(response.headers)

    if target_file:
        with open(target_file, 'wb') as fd:
            fd.write(response.content)

    click.echo(response.content)


def get_file(restpath, params, save_file_path, opts: options.Options):
    url = f'http://{opts.endpoint}/api/{restpath}'
    headers = {'Authentication': f'key {opts.apikey}, uid {opts.uid}'}

    if opts.verbose > 1:
        click.echo(f'Url: {url}')
        click.echo(f'Header: {headers}')
        click.echo(f'Params: {params}')

    response = requests.get(url, headers=headers, params=params)
    payload = response.json()

    filename = payload['filename']
    if not filename:
        click.echo("Did not get filename from Stedr - unable to download")
        return

    if opts.verbose > 0:
        click.echo(f'Saving {filename}')

    full_path = os.path.join(save_file_path, filename)
    directory = os.path.dirname(full_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(full_path, 'wb') as fd:
        fd.write(base64.b64decode(payload['image']))


def post(restpath, params, data, opts: options.Options):

    payload = json.dumps(data)
    url = f'http://{opts.endpoint}/api/{restpath}'
    headers = {'Authentication': f'key {opts.apikey}, uid {opts.uid}'}

    if opts.verbose > 1:
        click.echo(f'Url: {url}')
        click.echo(f'Header: {headers}')
        click.echo(f'Params: {params}')
        data_copy = data.copy()
        if 'image' in data_copy:
            data_copy['image'] = 'removed'
        payload_copy = json.dumps(data_copy)
        click.echo(f'Payload {payload_copy}')

    if opts.dryrun:
        return

    response = requests.post(
        url,
        params=params,
        headers=headers,
        data=payload)

    if opts.verbose > 0:
        click.echo(response.headers)
        click.echo(response.content)


def encode(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode('ascii')
