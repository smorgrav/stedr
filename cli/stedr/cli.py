import click
import datetime
from stedr.snap import image_upload, image_download, image_list, image_upload_from_source, image_predict, \
    image_reprocess
from stedr.stedr import set_watermark, run_cronfull, run_cronrules, run_cronsource, add_integration, set_heartbeat, \
    add_rule
from stedr.timelapse import remakemonth, remakeyear, remakeimage
from stedr.common import post, get
from stedr import options

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
@click.option('--progress', type=click.Path(file_okay=True, dir_okay=False),
              help="Progress file to support graceful retries")
def snap_upload(path, stedr, reprocess, backfill, date, progress):
    """Upload snaps from your machine

       This is an alternative way to bootstrap or enrich the set of snaps.
    """
    image_upload(stedr, path, reprocess, backfill, date, progress, opts)


@snap.command('download')
@click.argument('savedir', type=click.Path(file_okay=False))
@click.option('--stedr', required=True, help='The id of the stedr')
@click.option('--imageid', required=False, help='The id of the image')
@click.option('--imagelist', type=click.Path(file_okay=True, dir_okay=False), required=False)
@click.option('--progress', type=click.Path(file_okay=True, dir_okay=False))
def snap_download(stedr, imageid, progress, imagelist, savedir):
    image_download(stedr, imageid, progress, imagelist, savedir, opts)


@snap.command('list')
@click.option('--stedr', required=True, help="The id of the stedr")
@click.option('--file', type=click.Path(file_okay=True, dir_okay=False), required=False,
              help="Save the list to this file")
@click.option('--verbose/--no-verbose', required=False, help="More columns in output (if not json)")
@click.option('--json/--no-json', required=False, help="List raw json data")
@click.option('--from', 'fromdate', required=False, type=click.DateTime(),
              default=datetime.date(2016, 1, 1).strftime("%Y-%m-%d %H:%M:%S"),
              help="List snaps not older than this (defaults to 2016)")
@click.option('--to', 'todate', required=False, type=click.DateTime(),
              default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              help="List snaps not newer than this (defaults to now)")
def snap_list(stedr, file, verbose, json, fromdate, todate):
    """List all snaps available for a given Stedr.

       Often used to create a filelist for other commands (like download)
    """

    fromunix = int(fromdate.timestamp())
    tounix = int(todate.timestamp())

    image_list(stedr, file, fromunix, tounix, verbose, json, opts)


@snap.command('predict')
@click.option('--stedr', required=True, help="The id of the stedr")
@click.option('--snap', required=True, help="The id of the snap/image - typically a uuid")
def snap_predict(stedr, snap):
    """Get predictions from machine learning on this snap"""
    image_predict(stedr, snap, opts)


@snap.command('reprocess')
@click.option('--stedr', required=True, help='The id of the stedr')
@click.option('--snap', required=False, help='The id of the image')
@click.option('--snaps', type=click.Path(file_okay=True, dir_okay=False), required=False,
              help='File with list of ids, line separated')
@click.option('--progress', type=click.Path(file_okay=True, dir_okay=False), help="Enable gracefull retries")
def snap_reprocess(stedr, snap, file, progress):
    """Take snapid through the initial import pipeline again"""
    image_reprocess(stedr, snap, file, progress, opts)


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
@click.option('--name', required=False, help='The set if you want to set config for an alternative configuration set',
              default=opts.get_current_section())
@click.option('--uid', required=True, help="The user id - a long string of random characters")
@click.option('--apikey', required=True, help="The uuid you see under settings")
@click.option('--endpoint', default="playchat-e1a51.appspot.com", help='The hostname without https or path')
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
@click.option('--mode', required=True, type=click.Choice(['none', 'normal', 'exclusive']), help="The id of stedr")
def stedr_set_watermark(stedr, file, pos, mode):
    set_watermark(stedr, file, pos, mode, opts)


