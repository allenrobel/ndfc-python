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

import inspect
import logging
import sys
from os import environ

import yaml


class NdfcLoadConfig:
    """
    When instantiated, load the YAML file pointed to by NDFC_CONFIG_FILE
    environment variable, and set self.properties["config"] to the contents of
    this file.  self.properties["config"] will be a python dictionary
    representing the contents of CONFIG_FILE.

    The (current) mandatory keys in CONFIG_FILE are:

    ansible_vault : path to the Ansible Vault file to load.

    Example CONFIG_FILE:

    ansible_vault: "/path/to/my/ansible/vault"

    Used by NdfcCredentials() in ndfc_credentials.py
    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.config_file = environ.get("NDFC_PYTHON_CONFIG", None)
        if self.config_file is None:
            msg = "Missing NDFC_PYTHON_CONFIG environment variable. "
            msg += "Set NDFC_PYTHON_CONFIG to point to your ndfc-python "
            msg += "configuration file. For example: "
            msg += "export NDFC_PYTHON_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python"
            msg += "/config/config.yml"
            self.log.error(msg)
            sys.exit(1)
        self.properties = {}
        self.mandatory_keys = set()
        self.mandatory_keys.add("ansible_vault")
        self.load_config()
        self.verify_mandatory_keys()

    def verify_mandatory_keys(self):
        """
        Exit if all mandatory keys are not present in self.properties["config"]
        """
        method_name = inspect.stack()[0][3]
        for key in self.mandatory_keys:
            if key in self.properties["config"]:
                continue
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting. missing mandatory key {key} in config file "
            msg += f"{self.config_file}"
            print(msg)
            sys.exit(1)

    def load_config(self):
        """
        Open the YAML self.config_file, and load its contents
        into self.properties["config"]
        """
        method_name = inspect.stack()[0][3]
        try:
            with open(self.config_file, "r", encoding="utf-8") as handle:
                self.properties["config"] = yaml.safe_load(handle)
        except FileNotFoundError as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting. config file not found {self.config_file}"
            msg += f"Exception detail: {exception}"
            self.log.error(msg)
            sys.exit(1)
        except EOFError as exception:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Exiting. config file {self.config_file} "
            msg += "has no contents? "
            msg += f"Exception detail: {exception}"
            self.log.error(msg)
            sys.exit(1)
        if self.properties["config"] is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Exiting. No key/values found in config file: "
            msg += f"{self.config_file}"
            self.log.error(msg)
            sys.exit(1)

    @property
    def config(self):
        """
        Return the config dictionary (see load_config)
        """
        return self.properties["config"]
