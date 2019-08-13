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
    section = 'na'
    apikey = 'na'
    uid = 'na'
    endpoint = 'na'

    def init(self):
        if not isfile(CONFIGFILE):
            with open(CONFIGFILE, 'w+') as configfile:
                self.config.write(configfile)

        self.config.read(CONFIGFILE)
        self.section = self.config.get('DEFAULT', 'section', fallback='DEFAULT')
        self.apikey = self.get('apikey', 'na')
        self.endpoint = self.get('endpoint', 'na')
        self.uid = self.get('uid', 'na')

    def use(self, section):
        if self.config[section] is not None:
            self.set_inner('section', section, 'DEFAULT')
            self.init()
        else:
            click.echo('Config not defined - use "set" first')

    def get(self, name, default):
        return self.config.get(self.section, name, fallback=default)

    def get_current_section(self):
        return self.section

    def set(self, name, value):
        self.set_inner(name, value, self.section)

    def set_inner(self, name, value, section_name):
        if not section_name == 'DEFAULT' and not self.config.has_section(section_name):
            self.config.add_section(section_name)

        section = self.config[section_name]
        section[name] = value
        with open(CONFIGFILE, 'w') as configfile:
            self.config.write(configfile)

    def print_config(self, name=None):
        if name is not None:
            click.echo('Config: %s' % name)
            click.echo('uid: %s' % self.config[name]['uid'])
            click.echo('apikey: %s' % self.config[name]['apikey'])
            click.echo('endpoint: %s' % self.config[name]['endpoint'])
        else:
            click.echo('Current config: %s' % self.section)
            click.echo('uid: %s' % self.config[self.section]['uid'])
            click.echo('apikey: %s' % self.config[self.section]['apikey'])
            click.echo('endpoint: %s' % self.config[self.section]['endpoint'])

            if len(self.config.keys()) > 1:
                click.echo('')
                click.echo('Available sections:')
                for section in self.config:
                    click.echo('\t%s' % section)
