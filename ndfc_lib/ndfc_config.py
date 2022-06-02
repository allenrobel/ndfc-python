'''
ndfc_config.py

Description:

Load YAML file pointed to by the config_file variable, and return the contents as a python dict()

Usage:

from ndfc_lib.ndfc_config import NdfcLoadConfig

c = NdfcLoadConfig()
print('c.ansible_vault {}'.format(c.config['ansible_vault']))

Author:

Allen Robel (arobel@cisco.com)
'''
import yaml

config_file = '/Users/arobel/repos/ndfc-python/ndfc_lib/config.yml'
class NdfcLoadConfig(object):
    def __init__(self):
        self.properties = dict()
        self.load_config()

    def load_config(self):
        with open(config_file, 'r') as fp:
            self.properties['config'] = yaml.safe_load(fp)

    @property
    def config(self):
        return self.properties['config']