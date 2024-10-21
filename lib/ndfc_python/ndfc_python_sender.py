import argparse  # used for validating args
import inspect
import logging

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
        self._sender = Sender()

    @property
    def args(self):
        """
        # Summary
        args is optional.

        If not set, Sender() will read Nexus Dashboard credentials from
        environment variables:

        - NDFC_DOMAIN : The login domain for the Nexus Dashboard controller
        - NDFC_IP4 : The IPv4 address of the Nexus Dashboard controller
        - NDFC_PASSWORD : The login password for the Nexus Dashboard controller
        - NDFC_USERNAME : The login username for the Nexus Dashboard controller

        If set, it must be an argparse.Namespace instance containing one or
        more of:

        - ndfc_domain : The login domain for the Nexus Dashboard controller
        - ndfc_ip4 : The IPv4 address of the Nexus Dashboard controller
        - ndfc_password : The login password for the Nexus Dashboard controller
        - ndfc_username : The login username for the Nexus Dashboard controller
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

    def commit(self) -> None:
        """
        # Summary
        Initiate login to the Nexus Dashboard controller.

        # Raises
        - ValueError if:
            -   sender.login() is not successful
        """
        method_name = inspect.stack()[0][3]
        if self.args is not None:
            # If args contains any of the following, override the corresponding
            # environment variable.
            try:
                if self.args.controller_domain is not None:
                    # override NDFC_DOMAIN env variable
                    self.sender.domain = self.args.controller_domain
            except AttributeError:
                pass
            try:
                if self.args.controller_ip4 is not None:
                    # override NDFC_IP4 env variable
                    self.sender.ip4 = self.args.controller_ip4
            except AttributeError:
                pass
            try:
                if self.args.controller_password is not None:
                    # override NDFC_PASSWORD env variable
                    self.sender.password = self.args.controller_password
            except AttributeError:
                pass
            try:
                if self.args.controller_username is not None:
                    # override NDFC_USERNAME env variable
                    self.sender.username = self.args.controller_username
            except AttributeError:
                pass
        try:
            self.sender.login()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Unable to login to the controller. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
