#!/usr/bin/env python
"""
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
"""
import sys
from inspect import stack

from ansible.cli import CLI
from ansible.errors import AnsibleFileNotFound, AnsibleParserError
from ansible.parsing.dataloader import DataLoader
from ndfc_python.ndfc_config import NdfcLoadConfig

OUR_VERSION = 103


class NdfcCredentials:
    """
    Unencrypt NDFC and other credentials and provide to the user via properties
    after asking for the ansible vault password.
    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self._init_mandatory_keys()
        self.cred_obj = NdfcLoadConfig()
        self.load_credentials()

    def log(self, *args):
        """
        simple logger
        """
        print(f"{stack()[1].function}(v{self.lib_version}): {' '.join(args)}")

    def _init_mandatory_keys(self):
        """
        Initialize a set containing all mandatory keys
        """
        self.mandatory_keys = set()
        self.mandatory_keys.add("ansible_user")
        self.mandatory_keys.add("ansible_password")
        self.mandatory_keys.add("ndfc_ip")
        self.mandatory_keys.add("discover_username")
        self.mandatory_keys.add("discover_password")

    def load_credentials(self):
        """
        Load user credentials from ansible vault.  This asked for the ansible
        vault password.
        """
        try:
            loader = DataLoader()
            vault_secrets = CLI.setup_vault_secrets(loader=loader, vault_ids=None)
            loader.set_vault_secrets(vault_secrets)
            data = loader.load_from_file(self.cred_obj.config["ansible_vault"])
        except AnsibleFileNotFound as exception:
            self.log(
                "Exiting. Unable to load credentials in "
                f" {self.cred_obj.config['ansible_vault']}.",
                f" Exception detail: {exception}",
            )
            sys.exit(1)
        except AnsibleParserError as exception:
            self.log(
                "Exiting. Unable to load credentials in "
                f" {self.cred_obj.config['ansible_vault']}.",
                f" Exception detail: {exception}",
            )
            sys.exit(1)

        for key in self.mandatory_keys:
            if key not in data:
                self.log("Exiting. ansible_vault is missing key {key}")
                sys.exit(1)
        self.credentials = {}
        self.credentials["username"] = str(data["ansible_user"])
        self.credentials["password"] = str(data["ansible_password"])
        self.credentials["ndfc_ip"] = str(data["ndfc_ip"])
        self.credentials["discover_username"] = str(data["discover_username"])
        self.credentials["discover_password"] = str(data["discover_password"])

    @property
    def discover_username(self):
        """
        return current value of discover_username
        """
        return self.credentials["discover_username"]

    @property
    def discover_password(self):
        """
        return current value of discover_password
        """
        return self.credentials["discover_password"]

    @property
    def username(self):
        """
        return current value of username
        """
        return self.credentials["username"]

    @property
    def password(self):
        """
        return current value of password
        """
        return self.credentials["password"]

    @property
    def ndfc_ip(self):
        """
        return current value of ndfc_ip
        """
        return self.credentials["ndfc_ip"]
