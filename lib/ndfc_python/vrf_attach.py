"""
# Name

vrf_attach.py

# Description

Send vrf attach POST requests to the controller

## Caveats

- VRF Lite currently not supported

# Payload Example

```json
[
    {
        "lanAttachList": [
            {
                "deployment": "true",
                "extensionValues": "{\"content\":\"removed\"}",
                "fabric": SITE1,
                "freeformConfig": "",
                "instanceValues": "{\"content\":\"removed\"}",
                "serialNumber": 96KWEIQE2HC,
                "vlan": 2300,
                "vrfName": ndfc-python-vrf1
            }
        ],
        "vrfName": ndfc-python-vrf1
    }
]
```
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import json
import logging

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
from ndfc_python.validations import Validations
from ndfc_python.validators.vrf_attach import ExtensionValues, InstanceValues
from plugins.module_utils.common.properties import Properties


@Properties.add_rest_send
@Properties.add_results
class VrfAttach:
    """
    # Summary

    Attach VRFs

    ## Example VRF attach request

    ### See

    ./examples/vrf_attach.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.api_v1 = "/appcenter/cisco/ndfc/api/v1"
        self.ep_fabrics = f"{self.api_v1}/lan-fabric/rest/top-down/fabrics"
        self.fabric_inventory = FabricInventory()
        self._fabric_inventory_populated = False
        self.fabric_switches = {}
        self.validations = Validations()
        self._extension_values = []
        self._instance_values = []

        self.properties = {}

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

    def _final_verification(self):
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        if not self._fabric_inventory_populated:
            self.populate_fabric_inventory()
        # pylint: disable=no-member
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
        # pylint: enable=no-member

        if self.vrf_name_exists_in_fabric() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"vrfName {self.vrf_name} does not exist "
            msg += f"in fabric {self.fabric_name}. "
            msg += f"Create it first before calling {self.class_name}.commit"
            raise ValueError(msg)
        if not self.switch_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "switch_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)
        if self.switch_name not in self.fabric_inventory.devices:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"switch_name {self.switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        if self.peer_switch_name and self.peer_switch_name == self.switch_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "peer_switch_name must be different from switch_name"
            raise ValueError(msg)
        if self.peer_switch_name:
            # if self.peer_switch_name not in self.fabric_switches:
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

    def vrf_name_exists_in_fabric(self):
        """
        Return True if self.vrf exists in self.fabric_name.
        Else, return False
        """
        method_name = inspect.stack()[0][3]
        # TODO: update when this path is added to ansible-dcnm
        path = f"{self.ep_fabrics}/{self.fabric_name}/vrfs"
        verb = "GET"

        # pylint: disable=no-member
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
            if item.get("fabric") != self.fabric_name:
                continue
            if item.get("vrfName") != self.vrf_name:
                continue
            return True
        # pylint: enable=no-member
        return False

    def populate_fabric_inventory(self) -> None:
        """
        Get switch inventory for a specific fabric.
        """
        # pylint: disable=no-member
        try:
            self.fabric_inventory.fabric_name = self.fabric_name
            self.fabric_inventory.rest_send = self.rest_send  # type: ignore[attr-defined]
            self.fabric_inventory.results = self.results  # type: ignore[attr-defined]
            self.fabric_inventory.commit()
        except ValueError as error:
            msg = f"{self.class_name}.populate_fabric_inventory: "
            msg += f"Unable to populate fabric inventory for fabric {self.fabric_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        # pylint: enable=no-member
        self._fabric_inventory_populated = True

    def build_extension_values(self, value: list[ExtensionValues]) -> str:
        """
        Build the extensionValues property from a list of ExtensionValues objects
        and return it as a JSON string.
        """
        vrf_lite_conn_list = []
        for item in value:
            if isinstance(item, dict):
                item = ExtensionValues.model_validate(item)
            if item.IF_NAME is None or item.IF_NAME == "":
                continue
            vrf_lite_conn_item: dict = item.model_dump()
            vrf_lite_conn_item["AUTO_VRF_LITE_FLAG"] = str(vrf_lite_conn_item.get("AUTO_VRF_LITE_FLAG", True)).lower()
            vrf_lite_conn_list.append(vrf_lite_conn_item)
        outer = {}
        outer["VRF_LITE_CONN"] = json.dumps({"VRF_LITE_CONN": vrf_lite_conn_list})
        outer["MULTISITE_CONN"] = json.dumps({"MULTISITE_CONN": []})
        return json.dumps(outer)

    def _build_lan_attach_list_item(self, switch_name: str) -> dict:
        """
        Build the lanAttachList item for the payload.
        """
        _lan_attach_list_item = {}
        _lan_attach_list_item["deployment"] = True
        _lan_attach_list_item["extensionValues"] = self.build_extension_values(self.extension_values)
        _lan_attach_list_item["fabric"] = self.fabric_name
        _lan_attach_list_item["freeformConfig"] = self.freeform_config
        _lan_attach_list_item["instanceValues"] = json.dumps(self._instance_values.model_dump())
        _lan_attach_list_item["serialNumber"] = self.fabric_inventory.switch_name_to_serial_number(switch_name)
        _lan_attach_list_item["vlan"] = self.vlan
        _lan_attach_list_item["vrfName"] = self.vrf_name
        return _lan_attach_list_item

    def _build_payload(self) -> list[dict]:
        """
        Build and return the payload for the API request
        """
        _payload = []
        _payload_item = {}
        _payload_item["vrfName"] = self.vrf_name
        _lan_attach_list = []
        _lan_attach_list.append(self._build_lan_attach_list_item(self.switch_name))
        if self.peer_switch_name:
            _lan_attach_list.append(self._build_lan_attach_list_item(self.peer_switch_name))

        _payload_item["lanAttachList"] = _lan_attach_list
        _payload.append(_payload_item)
        return _payload

    def commit(self):
        """
        Attach a vrf to a switch
        """
        method_name = inspect.stack()[0][3]
        if not self._fabric_inventory_populated:
            self.populate_fabric_inventory()

        payload = self._build_payload()

        self._final_verification()

        # TODO: Update when we add endpoint to ansible-dcnm
        path = f"{self.ep_fabrics}/{self.fabric_name}/vrfs/attachments?quick-attach=true"
        verb = "POST"

        # pylint: disable=no-member
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
    def extension_values(self) -> list[ExtensionValues | dict]:
        """
        return the current value of extensionValues
        """
        return self._extension_values

    @extension_values.setter
    def extension_values(self, value: list[ExtensionValues | dict]) -> None:
        if not isinstance(value, list):
            msg = "extension_values must be a list of ExtensionValues objects or list of dict"
            raise ValueError(msg)
        for item in value:
            if not isinstance(item, ExtensionValues) and not isinstance(item, dict):
                msg = "extension_values must be a list of ExtensionValues objects or list of dict"
                raise ValueError(msg)
        self._extension_values = value

    @property
    def fabric_name(self) -> str:
        """
        return the current value of fabric
        """
        return self.properties.get("fabric")

    @fabric_name.setter
    def fabric_name(self, value: str) -> None:
        self.properties["fabric"] = value

    @property
    def freeform_config(self) -> str:
        """
        return the current value of freeformConfig

        freeformConfig is converted from a list to a newline-separated string in the setter.
        """
        return self.properties.get("freeformConfig")

    @freeform_config.setter
    def freeform_config(self, value: list[str]) -> None:
        self.properties["freeformConfig"] = self._freeform_config_to_string(value)

    @property
    def instance_values(self) -> str:
        """
        return the current value of instanceValues
        """
        return self._instance_values

    @instance_values.setter
    def instance_values(self, value: InstanceValues | dict) -> None:
        if not isinstance(value, InstanceValues) and not isinstance(value, dict):
            msg = "instance_values must be an InstanceValues object or dict"
            raise ValueError(msg)
        self._instance_values = value

    @property
    def peer_switch_name(self) -> str:
        """
        return the current value of peer_switch_name
        """
        return self.properties.get("peer_switch_name")

    @peer_switch_name.setter
    def peer_switch_name(self, value: str) -> None:
        self.properties["peer_switch_name"] = value

    @property
    def switch_name(self) -> str:
        """
        return the current value of switch_name
        """
        return self.properties.get("switch_name")

    @switch_name.setter
    def switch_name(self, value: str) -> None:
        self.properties["switch_name"] = value

    @property
    def vlan(self) -> str:
        """
        return the current value of vlan
        """
        return self.properties.get("vlan")

    @vlan.setter
    def vlan(self, value: str) -> None:
        self.validations.verify_vlan(value)
        self.properties["vlan"] = value

    @property
    def vrf_name(self) -> str:
        """
        return the current value of vrfName
        """
        return self.properties.get("vrfName")

    @vrf_name.setter
    def vrf_name(self, value: str) -> None:
        self.properties["vrfName"] = value
