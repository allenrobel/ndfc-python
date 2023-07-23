"""
ndfc_config.py

Description:

Load YAML file pointed to by CONFIG_FILE, verify all mandatory keys are
present, and return the contents as a python dict()

Edit the CONFIG_FILE constant below to point to your configuration file.

Usage:

from ndfc_python.ndfc_config import NdfcLoadConfig
c = NdfcLoadConfig()
print(f"c.ansible_vault {c.config['ansible_vault']}")
"""
import sys
from os import environ

import yaml

REPOS = f"{environ['HOME']}/repos"
# Edit me!
CONFIG_FILE = f"{REPOS}/ndfc-python/lib/ndfc_python/config/config.yml"


class NdfcLoadConfig:
    """
    When instantiated, load the YAML file pointed to by CONFIG_FILE (at the
    top of this file) and set self.properties["config"] to the contents of
    this file.  self.properties["config"] will be a python dictionary
    representing the contents of CONFIG_FILE.

    The (current) mandatory keys in CONFIG_FILE are:

    ansible_vault : path to the Ansible Vault file to load.

    Example CONFIG_FILE:

    ansible_vault: "/path/to/my/ansible/vault"

    Used by NdfcCredentials() in ndfc_credentials.py
    """

    def __init__(self):
        self.properties = {}
        self.mandatory_keys = set()
        self.mandatory_keys.add("ansible_vault")
        self.load_config()
        self.verify_mandatory_keys()

    def verify_mandatory_keys(self):
        """
        Exit if all mandatory keys are not present in self.properties["config"]
        """
        for key in self.mandatory_keys:
            if key in self.properties["config"]:
                continue
            msg = f"Exiting. {__class__.__name__}.load_config() - missing "
            msg += f"mandatory key '{key}' in CONFIG_FILE {CONFIG_FILE}"
            print(msg)
            sys.exit(1)

    def load_config(self):
        """
        Open the YAML file, CONFIG_FILE, and load its contents
        into self.properties["config"]
        """
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as handle:
                self.properties["config"] = yaml.safe_load(handle)
        except FileNotFoundError as exception:
            print(
                f"Exiting. {__class__.__name__}."
                f"load_config() - CONFIG_FILE not found: {CONFIG_FILE}"
                f" Exception detail: {exception}"
            )
            sys.exit(1)
        except EOFError as exception:
            print(
                f"Exiting. {__class__.__name__}."
                f"load_config() - CONFIG_FILE {CONFIG_FILE} has no contents?"
                f" Exception detail: {exception}"
            )
            sys.exit(1)
        if self.properties["config"] is None:
            msg = f"Exiting. {__class__.__name__}. "
            msg += "load_config() - No key/values found in CONFIG_FILE "
            msg += f"{CONFIG_FILE}"
            print(msg)
            sys.exit(1)

    @property
    def config(self):
        """
        Return the config dictionary (see load_config)
        """
        return self.properties["config"]
