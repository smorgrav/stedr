from stedr.common import post
from stedr import options


def remakemonth(stedr, year, month, opts: options.Options):
    if month == 0:
        for m in range(1,13):
            post(f'timelapse/{stedr}/remakemonth/{year}/{m}', None, {}, opts)
    else:
        post(f'timelapse/{stedr}/remakemonth/{year}/{month}', None, {}, opts)


def remakeyear(stedr, year, opts: options.Options):
    post(f'timelapse/{stedr}/remakeyear/{year}', None, {}, opts)


def remakeimage(stedr, year, opts: options.Options):
    post(f'timelapse/{stedr}/remakeimage/{year}', None, {}, opts)
