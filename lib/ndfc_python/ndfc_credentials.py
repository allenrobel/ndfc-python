#!/usr/bin/env python
'''
Description:

Read the caller's Ansible vault and expose the following keys via properties:

ansible_user - via property username
ansible_password - via property password
ndfc_ip - via property ndfc_ip

Dependencies:

1. Ansible libraries

Install with:

pip install ansible

2. NdfcLoadConfig()

In this repo at lib/ndfc_python/ndfc_config.py

NdfcLoadConfig() loads ndfc_python's settings, which includes the path to your
ansible vault.  To configure this path, edit ndfc-python/lib/ndfc_python/ndfc_config.py
and modify the config_file variable at the top of the file.
'''
from ansible import constants as C
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader

from ndfc_python.ndfc_config import NdfcLoadConfig 

class NdfcCredentials(object):
    def __init__(self):
        self.mandatory_keys = set()
        self.mandatory_keys.add('ansible_user')
        self.mandatory_keys.add('ansible_password')
        self.mandatory_keys.add('ndfc_ip')
        self.mandatory_keys.add('discover_username')
        self.mandatory_keys.add('discover_password')


        self.c = NdfcLoadConfig()

        self.load_credentials()

    def load_credentials(self):
        try:
            loader = DataLoader()
            vault_secrets = CLI.setup_vault_secrets(loader=loader,
                        vault_ids=C.DEFAULT_VAULT_IDENTITY_LIST)
            loader.set_vault_secrets(vault_secrets)
            data = loader.load_from_file(self.c.config['ansible_vault'])
        except e as Exception:
            print('unable to load credentials in {}.'.format(self.c.config['ansible_vault']))
            print('Exception was: {}'.format(e))
            exit(1)

        for k in self.mandatory_keys:
            if k not in data:
                print('Exiting. ansible_vault is missing key {}'.format(k))
                exit(1)
        self.credentials = dict()
        self.credentials['username'] = str(data['ansible_user'])
        self.credentials['password'] = str(data['ansible_password'])
        self.credentials['ndfc_ip'] = str(data['ndfc_ip'])
        self.credentials['discover_username'] = str(data['discover_username'])
        self.credentials['discover_password'] = str(data['discover_password'])
    @property
    def discover_username(self):
        return self.credentials['discover_username']
    @property
    def discover_password(self):
        return self.credentials['discover_password']
    @property
    def username(self):
        return self.credentials['username']
    @property
    def password(self):
        return self.credentials['password']
    @property
    def ndfc_ip(self):
        return self.credentials['ndfc_ip']
