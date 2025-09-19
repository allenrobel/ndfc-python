"""
# Name

policy_info_switch.py

# Description

Send GET request to the controller for policy information for a specific switch.

# Endpoint

Verb: GET
Path: /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/switches?serialNumber=<serialNumber>

"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
from ndfc_python.common.fabric.fabrics_info import FabricsInfo
from ndfc_python.common.properties import Properties


class PolicyInfoSwitchEndpoint:
    """
    PolicyInfoSwitchEndpoint class to build the endpoint for the PolicyInfoSwitch API request
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.apiv1 = "/appcenter/cisco/ndfc/api/v1"
        self._path = f"{self.apiv1}/lan-fabric/rest/control/policies/switches?serialNumber="
        self.serial_number = ""
        self._verb = "GET"
        self._committed = False

    def _final_verification(self) -> None:
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        if not self.serial_number:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.serial_number must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

    def commit(self) -> None:
        """
        Build the endpoint path for the API request
        """
        self._path = f"{self._path}{self.serial_number}"
        self._committed = True

    @property
    def path(self) -> str:
        """
        Return the endpoint path.

        instance.commit() must be called before accessing this property.
        """
        method_name = inspect.stack()[0][3]
        if not self._committed:
            method_name = inspect.stack()[0][3]
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.commit() must be called before accessing "
            msg += f"{self.class_name}.{method_name}"
            raise ValueError(msg)
        return self._path

    @property
    def verb(self) -> str:
        """
        return the current value of verb
        """
        return self._verb

    @property
    def serial_number(self) -> str:
        """
        return the current value of serial_number
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value: str) -> None:
        self._serial_number = value


class PolicyInfoSwitch:
    """
    # Summary

    Get switch policy information

    ## Example switch policy info request

    ### See

    ./examples/policy_info_switch.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.endpoint = PolicyInfoSwitchEndpoint()
        self.fabric_inventory = FabricInventory()
        self.fabrics_info = FabricsInfo()
        self.properties = Properties()

        self.rest_send = self.properties.rest_send
        self._policies = []
        self._policies_populated = False
        self._fabric_inventory_populated = False

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

        if not self.fabric_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.fabric_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if not self.switch_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.switch_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        if not self._fabric_inventory_populated:
            self.populate_fabric_inventory()

        if self.switch_name not in self.fabric_inventory.devices:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"switch_name {self.switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)

    def commit(self) -> None:
        """
        Retrieve switch policy information from the controller.
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        self.endpoint.serial_number = self.fabric_inventory.switch_name_to_serial_number(self.switch_name)
        self.endpoint.commit()

        try:
            self.rest_send.path = self.endpoint.path
            self.rest_send.verb = self.endpoint.verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        self._populate_policies()

    def fabric_exists(self) -> bool:
        """
        Return True if self.fabric_name exists on the controller.
        Return False otherwise.
        """
        self.fabrics_info.rest_send = self.rest_send
        self.fabrics_info.commit()
        self.fabrics_info.filter = self.fabric_name
        return self.fabrics_info.fabric_exists

    def populate_fabric_inventory(self) -> None:
        """
        Get switch inventory for a specific fabric.
        """
        try:
            self.fabric_inventory.fabric_name = self.fabric_name
            self.fabric_inventory.rest_send = self.rest_send
            self.fabric_inventory.commit()
        except ValueError as error:
            msg = f"{self.class_name}.populate_fabric_inventory: "
            msg += f"Unable to populate fabric inventory for fabric {self.fabric_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._fabric_inventory_populated = True

    def _populate_policies(self) -> None:
        """
        # Summary

        Populate switch policies for switch_name.

        ## Raises

        - ValueError: if FabricInventory raises

        """
        method_name = inspect.stack()[0][3]
        switch_policy_endpoint = PolicyInfoSwitchEndpoint()
        switch_policy_endpoint.serial_number = self.fabric_inventory.switch_name_to_serial_number(self.switch_name)
        switch_policy_endpoint.commit()
        path = f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/switches?serialNumber={self.fabric_inventory.switch_name_to_serial_number(self.switch_name)}"
        verb = "GET"
        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.payload = None
            self.rest_send.commit()
            self._policies = self.rest_send.response_current.get("DATA", [])
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to populate switch policies for switch {self.switch_name} "
            msg += f"in fabric {self.fabric_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._policies_populated = True

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
    def switch_name(self) -> str:
        """
        Set (setter) or return (getter) the current value of switch_name
        """
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value: str) -> None:
        self._switch_name = value

    @property
    def policies(self) -> str:
        """
        Return the current value of policies
        """
        return self._policies
