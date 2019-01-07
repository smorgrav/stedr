from common import post, encode
import options


def set_watermark(stedr, f, pos, mode, opts: options.Options):
    data = {'image': encode(f), 'mode': mode, 'position': pos}
    post(f'stedr/{stedr}/watermark', None, data, opts)


def run_cron(stedr, count, opts: options.Options):
    post(f'cron/{stedr}/source', {"count": count}, {}, opts)


def add_integration(stedr, name, type, opts: options.Options):
    post(f'stedr/{stedr}/integration', {}, {"name": name, "type": type}, opts)
