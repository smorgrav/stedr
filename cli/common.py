import json
import base64
import click
import requests
import options
from io import open

def post(restpath, data, opts: options.Options):

    payload = json.dumps(data)
    url = f'http://{opts.endpoint}/api/{restpath}'
    headers = {'Authentication': f'key {opts.apikey}, uid {opts.uid}'}

    if opts.verbose > 1:
        click.echo(f'Url: {url}')
        click.echo(f'Header: {headers}')
        data_copy = data.copy()
        if 'image' in data_copy:
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

def encode(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode('ascii')