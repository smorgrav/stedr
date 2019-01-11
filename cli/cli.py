import click
import options
from snap import image_upload, image_download, image_list, image_upload_from_source
from stedr import set_watermark, run_cron, add_integration
from timelapse import remakemonth, remakeyear, remakeimage
from common import post, get

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


@snap.command('import')
@click.option('--stedr', required=True, help="The id of the stedr")
@click.option('--backfill/--no-backfill', default=False, help="Allow older images than already imported")
@click.option('--count', required=False, default=1, help="Number of snaps to import")
def snap_from_source(stedr, backfill, count):
    """Import snaps from the source assosiated with the stedr.

       This is an alternative to wait for the automatic import job or a way to
       bulk import snaps when creating a new stedr.
    """
    image_upload_from_source(stedr, backfill, count, opts)


@snap.command('upload')
@click.argument('path', type=click.Path(exists=True))
@click.option('--reprocess/--no-reprocess', default=False, help="Reprocess previous image was identical")
@click.option('--backfill/--no-backfill', default=False, help="Allow older images than already imported")
@click.option('--stedr', required=True, help="The id of the stedr")
@click.option('--date', required=False, default="exif", help="exif, now or explicit. Defaults to exif")
@click.option('--progress', type=click.Path(file_okay=True, dir_okay=False), help="Progress file to support graceful retries")
def snap_upload(path, stedr, reprocess, backfill, date, progress):
    image_upload(stedr, path, reprocess, backfill, date, progress, opts)


@snap.command('download')
@click.argument('savedir', type=click.Path(file_okay=False))
@click.option('--stedr', required=True, help="The id of the stedr")
@click.option('--imageid', required=False, help="The id of the image")
@click.option('--imagelist', type=click.Path(file_okay=True, dir_okay=False), required=False, help="A list of image ids")
@click.option('--progress', type=click.Path(file_okay=True, dir_okay=False), help="Progress file to support graceful retries for the list")
def snap_download(stedr, imageid, progress, imagelist, savedir):
    image_download(stedr, imageid, progress, imagelist, savedir, opts)


@snap.command('list')
@click.option('--stedr', required=True, help="The id of the stedr")
@click.option('--imagelist', type=click.Path(file_okay=True, dir_okay=False), required=False, help="Save the list to this file")
def snap_list(stedr, imagelist):
    image_list(stedr, imagelist, opts)


#
# Config groups - set uid, key and endpoint for the cli
#
@cli.group()
def config():
    pass


@config.command('show')
@click.option('--name', required=False, help="Show config and list available config sets")
def list_cmd(name):
    click.echo(opts.print_config(name=name))


@config.command('use')
@click.option('--name', required=True, help="The config set to use")
def use_cmd(name):
    opts.use(name)
    opts.print_config()


@config.command('set')
@click.option('--name', required=False, help="The set if you want to set config for an alternative configuration set",
              default=opts.get_current_section())
@click.option('--uid', required=True, help="The user id - a long string of random characters")
@click.option('--apikey', required=True, help="The uuid you see under settings")
@click.option('--endpoint', default="playchat-e1a51.appspot.com", help="The hostname without https or path")
def set_cmd(name, uid, apikey, endpoint):
    opts.set_inner('uid', uid, name)
    opts.set_inner('apikey', apikey, name)
    opts.set_inner('endpoint', endpoint, name)
    opts.print_config()


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


@stedrgroup.command('add-integration')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--name', required=True, help="Your name for the integration")
@click.option('--type', required=True, type=click.Choice(['regops', 'email']), help="One of the supported integrations")
def stedr_add_integration(stedr, name, type):
    add_integration(stedr, name, type, opts)


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
@click.option('--stedr', required=True, help="The id of stimageedr")
@click.option('--year', required=True, help="E.g. 2018")
def remake_image(stedr, year):
    remakeimage(stedr, year, opts)


@cli.group('dataflow')
def dataflow():
    pass


@dataflow.command('wordcount', help="Test function for dataflow")
def wordcount():
    post('dataflow/wordcount', None, {}, opts)


@cli.group('cron')
def cron():
    pass


@cron.command('source')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--count', required=False, default=1, help="Number of files to import from url")
def cron_source(stedr, count):
    run_cron(stedr, count, opts)


@cron.command('teapot', help="The http variant of hello world - basically to check that the service is up")
def teapot():
    get('teapot', None, None, opts)


@cli.group('ml')
def ml():
    pass


@ml.command('new', help="Create a new model")
@click.option('--name', required=True, help="The name of the new model")
@click.option('--projectid', required=True, help="google cloud projectid where the model lives")
@click.option('--model', required=True, help="mlengine model name")
@click.option('--version', required=True, help="mlengine version")
@click.option('--width', required=False, default=224, help="224 for vvg, resnet and more, 299 for inception")
@click.option('--height', required=False, default=224, help="224 for vvg, resnet and more, 299 for inception")
@click.option('--type', required=False, default=0, help="TODO really - the idea is to enumerate channel configuration")
def new_model(name, projectid, model, version, width, height, type):
    post('ml', None, {
        'name': name,
        'projectid': projectid,
        'model': model,
        'existingmodel': True,
        'version': version,
        'width': width,
        'height': height,
        'type': type
    }, opts)
