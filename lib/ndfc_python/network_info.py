"""
# Name

network_info.py

# Description

Send GET request to the controller for network information

# Endpoint

Verb: GET
Path: /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{{fabric_name}}/networks/{{network_name}}

"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from ndfc_python.common.fabric.fabrics_info import FabricsInfo
from ndfc_python.common.properties import Properties
from ndfc_python.validations import Validations


class NetworkInfoEndpoint:
    """
    NetworkInfoEndpoint class to build the endpoint for the NetworkInfo API request
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.apiv1 = "/appcenter/cisco/ndfc/api/v1"
        self.ep_fabrics = f"{self.apiv1}/lan-fabric/rest/top-down/fabrics"

        self._path = ""
        self._fabric_name = ""
        self._network_name = ""

        self.verb = "GET"

    def _final_verification(self) -> None:
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        if not self.fabric_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.fabric_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if not self.network_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.network_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

    def commit(self) -> None:
        """
        Build and return the endpoint for the API request
        """
        self.path = f"{self.ep_fabrics}/{self.fabric_name}/networks/{self.network_name}"

    @property
    def path(self) -> str:
        """
        Set (setter) or return (getter) the current value of the endpoint path
        """
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value

    @property
    def fabric_name(self) -> str:
        """
        return the current value of fabric
        """
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value: str) -> None:
        self._fabric_name = value

    @property
    def network_name(self) -> str:
        """
        return the current value of networkName
        """
        return self._network_name

    @network_name.setter
    def network_name(self, value: str) -> None:
        self._network_name = value


class NetworkInfo:
    """
    # Summary

    Get network information

    ## Example network info request

    ### See

    ./examples/network_info.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.fabrics_info = FabricsInfo()
        self.endpoint = NetworkInfoEndpoint()
        self.properties = Properties()
        self.validations = Validations()

        self.rest_send = self.properties.rest_send

        self._fabric_name = ""
        self._network_name = ""

    def _final_verification(self) -> None:
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        if self.rest_send is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.rest_send must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        if self.network_name_exists_in_fabric() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"network_name {self.network_name} does not exist "
            msg += f"in fabric {self.fabric_name}."
            raise ValueError(msg)

    def fabric_exists(self) -> bool:
        """
        Return True if self.fabric_name exists on the controller.
        Return False otherwise.
        """
        self.fabrics_info.rest_send = self.rest_send
        self.fabrics_info.commit()
        self.fabrics_info.filter = self.fabric_name
        return self.fabrics_info.fabric_exists

    def network_name_exists_in_fabric(self) -> bool:
        """
        Return True if networkName exists in the fabric.
        Else return False
        """
        method_name = inspect.stack()[0][3]
        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/networks"
        verb = "GET"

        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        for item in self.rest_send.response_current["DATA"]:
            if "networkName" not in item:
                continue
            if item["networkName"] == self.network_name:
                return True
        return False

    def commit(self) -> None:
        """
        Retrieve network information from the controller.
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        self.endpoint.fabric_name = self.fabric_name
        self.endpoint.network_name = self.network_name
        self.endpoint.commit()
        path = self.endpoint.path
        verb = self.endpoint.verb

        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

    @property
    def fabric_name(self) -> str:
        """
        Set (setter) or return (getter) the current value of fabric_name
        """
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value: str) -> None:
        self._fabric_name = value

    @property
    def network_name(self) -> str:
        """
        Set (setter) or return (getter) the current value of network_name
        """
        return self._network_name

    @network_name.setter
    def network_name(self, value: str) -> None:
        self._network_name = value
