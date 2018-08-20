import configparser
from io import open
from pathlib import Path
import click
from os.path import isfile


CONFIGFILE = Path.home() / '.stedr'


class Options:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.init()

    # Non-sticky options
    verbose = 0
    dryrun = False

    # Sticky options - persisted in config file
    apikey = 'na'
    uid = 'na'
    endpoint = 'na'

    def init(self):
        if not isfile(CONFIGFILE):
            with open(CONFIGFILE, 'w+') as configfile:
                self.config.write(configfile)

        self.config.read(CONFIGFILE)
        self.apikey = self.config.get('DEFAULT', 'apikey', fallback='na')
        self.endpoint = self.config.get('DEFAULT', 'endpoint', fallback='na')
        self.uid = self.config.get('DEFAULT', 'uid', fallback='na')

    def get(self, name, default):
        return self.config.get('DEFAULT', name, fallback=default)

    def set(self, name, value):
        default_section = self.config['DEFAULT']
        default_section[name] = value
        with open(CONFIGFILE, 'w') as configfile:
            self.config.write(configfile)
        self.init()

    def to_string(self):
        click.echo('uid: %s' % self.config['DEFAULT']['uid'])
        click.echo('apikey: %s' % self.config['DEFAULT']['apikey'])
        click.echo('endpoint: %s' % self.config['DEFAULT']['endpoint'])
