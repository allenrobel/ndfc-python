#!/usr/bin/env python
"""
# Description

Read an Ansible vault for the following keys and expose
them via properties of the same name.  These keys must
exist in the vault.

- nd_domain
  - Nexus Dashboard login domain
- nd_ip4
  - Nexus Dashboard IPv4 address
- nd_password
  - Nexus Dashboard password
- nd_username
  - Nexus Dashboard username
- nxos_password
  - NX-OS switches password
  - Used for Nexus Dashboard Fabric Contoller switch discovery
- nxos_username
  - NX-OS switches username
  - Used for Nexus Dashboard Fabric Contoller switch discovery

## Dependencies

1. Ansible

pip install ansible

"""
import inspect
import logging

from ansible.cli import CLI
from ansible.errors import AnsibleFileNotFound, AnsibleParserError
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.vault import AnsibleVaultError, AnsibleVaultPasswordError


class CredentialsAnsibleVault:
    """
    Unencrypt NDFC and other credentials and provide to the user via properties
    after asking for the ansible vault password.
    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self._ansible_vault = None
        self.credentials = {}

        self.mandatory_vault_keys = set()
        self.mandatory_vault_keys.add("nd_domain")
        self.mandatory_vault_keys.add("nd_ip4")
        self.mandatory_vault_keys.add("nd_password")
        self.mandatory_vault_keys.add("nd_username")
        self.mandatory_vault_keys.add("nxos_password")
        self.mandatory_vault_keys.add("nxos_username")

    def commit(self):
        """
        Load user credentials from ansible vault.  This asked for the ansible
        vault password.
        """
        method_name = inspect.stack()[0][3]

        if self.ansible_vault is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "set instance.ansible_vault before calling commit."
            raise ValueError(msg)

        try:
            loader = DataLoader()
            secrets = CLI.setup_vault_secrets(loader=loader, vault_ids=None)
            loader.set_vault_secrets(secrets)
            data = loader.load_from_file(self.ansible_vault)
        except AnsibleFileNotFound as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Unable to load credentials in "
            msg += f" {self.ansible_vault}. "
            msg += f"Exception detail: AnsibleFileNotFound: {error}"
            raise ValueError(msg) from error
        except AnsibleParserError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Unable to load credentials in "
            msg += f" {self.ansible_vault}. "
            msg += f"Exception detail: AnsibleParserError: {error}"
            raise ValueError(msg) from error
        except AnsibleVaultPasswordError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Unable to load credentials in "
            msg += f" {self.ansible_vault}. "
            msg += f"Exception detail: AnsibleVaultPasswordError: {error}"
            raise ValueError(msg) from error

        for key in self.mandatory_vault_keys:
            if key not in data:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"ansible_vault is missing key {key}. "
                msg += f"vault file: {self.ansible_vault}"
                raise ValueError(msg)

        try:
            self.credentials = {}
            self.credentials["nd_domain"] = str(data["nd_domain"])
            self.credentials["nd_ip4"] = str(data["nd_ip4"])
            self.credentials["nd_password"] = str(data["nd_password"])
            self.credentials["nd_username"] = str(data["nd_username"])
            self.credentials["nxos_password"] = str(data["nxos_password"])
            self.credentials["nxos_username"] = str(data["nxos_username"])
        except AnsibleVaultError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Perhaps an incorrect Ansible Vault password was entered? "
            msg += f"Error detail: AnsibleVaultError: {error}"
            raise ValueError(error) from error

    @property
    def ansible_vault(self):
        """
        Path to the Ansible Vault file.
        """
        return self._ansible_vault

    @ansible_vault.setter
    def ansible_vault(self, value):
        self._ansible_vault = value

    @property
    def nd_domain(self):
        """
        return current value of nd_domain
        """
        return self.credentials["nd_domain"]

    @property
    def nd_ip4(self):
        """
        return current value of nd_ip4
        """
        return self.credentials["nd_ip4"]

    @property
    def nd_password(self):
        """
        return current value of nd_password
        """
        return self.credentials["nd_password"]

    @property
    def nd_username(self):
        """
        return current value of nd_username
        """
        return self.credentials["nd_username"]

    @property
    def nxos_password(self):
        """
        return current value of nxos_password
        """
        return self.credentials["nxos_password"]

    @property
    def nxos_username(self):
        """
        return current value of nxos_username
        """
        return self.credentials["nxos_username"]
