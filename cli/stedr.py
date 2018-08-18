import click
import options
from upload import image_upload

# To enable -h abbrivation of help option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# Global attributes
opts = options.Options


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True, help='Print out more for each command')
@click.option('-n', '--dryrun', is_flag=True, help='Do as much as possible without changing anything')
@click.option('-e', '--endpoint', help='Override configured endpoint')
@click.option('-k', '--apikey', help='Override configured apikey')
@click.option('-u', '--uid', help='Override configured uid')
def cli(verbose, dryrun, endpoint, apikey, uid):
    """
    The command line for Stedr - know your place!
    """
    if verbose > 0:
        click.echo('Verbose mode is %s' % verbose)
        opts.verbose = verbose
    if dryrun:
        click.echo('Dryrun mode!')
        opts.verbose = dryrun
    if endpoint:
        click.echo('Overriding endpoint: %s' % endpoint)
        opts.endpoint = endpoint
    if apikey:
        click.echo('Overriding apikey: %s' % apikey)
        opts.apikey = apikey
    if uid:
        click.echo('Overriding uid: %s' % uid)
        opts.uid = uid


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--dedup/--no-dedup', default=True, help="Ignore upload if previous image was identical")
@click.option('--replace/--no-replace', default=False, help="Replace existing image if same timestamp")
def upload(path, dedup, replace):
    click.echo('Uploading %s' % path)
    image_upload('mycamera', path, replace, dedup, opts)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def test(path):
    click.echo('Verbose mode is %s' % opts.verbose)
    click.echo('test %s' % opts.dryrun)
    click.echo('Path: %s' % path)


@cli.group()
def config():
    pass


@config.command('list')
def list_cmd():
    click.echo('Current config:')
    click.echo('Verbose mode is %s' % opts.verbose)
    click.echo('Endpoint %s' % opts.endpoint)
    click.echo('Uid %s' % opts.uid)
    click.echo('Apikey %s' % opts.apikey)


@config.command('set')
@click.option('--uid', required=True, help="The user id - a long string of random characters")
@click.option('--apikey', required=True, help="The uuid you see under settings")
@click.option('--endpoint', default="playchat-e1a51.appspot.com", help="The hostname without https or path")
def set_cmd(uid, apikey, endpoint):
    click.echo('hei %s' % uid)
    click.echo('hei %s' % apikey)
    click.echo('hei %s' % endpoint)

