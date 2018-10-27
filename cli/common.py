import json
import base64
import click
import requests
import options
from io import open


def get(restpath, params, opts: options.Options):
    url = f'http://{opts.endpoint}/api/{restpath}'
    headers = {'Authentication': f'key {opts.apikey}, uid {opts.uid}'}

    if opts.verbose > 1:
        click.echo(f'Url: {url}')
        click.echo(f'Header: {headers}')
        click.echo(f'Params: {params}')

    response = requests.get(url, headers=headers, params=params)

    if opts.verbose > 0:
        click.echo(response.headers)

    click.echo(response.content)


def getFile(restpath, params, save_file_path, opts: options.Options):
    url = f'http://{opts.endpoint}/api/{restpath}'
    headers = {'Authentication': f'key {opts.apikey}, uid {opts.uid}'}

    if opts.verbose > 1:
        click.echo(f'Url: {url}')
        click.echo(f'Header: {headers}')
        click.echo(f'Params: {params}')

    response = requests.get(url, headers=headers, params=params)

    with open(save_file_path, 'wb') as fd:
        fd.write(response.content)


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
