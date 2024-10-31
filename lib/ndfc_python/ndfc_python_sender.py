# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import argparse  # used for validating args
import inspect
import logging

from ndfc_python.credential_selector import CredentialSelector
from plugins.module_utils.common.sender_requests import Sender


class NdfcPythonSender:
    """
    ### Summary

    Instantiate and configure Sender()

    ### Example usage

    args is an argparse.Namespace object containing:
    - domain : The login domain for the Nexus Dashboard controller
    - ip4 : The IPv4 address of the Nexus Dashboard controller
    - password : The login password for the Nexus Dashboard controller
    - username : The login username for the Nexus Dashboard controller

    ```python
    try:
        ndfc_sender = NdfcPythonSender()
        ndfc_sender.args = args
        ndfc_sender.commit()
    except ValueError as error:
        msg = f"Exiting.  Error detail: {error}"
        log.error(msg)
        sys.exit(1)

    # The logged-in Sender() instance can now be passed to RestSend()

    rest_send.sender = ndfc_sender.sender
    ```

    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")
        self._args = None
        self._credential_names = []
        self._credential_names.append("nd_domain")
        self._credential_names.append("nd_ip4")
        self._credential_names.append("nd_password")
        self._credential_names.append("nd_username")
        self._credential_names.append("nxos_password")
        self._credential_names.append("nxos_username")
        self._sender = Sender()
        self._nd_domain = None
        self._nd_ip4 = None
        self._nd_password = None
        self._nd_username = None
        self._nxos_password = None
        self._nxos_username = None

    @property
    def args(self):
        """
        # Summary
        args is optional.

        If not set, Sender() will read Nexus Dashboard credentials from
        environment variables:

        - ND_DOMAIN : The login domain for the Nexus Dashboard controller
        - ND_IP4 : The IPv4 address of the Nexus Dashboard controller
        - ND_PASSWORD : The login password for the Nexus Dashboard controller
        - ND_USERNAME : The login username for the Nexus Dashboard controller

        If set, it must be an argparse.Namespace instance containing one or
        more of:

        - nd_domain : The login domain for the Nexus Dashboard controller
        - nd_ip4 : The IPv4 address of the Nexus Dashboard controller
        - nd_password : The login password for the Nexus Dashboard controller
        - nd_username : The login username for the Nexus Dashboard controller
        """
        return self._args

    @args.setter
    def args(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, argparse.Namespace):
            msg = f"{self.class_name}.{method_name}: "
            msg += "args must be an argparse.Namespace instance."
            raise ValueError(msg)
        self._args = value

    @property
    def sender(self):
        """
        # Summary
        Return an instance of Sender().
        """
        return self._sender

    def set_sender_credentials(self) -> None:
        """
        # Summary

        Use CredentialSelector to get Nexus Dashboard credentials from
        environment variables, args, or an Ansible Vault.
        """
        method_name = inspect.stack()[0][3]
        cs = CredentialSelector()
        cs.script_args = self.args
        for credential in self._credential_names:
            cs.credential_name = credential
            try:
                cs.commit()
            except ValueError as error:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Got error {error}"
                raise ValueError(msg) from error
            if credential == "nd_domain":
                self.sender.domain = cs.credential_value
                self._nd_domain = cs.credential_value
            if credential == "nd_ip4":
                self.sender.ip4 = cs.credential_value
                self._nd_ip4 = cs.credential_value
            if credential == "nd_password":
                self.sender.password = cs.credential_value
                self._nd_password = cs.credential_value
            if credential == "nd_username":
                self.sender.username = cs.credential_value
                self._nd_username = cs.credential_value
            if credential == "nxos_password":
                self._nxos_password = cs.credential_value
            if credential == "nxos_username":
                self._nxos_username = cs.credential_value

    def commit(self) -> None:
        """
        # Summary
        Initiate login to the Nexus Dashboard controller.

        # Raises
        - ValueError if:
            -   sender.login() is not successful
        """
        method_name = inspect.stack()[0][3]
        self.set_sender_credentials()
        try:
            self.sender.login()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Unable to login to the controller. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

    @property
    def nd_domain(self):
        """
        # Summary
        Return the Nexus Dashboard domain.
        """
        return self._nd_domain

    @property
    def nd_ip4(self):
        """
        # Summary
        Return the Nexus Dashboard IPv4 address.
        """
        return self._nd_ip4

    @property
    def nd_password(self):
        """
        # Summary
        Return the Nexus Dashboard password.
        """
        return self._nd_password

    @property
    def nd_username(self):
        """
        # Summary
        Return the Nexus Dashboard username.
        """
        return self._nd_username

    @property
    def nxos_password(self):
        """
        # Summary
        Return the NX-OS password.
        """
        return self._nxos_password

    @property
    def nxos_username(self):
        """
        # Summary
        Return the NX-OS username.
        """
        return self._nxos_username
