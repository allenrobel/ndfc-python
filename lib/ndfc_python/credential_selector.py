"""
# credential_selector.py

## Summary

Decide which source to use for a credential (e.g. nd_password) and return
the value at that source.

## Description

There can be many (currently three) credentials sources.  This class decides
among command-line (argparse args), environment variables (listed below), and
Ansible Vault (--ansible-vault location passed via argparse args).  It
prioritizes them as follows:

1.  argparse (command line)
2.  environment variable
3.  Ansible Vault (assuming the --ansible-vault argument is present and points
    to a valid vault file)

Given the following, return the value of a credential from the source of
greatest priority.

1. credential_name
2. argparse parser.parse_args() instance

Usage:

from ndfc_python.ndfc_config import CredentialSelector
cs = CredentialsSelector()
cs.script_args = parser.parse_args()
cs.credential_name = "nd_password"
print(f"Would select value: {cs.credential_value}")
"""

import argparse
import inspect
import logging
from os import environ
from typing import Any

from ndfc_python.credentials.credentials_ansible_vault import CredentialsAnsibleVault


class CredentialSelector:
    """
    # CredentialSelector

    ## Summary

    Decide which source to use for a credential (e.g. nd_password) and return
    the value at that source.

    ## Raises

    ### ValueError

    - If `credential_name` cannot be found in any source.
    - If `script_args` is not a parser.parse_args() instance.
    - If ansible_vault is found in `script_args`, and an error
        occurs when reading the vault from the location provided.

    ### Usage example

    #### Script invocation.

    ``` bash title="Script invocation"
    export ND_PASSWORD=MySuperSecretPassword
    ./my_script.py --ansible-vault /tmp/myVault --nd_username admin
    ```

    #### Assumptions

    Assume that the Ansible Vault at location /tmp/myVault contains
    `nd_domain` with value "local" and contains nothing else.


    ### Instantiation

    ``` python title="Instantiation and initial setup"
    instance = CredentialSelector()
    instance.script_args = parser.parse_args()
    ```

    #### nd_username

    ``` python title="Retrieve value of nd_usernaem"
    instance.credential_name = "nd_username"
    instance.commit()
    value = instance.credential_value
    ```

    `value` == "admin"

    #### nd_password

    ``` python title="Retrieve value of nd_password"
    instance.credential_name = "nd_password"
    instance.commit()
    value = instance.credential_value
    ```

    `value` == "MySuperSecretPassword"

    #### nd_domain

    ``` python title="Retrieve value of nd_domain"
    instance.credential_name = "nd_domain"
    instance.commit()
    value = instance.credential_value
    ```

    `value` is "local"

    #### nd_ip4

    ``` python title="Retrieve value of nd_domain"
    instance.credential_name = "nd_ip4"
    instance.commit()
    value = instance.credential_value
    ```

    `ValueError` is raised since no source contains nd_ip4

    ### Notes

    1.  Had `--ansible-vault` not been set on the script command line
        `nd_domain` above would have also raised a ValueError.

    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self._ansible_vault_instance = None
        self._credential_name = None
        self._credential_value = None
        self._script_args = None

    def get_value(self, instance) -> str | None:
        """
        # Summary

        Given instance (a class instance with zero or more of the attributes
        listed below), return the value of self.credential_name, if the
        class instance contains it.

        -   Return the value of self.credential_name if found in
            instance
        -   Return None otherwise.

        ## Attribues

        - nd_domain
        - nd_ip4
        - nd_ip6 (currently not used)
        - nd_password
        - nd_username
        - nxos_password
        - nxos_username

        ## Raises

        None
        """
        value = None
        if instance is None:
            return value
        try:
            if self.credential_name == "nd_ip4":
                value = instance.nd_ip4
            if self.credential_name == "nd_ip6":
                value = instance.nd_ip6
            if self.credential_name == "nd_domain":
                value = instance.nd_domain
            if self.credential_name == "nd_password":
                value = instance.nd_password
            if self.credential_name == "nd_username":
                value = instance.nd_username
            if self.credential_name == "nxos_password":
                value = instance.nxos_password
            if self.credential_name == "nxos_username":
                value = instance.nxos_username
        except AttributeError:
            return None
        return value

    def script_arg_value(self) -> str | None:
        """
        # Summary

        -   Return the value of self.credential_name if found in
            self.script_args
        -   Return None otherwise.

        ## Raises

        None
        """
        return self.get_value(self.script_args)

    def environment_value(self) -> str | None:
        """
        # Summary

        -   Return the value of the environment variable named
            self.credential_name.upper() if it's found in
            the environment.
        -   Return None if the environment variable does not exist.

        ## Example

        Below assumes that nd_username is not in `script_args`.

        ``` bash title="set environment variable"
        export ND_USERNAME="admin"
        ```

        ``` python title="CredentialSelector usage"
        cs = CredentialSelector()
        cs.credential_name = "nd_username"
        cs.commit()
        value = cs.credential_value
        ```

        value == "admin"

        ## Raises

        None
        """
        # This confuses pylint 3.2.6 on Github which reports the following:
        # E1101: Instance of 'CredentialSelector' has no 'upper' member (no-member)
        # pylint 3.3.1 locally doesn't complain.
        return environ.get(self.credential_name.upper())  # pylint: disable=no-member

    def ansible_vault_value(self):
        """
        # Summary

        -   Return the value of self.credential_name if it's found in
            the ansible vault.
        -   Return None if the vault does not contain the variable.
        -   Return None if the ansible vault has not been instantiated.
        """
        if self._ansible_vault_instance is None:
            return None
        return self.get_value(self._ansible_vault_instance)

    def instantiate_ansible_vault(self) -> None:
        """
        # Summary

        Instantiate CredentialsAnsibleVault() if the following
        are true:

        -   self.script_args contains `ansible_vault`
        -   self.ansible_vault_instance is not instantiated

        ## Raises

        ### ValueError

        -   If `script_args` is not set
        -   If an error occurred when reading the Ansible Vault
        """
        method_name = inspect.stack()[0][3]
        ansible_vault = None
        try:
            ansible_vault = self.script_args.ansible_vault
        except AttributeError:
            return
        if ansible_vault is None:
            return

        # If we've already read the vault, do nothing.
        if self._ansible_vault_instance is not None:
            return

        try:
            self._ansible_vault_instance = CredentialsAnsibleVault()
            self._ansible_vault_instance.ansible_vault = ansible_vault
            self._ansible_vault_instance.commit()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Perhaps an incorrect vault password was entered? "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

    def commit(self) -> None:
        """
        # Summary

        Find and set the value of credential_name.

        ## Raises

        ### ValueError

        - If credential_name is not set
        - If script_args is not set
        - If unable to find the value in any credential source
        """
        method_name = inspect.stack()[0][3]
        if self.credential_name is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Call {self.class_name}.credential_name before calling "
            msg += f"{self.class_name}.{method_name}"
            raise ValueError(msg)

        if self.script_args is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Call {self.class_name}.script_args before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        self.instantiate_ansible_vault()

        if self.script_arg_value() is not None:
            self.credential_value = self.script_arg_value()
        elif self.environment_value() is not None:
            self.credential_value = self.environment_value()
        elif self.ansible_vault_value() is not None:
            self.credential_value = self.ansible_vault_value()
        else:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to find value for {self._credential_name}"
            raise ValueError(msg)

    @property
    def credential_name(self) -> str:
        """
        The name of the credential for which a value is desired.
        """
        return self._credential_name

    @credential_name.setter
    def credential_name(self, value: str):
        self._credential_name = value

    @property
    def credential_value(self) -> Any:
        """
        The value of credential_name.
        """
        return self._credential_value

    @credential_value.setter
    def credential_value(self, value):
        self._credential_value = value

    @property
    def script_args(self) -> argparse.Namespace:
        """
        # Summary

        The value of script_args.

        `script_args` must be an instance of argparse's parser.parse_args()

        ## Example

        ``` python title="Example"
        import argparse

        parser_help = "Absolute path to an Ansible Vault. "
        parser_help += "e.g. /home/myself/.ansible/vault. "

        parser_ansible_vault = argparse.ArgumentParser(add_help=False)
        optional = parser_ansible_vault.add_argument_group(title="OPTIONAL ARGS")
        optional.add_argument(
            "-v",
            "--ansible-vault",
            dest="ansible_vault",
            required=False,
            default=None,
            help=f"{parser_help}",
        )
        script_args = parser_ansible_vault.parse_args()

        CredentialSelector().script_args = script_args
        ```
        """
        return self._script_args

    @script_args.setter
    def script_args(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, argparse.Namespace):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{method_name} must be an instance of argparse.Namespace"
            # Yes, should be TypeError. Using ValueError for simplicity.
            raise ValueError(msg)
        self._script_args = value
