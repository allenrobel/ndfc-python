"""
ndfc_config.py

Description:

Load YAML file pointed to by the config_file variable, verify all mandatory keys are present,
and return the contents as a python dict()

Usage:

from ndfc_python.ndfc_config import NdfcLoadConfig
c = NdfcLoadConfig()
print(f"c.ansible_vault {c.config['ansible_vault']}")
"""
import sys

import yaml

config_file = "/Users/arobel/repos/ndfc-python/lib/ndfc_python/config/config.yml"


class NdfcLoadConfig:
    """
    When instantiated, load the YAML file pointed to by config_file (at the
    top of this file) and set self.properties["config"] to the contents of
    this file.  self.properties["config"] will be a python dictionary representing
    the contents of config_file.

    The (current) mandatory keys in config_file are:

    ansible_vault : path to the Ansible Vault file to load.

    Example config_file:

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
            print(
                f"Exiting. {__class__.__name__}.load_config() - missing mandatory key '{key}'"
                f" in config_file {config_file}"
            )
            sys.exit(1)

    def load_config(self):
        """
        Open the YAML file, config_file, and load its contents
        into self.properties["config"]
        """
        try:
            with open(config_file, "r", encoding="utf-8") as fp:
                self.properties["config"] = yaml.safe_load(fp)
        except FileNotFoundError as exception:
            print(
                f"Exiting. {__class__.__name__}."
                f"load_config() - config_file not found: {config_file}"
                f" Exception detail: {exception}"
            )
            sys.exit(1)
        except EOFError as exception:
            print(
                f"Exiting. {__class__.__name__}."
                f"load_config() - config_file {config_file} has no contents?"
                f" Exception detail: {exception}"
            )
            sys.exit(1)
        if self.properties["config"] is None:
            print(
                f"Exiting. {__class__.__name__}."
                f"load_config() - No key/values found in config_file {config_file}"
            )
            sys.exit(1)

    @property
    def config(self):
        """
        Return the config dictionary (see load_config)
        """
        return self.properties["config"]
