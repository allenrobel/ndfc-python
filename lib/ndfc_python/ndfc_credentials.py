#!/usr/bin/env python
"""
Description:

Read the caller's Ansible vault and expose the following keys via properties:

ansible_user - via property username
ansible_password - via property password
discover_username - via property discover_username, the switch username
discover_password - via property discover_password, the switch password
ndfc_ip - via property ndfc_ip
nd_domain = via the property nd_domain

Dependencies:

1. Ansible libraries

Install with:

pip install ansible

2. NdfcLoadConfig()

In this repo at lib/ndfc_python/ndfc_config.py

NdfcLoadConfig() loads ndfc_python's settings, which includes the path
to your ansible vault.  To configure this path, edit
ndfc-python/lib/ndfc_python/ndfc_config.py and modify the config_file variable
at the top of the file.
"""
import inspect
import logging
import sys

from ansible.cli import CLI
from ansible.errors import AnsibleFileNotFound, AnsibleParserError
from ansible.parsing.dataloader import DataLoader
from ndfc_python.ndfc_config import NdfcLoadConfig

OUR_VERSION = 106


class NdfcCredentials:
    """
    Unencrypt NDFC and other credentials and provide to the user via properties
    after asking for the ansible vault password.
    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")
        self._init_mandatory_keys()
        self.cred_obj = NdfcLoadConfig()
        self.load_credentials()

    def _init_mandatory_keys(self):
        """
        Initialize a set containing all mandatory keys
        """
        self.mandatory_keys = set()
        self.mandatory_keys.add("ansible_user")
        self.mandatory_keys.add("ansible_password")
        self.mandatory_keys.add("ndfc_ip")
        self.mandatory_keys.add("nd_domain")
        self.mandatory_keys.add("discover_username")
        self.mandatory_keys.add("discover_password")

    def load_credentials(self):
        """
        Load user credentials from ansible vault.  This asked for the ansible
        vault password.
        """
        method_name = inspect.stack()[0][3]
        try:
            loader = DataLoader()
            secrets = CLI.setup_vault_secrets(loader=loader, vault_ids=None)
            loader.set_vault_secrets(secrets)
            data = loader.load_from_file(self.cred_obj.config["ansible_vault"])
        except AnsibleFileNotFound as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Exiting. Unable to load credentials in "
            msg += f" {self.cred_obj.config['ansible_vault']}. "
            msg += f"Exception detail: {exception}"
            self.log.debug(msg)
            sys.exit(1)
        except AnsibleParserError as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Exiting. Unable to load credentials in "
            msg += f" {self.cred_obj.config['ansible_vault']}. "
            msg += f"Exception detail: {exception}"
            self.log.debug(msg)
            sys.exit(1)

        for key in self.mandatory_keys:
            if key not in data:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Exiting. ansible_vault is missing key {key}. "
                msg += f"value file: {self.cred_obj.config['ansible_vault']}"
                self.log.debug(msg)
                sys.exit(1)
        self.credentials = {}
        self.credentials["username"] = str(data["ansible_user"])
        self.credentials["password"] = str(data["ansible_password"])
        self.credentials["nd_domain"] = str(data["nd_domain"])
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
    def nd_domain(self):
        """
        return current value of nd_domain
        """
        return self.credentials["nd_domain"]

    @property
    def ndfc_ip(self):
        """
        return current value of ndfc_ip
        """
        return self.credentials["ndfc_ip"]
