import click
import options
from snap import image_upload
from stedr import set_watermark, run_cron
from timelapse import remakemonth, remakeyear, remakeimage
from common import post

# To enable -h abbrivation of help option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# Global attributes
opts = options.Options()


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
        opts.dryrun = dryrun
    if endpoint:
        click.echo('Overriding endpoint: %s' % endpoint)
        opts.endpoint = endpoint
    if apikey:
        click.echo('Overriding apikey: %s' % apikey)
        opts.apikey = apikey
    if uid:
        click.echo('Overriding uid: %s' % uid)
        opts.uid = uid


#
# Snap group (or to be at least)
#
@cli.group()
def snap():
    pass


@snap.command('upload')
@click.argument('path', type=click.Path(exists=True))
@click.option('--reprocess/--no-reprocess', default=False, help="Reprocess previous image was identical")
@click.option('--backfill/--no-backfill', default=False, help="Allow older images than already imported")
@click.option('--stedr', required=True, help="The id of the stedr")
@click.option('--date', required=False, default="exif", help="exif, now or explicit. Defaults to exif")
@click.option('--progress', type=click.Path(file_okay=True, dir_okay=False), help="Progress file to support graceful retries")
def snap_upload(path, stedr, reprocess, backfill, date, progress):
    image_upload(stedr, path, reprocess, backfill, opts, date, progress)


@snap.command('download')
def snap_download():
    click.echo('download')


#
# Config groups - set uid, key and endpoint for the cli
#
@cli.group()
def config():
    pass


@config.command('list')
def list_cmd():
    click.echo(opts.to_string())


@config.command('set')
@click.option('--uid', required=True, help="The user id - a long string of random characters")
@click.option('--apikey', required=True, help="The uuid you see under settings")
@click.option('--endpoint', default="playchat-e1a51.appspot.com", help="The hostname without https or path")
def set_cmd(uid, apikey, endpoint):
    opts.set('uid', uid)
    opts.set('apikey', apikey)
    opts.set('endpoint', endpoint)
    click.echo('Settings are now: %s' % opts.to_string())


#
# Stedr group - List info or upload watermark
#
@cli.group('stedr')
def stedrgroup():
    pass


@stedrgroup.command('set-watermark')
@click.argument('file', type=click.Path(exists=True, dir_okay=False))
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--pos', required=True, nargs=2, type=float, help="E.g. 0,0.5")
@click.option('--mode', required=True,  type=click.Choice(['none', 'normal', 'exclusive']), help="The id of stedr")
def stedr_set_watermark(stedr, file, pos, mode):
    set_watermark(stedr, file, pos, mode, opts)


@stedrgroup.command('list')
def stedr_list():
    click.echo('list')


@cli.group('timelapse')
def timelapse():
    pass


@timelapse.command('remake-month')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--year', required=True, help="E.g. 2018")
@click.option('--month', required=False, default=0, help="E.g 9 for September (default is 0 == all months")
def remake_month(stedr, year, month):
    remakemonth(stedr, year, month, opts)


@timelapse.command('remake-year')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--year', required=True, help="E.g. 2018")
def remake_year(stedr, year):
    remakeyear(stedr, year, opts)


@timelapse.command('remake-image')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--year', required=True, help="E.g. 2018")
def remake_image(stedr, year):
    remakeimage(stedr, year, opts)


@cli.group('dataflow')
def dataflow():
    pass


@dataflow.command('wordcount')
def wordcount():
    post('dataflow/wordcount', {}, opts)


@cli.group('cron')
def cron():
    pass


@cron.command('source')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--count', required=False, default=1, help="Number of files to import from url")
def cron_source(stedr, count):
    run_cron(stedr, count, opts)