@stedrgroup.command('set-heartbeat')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--id', required=True, help="The id for the integration (ie the integration config")
@click.option('--type', required=True, type=click.Choice(['regobs', 'email', 'logger', 'opsgenie']),
              help="One of the supported integrations")
@click.option('--hour', default=36, type=click.IntRange(1, 720),
              help="How long between two snaps before we trigger an action in hours (defaults to 36)")
def stedr_set_heartbeat(stedr, id, type, hour):
    set_heartbeat(stedr, hour, type, id, opts)


@stedrgroup.command('add-integration')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--name', required=True, help="Your name for the integration")
@click.option('--type', required=True, type=click.Choice(['regobs', 'email', 'opsgenie']),
              help="One of the supported integrations")
@click.option('--params', '-p', multiple=True, required=False,
              help="mulitple pairs of key=value. eg. -p apikey=dsds -p message={STEDR_ID}")
def stedr_add_integration(stedr, name, type, params):
    add_integration(stedr, name, type, params, opts)


@stedrgroup.command('add-rule')
@click.option('--stedr', required=True, help="The id of stedr")
def stedr_add_rule(stedr):
    add_rule(stedr, opts)


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


@cron.command('full')
@click.option('--stedr', required=False, help="The id of stedr")
def cron_full(stedr):
    run_cronfull(stedr, opts)


@cron.command('rules')
@click.option('--stedr', required=False, help="The id of stedr")
def cron_rules(stedr):
    run_cronrules(stedr, opts)


@cron.command('source')
@click.option('--stedr', required=True, help="The id of stedr")
@click.option('--count', required=False, default=1, help="Number of files to import from url")
@click.option('--backfill/--no-backfill', required=False, default=False, help="Allow import of older images")
def cron_source(stedr, count, backfill):
    run_cronsource(stedr, count, backfill, opts)


@cli.command('teapot', help="Check that we can communicate with the kettle")
def teapot():
    """A test command  - to verify communication with the kettle"""
    get('teapot', None, None, opts)


@cli.group('ml')
def ml():
    pass


@ml.command('new', help="Create a new model ")
@click.option('--name', required=True, help="The name of the new model")
@click.option('--width', required=False, default=224, help="224 for vvg, resnet and more, 299 for inception")
@click.option('--height', required=False, default=224, help="224 for vvg, resnet and more, 299 for inception")
@click.option('--type', required=False, default=0, help="TODO really - the idea is to enumerate channel configuration")
def new_model(name, width, height, type):
    post('ml/model', None, {
        'name': name,
        'width': width,
        'height': height,
        'type': type
    }, opts)


@ml.command('train', help="Train the model (again)")
@click.option('--modelid', required=True, help="The model id")
def train_model(modelid):
    post(f'ml/model/{modelid}/train', None, None, opts)


@ml.command('deploy', help="Deploy a trained session - optionally a manually deployed session")
@click.option('--modelid', required=True, help="The model id")
def deploy_model(modelid):
    post(f'ml/model/{modelid}/deploy', None, None, opts)


@ml.command('manual', help="Deploy a trained session - optionally a manually deployed session")
@click.option('--modelid', required=True, help="The model id")
@click.option('--mlproject', required=False, help="mlengine project id for the manually deployed session")
@click.option('--mlmodel', required=False, help="only nessesary if different from modelid")
@click.option('--mlversion', required=False, help="mlengine version for the manually deplyed session")
def manual_model(modelid, projectid, model, version):
    post(f'ml/model/{modelid}/manual', {'projectid': projectid, 'model': model, 'version': version}, None, opts)


@ml.command('export', help="Export supervised values with the serving url. Pandas csv format")
@click.option('--file', required=False, type=click.Path(file_okay=False), help="File to save csv formatted output")
@click.option('--modelid', required=True, help="The model id")
def export_supervised(modelid, file):
    get(f'ml/model/{modelid}/csv2', file, None, opts)


if __name__ == '__main__':
    cli()
