from stedr.common import post, encode
from stedr import options

def set_watermark(stedr, f, pos, mode, opts: options.Options):
    data = {'image': encode(f), 'mode': mode, 'position': pos}
    post(f'stedr/{stedr}/watermark', None, data, opts)


def set_heartbeat(stdr, hours, type, id, opts: options.Options):
    post(f'stedr/{stdr}/heartbeat', {"hours": hours, "type": type, "id": id}, {}, opts)


def run_cronsource(stdr, count, backfill, opts: options.Options):
    post(f'cron/{stdr}/source/run', {"count": count, "backfill": backfill}, {}, opts)


def run_cronrules(stdr, opts: options.Options):
    post(f'cron/{stdr}/rules/run', {}, {}, opts)


def run_cronfull(stdr, opts: options.Options):
    params = {}
    if stdr is not None:
        params["stedr"] = stdr

    post(f'cron/run', params, {}, opts)


def add_integration(stdr, name, type, params, opts: options.Options):
    if params is None:
        params = []
    paramsdict = {params[i].split("=")[0]: params[i].split("=")[1] for i in range(0, len(params))}
    print(paramsdict)
    post(f'stedr/{stdr}/integration', {}, {"name": name, "type": type, "params": paramsdict}, opts)


def add_rule(stdr, opts: options.Options):
    post(f'stedr/{stdr}/rule', {}, {}, opts)
