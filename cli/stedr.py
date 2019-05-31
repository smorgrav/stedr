from common import post, encode
import options


def set_watermark(stedr, f, pos, mode, opts: options.Options):
    data = {'image': encode(f), 'mode': mode, 'position': pos}
    post(f'stedr/{stedr}/watermark', None, data, opts)


def set_heartbeat(stedr, hours, type, id, opts: options.Options):
    post(f'stedr/{stedr}/heartbeat', {"hours": hours, "type": type, "id": id}, {}, opts)


def run_cronsource(stedr, count, backfill, opts: options.Options):
    post(f'cron/{stedr}/source/run', {"count": count, "backfill": backfill}, {}, opts)


def run_cronrules(stedr, opts: options.Options):
    post(f'cron/{stedr}/rules/run', {}, {}, opts)


def run_cronfull(stedr, opts: options.Options):
    params = {}
    if stedr is not None:
        params["stedr"] = stedr

    post(f'cron/run', params, {}, opts)


def add_integration(stedr, name, type, params, opts: options.Options):
    if params is None:
        params = []
    paramsdict = {params[i].split("=")[0]: params[i].split("=")[1] for i in range(0, len(params))}
    print(paramsdict)
    post(f'stedr/{stedr}/integration', {}, {"name": name, "type": type, "params": paramsdict}, opts)


def add_rule(stedr, opts: options.Options):
    post(f'stedr/{stedr}/rule', {}, {}, opts)
