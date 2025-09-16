"""
# Name

network_attach.py

# Description

Send network attach POST requests to the controller

# Payload Example

```json
[
    {
        "networkName": "{{network_1_name}}",
        "lanAttachList": [
            {
                "deployment": "true",
                "detachSwitchPorts": "",
                "dot1QVlan": "",
                "extensionValues": "",
                "fabric": "{{fabric_1}}",
                "freeformConfig": "",
                "instanceValues": "",
                "msoCreated": "false",
                "msoSetVlan": "false",
                "networkName": "{{network_1_name}}",
                "serialNumber": "{{switch_1_serial_number}}",
                "switchPorts": "Ethernet1/11",
                "torPorts": "",
                "untagged": "true",
                "vlan": "{{network_1_vlan_id}}",
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


class NetworkAttach:
    """
    # Summary

    Attach networks

    ## Example network attach request

    ### See

    ./examples/network_attach.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.fabrics_info = FabricsInfo()
        self.properties = Properties()
        self.rest_send = self.properties.rest_send
        self.results = self.properties.results

        self.validations = Validations()

        self.api_v1 = "/appcenter/cisco/ndfc/api/v1"
        self.ep_fabrics = f"{self.api_v1}/lan-fabric/rest/top-down/fabrics"
        self.fabric_inventory = FabricInventory()

        self._detach_switch_ports = ""
        self._dot1q_vlan = ""
        self._extension_values = ""
        self._fabric_inventory_populated = False
        self._fabric_name = ""
        self._freeform_config = ""
        self._instance_values = ""
        self._network_name = ""
        self._peer_switch_name = ""
        self._rest_send = None
        self._results = None
        self._switch_name = ""
        self._switch_ports = ""
        self._tor_ports = ""
        self._untagged = False
        self._vlan = ""

    def _list_to_string(self, lst: list[str]) -> str:
        """
        Convert a list of strings to a comma-separated string.
        Empty list is converted to ""
        """
        return ",".join(lst)

    def _freeform_config_to_string(self, lst: list[str]) -> str:
        """
        Convert the freeform config list to a newline-separated string.
        Empty list is converted to ""
        """
        return "\n".join(lst)

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

        if self.results is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.results must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if not self.fabric_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "fabric_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if not self.network_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "network_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if not self.switch_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "switch_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.peer_switch_name == self.switch_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"peer_switch_name {self.peer_switch_name} must be different from switch_name {self.switch_name}"
            raise ValueError(msg)

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        if not self._fabric_inventory_populated:
            self.populate_fabric_inventory()

        if self.network_name_exists_in_fabric() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"networkName {self.network_name} does not exist "
            msg += f"in fabric {self.fabric_name}. "
            msg += f"Create it first before calling {self.class_name}.commit"
            raise ValueError(msg)

        if self.switch_name not in self.fabric_inventory.devices:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"switch_name {self.switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)

        if self.peer_switch_name:

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

    def populate_fabric_inventory(self) -> None:
        """
        # Summary

        Populate switch inventory for fabric_name.

        ## Raises

        - ValueError: if FabricInventory raises

        """
        method_name = inspect.stack()[0][3]
        try:
            self.fabric_inventory.fabric_name = self.fabric_name
            self.fabric_inventory.rest_send = self.rest_send
            self.fabric_inventory.results = self.results
            self.fabric_inventory.commit()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to populate fabric inventory for fabric {self.fabric_name}. "
            if self.fabric_inventory.return_code == 404:
                msg += f"fabric_name {self.fabric_name} does not exist on the controller. "
            else:
                msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._fabric_inventory_populated = True

    def _build_lan_attach_list_item(self, switch_name: str) -> dict:
        """
        Build and return a single item for the lanAttachList
        """
        _lan_attach_list_item = {}
        _lan_attach_list_item["deployment"] = True
        _lan_attach_list_item["detachSwitchPorts"] = self.detach_switch_ports
        _lan_attach_list_item["dot1QVlan"] = self.dot1q_vlan
        _lan_attach_list_item["extensionValues"] = self.extension_values
        _lan_attach_list_item["fabric"] = self.fabric_name
        _lan_attach_list_item["freeformConfig"] = self.freeform_config
        _lan_attach_list_item["instanceValues"] = self.instance_values
        _lan_attach_list_item["networkName"] = self.network_name
        try:
            _lan_attach_list_item["serialNumber"] = self.fabric_inventory.switch_name_to_serial_number(switch_name)
        except ValueError as error:
            msg = f"{self.class_name}._build_lan_attach_list_item: "
            msg += f"Unable to get serial number for switch_name {switch_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        _lan_attach_list_item["switchPorts"] = self.switch_ports
        _lan_attach_list_item["torPorts"] = self.tor_ports
        _lan_attach_list_item["untagged"] = self.untagged
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
        Attach a network to a switch
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
        return the current value of detachSwitchPorts

        detachSwitchPorts is converted from a list to a comma-separated string in the setter.
        """
        return self._detach_switch_ports

    @detach_switch_ports.setter
    def detach_switch_ports(self, value: list[str]) -> None:
        self._detach_switch_ports = self._list_to_string(value)

    @property
    def dot1q_vlan(self) -> str:
        """
        return the current value of dot1QVlan
        """
        return self._dot1q_vlan

    @dot1q_vlan.setter
    def dot1q_vlan(self, value: str) -> None:
        self._dot1q_vlan = value

    @property
    def extension_values(self) -> str:
        """
        return the current value of extensionValues
        """
        return self._extension_values

    @extension_values.setter
    def extension_values(self, value: str) -> None:
        self._extension_values = value

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
    def freeform_config(self) -> str:
        """
        return the current value of freeformConfig

        freeformConfig is converted from a list to a newline-separated string in the setter.
        """
        return self._freeform_config

    @freeform_config.setter
    def freeform_config(self, value: list[str]) -> None:
        self._freeform_config = self._freeform_config_to_string(value)

    @property
    def instance_values(self) -> str:
        """
        return the current value of instanceValues
        """
        return self._instance_values

    @instance_values.setter
    def instance_values(self, value: str) -> None:
        self._instance_values = value

    @property
    def network_name(self) -> str:
        """
        return the current value of networkName
        """
        return self._network_name

    @network_name.setter
    def network_name(self, value: str) -> None:
        self._network_name = value

    @property
    def peer_switch_name(self) -> str:
        """
        return the current value of peer_switch_name
        """
        return self._peer_switch_name

    @peer_switch_name.setter
    def peer_switch_name(self, value: str) -> None:
        self._peer_switch_name = value

    @property
    def switch_name(self) -> str:
        """
        return the current value of switch_name
        """
        return self._switch_name

    @switch_name.setter
    def switch_name(self, value: str) -> None:
        self._switch_name = value

    @property
    def switch_ports(self) -> str:
        """
        return the current value of switchPorts
        """
        return self._switch_ports

    @switch_ports.setter
    def switch_ports(self, value: list[str]) -> None:
        self._switch_ports = self._list_to_string(value)

    @property
    def tor_ports(self) -> str:
        """
        return the current value of torPorts

        torPorts is converted from a list to a comma-separated string in the setter.
        """
        return self._tor_ports

    @tor_ports.setter
    def tor_ports(self, value: list[str]) -> None:
        self._tor_ports = self._list_to_string(value)

    @property
    def untagged(self) -> bool:
        """
        return the current value of untagged
        """
        return self._untagged

    @untagged.setter
    def untagged(self, value: bool) -> None:
        self._untagged = value

    @property
    def vlan(self) -> str:
        """
        return the current value of vlan
        """
        return self._vlan

    @vlan.setter
    def vlan(self, value: str) -> None:
        self.validations.verify_vlan(value)
        self._vlan = value
