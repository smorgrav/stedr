from common import post
import options

def remakemonth(stedr, year, month, opts: options.Options):
    if month == 0:
        for m in range(1,13):
            post(f'timelapse/{stedr}/remakemonth/{year}/{m}', {}, opts)
    else:
        post(f'timelapse/{stedr}/remakemonth/{year}/{month}', {}, opts)


def remakeyear(stedr, year, opts: options.Options):
    post(f'timelapse/{stedr}/remakeyear/{year}', {}, opts)


def remakeimage(stedr, year, opts: options.Options):
    post(f'timelapse/{stedr}/remakeimage/{year}', {}, opts)
