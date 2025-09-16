"""
# Name

network_detach.py

# Description

Send network detach POST requests to the controller

# Payload Example

network detach operation is determined by lanAttachList[x].deployment == false

```json
[
    {
        "networkName": "v1n1",
        "lanAttachList": [
            {
                "deployment": "false",
                "detachSwitchPorts": "Ethernet1/2",
                "fabric": "SITE3",
                "networkName": "v1n1",
                "serialNumber": "12345678",
                "vlan": "2301",
            }
        ]
    }
]
```
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
from ndfc_python.common.fabric.fabrics_info import FabricsInfo
from ndfc_python.common.properties import Properties
from ndfc_python.validations import Validations


class NetworkDetach:
    """
    # Summary

    Detach networks

    ## Example network detach request

    ### See

    ./examples/network_detach.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.fabrics_info = FabricsInfo()
        self.properties = Properties()
        self.rest_send = self.properties.rest_send
        self.results = self.properties.results

        self.fabric_inventory = FabricInventory()
        self.validations = Validations()

        self.api_v1 = "/appcenter/cisco/ndfc/api/v1"
        self.ep_fabrics = f"{self.api_v1}/lan-fabric/rest/top-down/fabrics"

        self._detach_switch_ports = ""
        self._fabric_name = ""
        self._network_name = ""
        self._peer_switch_name = ""
        self._switch_name = ""
        self._vlan = ""

    def _list_to_string(self, lst: list[str]) -> str:
        """
        Convert a list of strings to a comma-separated string.
        Empty list is converted to ""
        """
        return ",".join(lst)

    def _final_verification(self):
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        if self.rest_send is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.rest_send must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.results is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.results must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        if self.network_name_exists_in_fabric() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"networkName {self.network_name} does not exist "
            msg += f"in fabric {self.fabric_name}."
            raise ValueError(msg)

        if not self.switch_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "switch_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.peer_switch_name:
            if self.peer_switch_name == self.switch_name:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"peer_switch_name {self.peer_switch_name} must differ "
                msg += f"from switch_name {self.switch_name}."
                raise ValueError(msg)
            if self.peer_switch_name not in self.fabric_inventory.devices:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"peer_switch_name {self.peer_switch_name} "
                msg += f"not found in fabric {self.fabric_name}."
                raise ValueError(msg)
            if not self.fabric_inventory.is_vpc_peer(self.switch_name, self.peer_switch_name):
                msg = f"{self.class_name}.{method_name}: "
                msg += f"switch_name {self.switch_name} and "
                msg += f"peer_switch_name {self.peer_switch_name} "
                msg += "are not vPC peer switches."
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

    def network_name_exists_in_fabric(self):
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

    def _build_lan_attach_list_item(self, switch_name: str) -> dict:
        """
        Build and return a lanAttachList item for the given switch_name
        """
        method_name = inspect.stack()[0][3]
        _lan_attach_list_item = {}
        _lan_attach_list_item["deployment"] = False
        _lan_attach_list_item["detachSwitchPorts"] = self.detach_switch_ports
        _lan_attach_list_item["fabric"] = self.fabric_name
        _lan_attach_list_item["networkName"] = self.network_name
        try:
            _lan_attach_list_item["serialNumber"] = self.fabric_inventory.switch_name_to_serial_number(switch_name)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to get serial number for switch_name {switch_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        _lan_attach_list_item["vlan"] = self.vlan
        return _lan_attach_list_item

    def _build_payload(self) -> list[dict]:
        """
        Build and return the payload for the API request
        """
        _payload = []
        _payload_item = {}
        _payload_item["networkName"] = self.network_name
        _lan_attach_list = []
        _lan_attach_list.append(self._build_lan_attach_list_item(self.switch_name))
        if self.peer_switch_name:
            _lan_attach_list.append(self._build_lan_attach_list_item(self.peer_switch_name))

        _payload_item["lanAttachList"] = _lan_attach_list
        _payload.append(_payload_item)
        return _payload

    def commit(self) -> None:
        """
        Detach a network from a switch
        """
        method_name = inspect.stack()[0][3]
        self.fabric_inventory.fabric_name = self.fabric_name
        self.fabric_inventory.rest_send = self.rest_send
        self.fabric_inventory.results = self.results
        self.fabric_inventory.commit()

        self._final_verification()
        payload = self._build_payload()

        # TODO: Update when we add endpoint to ansible-dcnm
        path = f"{self.ep_fabrics}/{self.fabric_name}/networks/attachments"
        verb = "POST"

        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.payload = payload
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

    @property
    def detach_switch_ports(self) -> str:
        """
        Set (setter) or return (getter) the current value of detach_switch_ports

        detach_switch_ports is converted from a list to a comma-separated string in the setter.
        """
        return self._detach_switch_ports

    @detach_switch_ports.setter
    def detach_switch_ports(self, value: list[str]) -> None:
        self._detach_switch_ports = self._list_to_string(value)

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

    @property
    def peer_switch_name(self) -> str:
        """
        Set (setter) or return (getter) the current value of peer_switch_name
        """
        return self._peer_switch_name

    @peer_switch_name.setter
    def peer_switch_name(self, value: str) -> None:
        self._peer_switch_name = value

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
    def vlan(self) -> str:
        """
        Set (setter) or return (getter) the current value of vlan
        """
        return self._vlan

    @vlan.setter
    def vlan(self, value: str) -> None:
        self.validations.verify_vlan(value)
        self._vlan = value
