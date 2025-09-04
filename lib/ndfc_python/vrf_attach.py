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

import copy
import inspect
import json
import logging

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
from ndfc_python.validations import Validations
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.fabric.fabric_details_v2 import FabricDetailsByName


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
        self.fabric_switches = {}
        self.validations = Validations()

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

    def is_vpc_peer(self, switch_name: str, peer_switch_name: str) -> bool:
        """
        Return True if switch_name and peer_switch_name are vPC peers.
        Return False otherwise.
        """
        if not self.fabric_switches:
            self.populate_fabric_switches()

        serial_number = self._switch_name_to_serial_number(switch_name)
        peer_serial_number = self._switch_name_to_serial_number(peer_switch_name)
        switch = self.fabric_switches.get(switch_name)
        peer_switch = self.fabric_switches.get(peer_switch_name)

        if switch is None:
            msg = f"Switch name {switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        if peer_switch is None:
            msg = f"Switch name {peer_switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)

        if switch.get("isVpcConfigured") is not True:
            return False
        if peer_switch.get("isVpcConfigured") is not True:
            return False

        if switch.get("peerSerialNumber") != peer_serial_number:
            return False
        if peer_switch.get("peerSerialNumber") != serial_number:
            return False

        return True

    def _final_verification(self):
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
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

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

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
        if self.peer_switch_name and self.peer_switch_name == self.switch_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "peer_switch_name must be different from switch_name"
            raise ValueError(msg)
        if self.peer_switch_name:
            if not self.fabric_switches:
                self.populate_fabric_switches()
            if self.peer_switch_name not in self.fabric_switches:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"peer_switch_name {self.peer_switch_name} "
                msg += f"not found in fabric {self.fabric_name}."
                raise ValueError(msg)
            if not self.is_vpc_peer(self.switch_name, self.peer_switch_name):
                msg = f"{self.class_name}.{method_name}: "
                msg += f"switch_name {self.switch_name} and "
                msg += f"peer_switch_name {self.peer_switch_name} "
                msg += "are not vPC peer switches."
                raise ValueError(msg)

    def fabric_exists(self):
        """
        Return True if self.fabric_name exists on the controller.
        Return False otherwise.
        """
        instance = FabricDetailsByName()
        # pylint: disable=no-member
        instance.rest_send = self.rest_send
        instance.results = self.results
        # pylint: enable=no-member
        instance.refresh()
        instance.filter = self.fabric_name
        if instance.filtered_data is None:
            return False
        return True

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

    def populate_fabric_switches(self) -> None:
        """Get switches for a specific fabric.

        Populates self.fabric_switches:
            dict keyed on switch_name, containing switch details.

        Example:

            {
                "VP3": {
                    "switchRoleEnum": "Leaf",
                    "vrf": "management",
                    "fabricTechnology": "VXLANFabric",
                    "deviceType": "Switch_Fabric",
                    "fabricId": 4,
                    "name": null,
                    "domainID": 0,
                    "wwn": null,
                    "membership": null,
                    "ports": 0,
                    "model": "N9K-C9300v",
                    "version": null,
                    "upTime": 0,
                    "ipAddress": "192.168.14.153",
                    "mgmtAddress": null,
                    "vendor": "Cisco",
                    "displayHdrs": null,
                    "displayValues": null,
                    "colDBId": 0,
                    "fid": 0,
                    "isLan": false,
                    "is_smlic_enabled": false,
                    "present": true,
                    "licenseViolation": false,
                    "managable": true,
                    "mds": false,
                    "connUnitStatus": 0,
                    "standbySupState": 0,
                    "activeSupSlot": 0,
                    "unmanagableCause": "",
                    "lastScanTime": 0,
                    "fabricName": "SITE4",
                    "modelType": 0,
                    "logicalName": "VP3",
                    "switchDbID": 30820,
                    "uid": 0,
                    "release": "10.3(8)",
                    "location": null,
                    "contact": null,
                    "upTimeStr": "01:58:36",
                    "upTimeNumber": 0,
                    "network": null,
                    "nonMdsModel": null,
                    "numberOfPorts": 0,
                    "availPorts": 0,
                    "usedPorts": 0,
                    "vsanWwn": null,
                    "vsanWwnName": null,
                    "swWwn": null,
                    "swWwnName": null,
                    "serialNumber": "9EJ4B3H5GJ3",
                    "domain": null,
                    "principal": null,
                    "status": "ok",
                    "index": 0,
                    "licenseDetail": null,
                    "isPmCollect": false,
                    "sanAnalyticsCapable": false,
                    "vdcId": 0,
                    "vdcName": "",
                    "vdcMac": null,
                    "fcoeEnabled": false,
                    "cpuUsage": 0,
                    "memoryUsage": 0,
                    "scope": null,
                    "fex": false,
                    "health": -1,
                    "npvEnabled": false,
                    "linkName": null,
                    "username": null,
                    "primaryIP": "",
                    "primarySwitchDbID": 0,
                    "secondaryIP": "",
                    "secondarySwitchDbID": 0,
                    "isEchSupport": false,
                    "moduleIndexOffset": 9999,
                    "sysDescr": "",
                    "isTrapDelayed": false,
                    "switchRole": "leaf",
                    "mode": "Normal",
                    "hostName": "VP3",
                    "ipDomain": "",
                    "systemMode": "Normal",
                    "waitForSwitchModeChg": false,
                    "sourceVrf": "management",
                    "sourceInterface": "mgmt0",
                    "protoDiscSettings": null,
                    "operMode": null,
                    "modules": null,
                    "fexMap": {},
                    "isVpcConfigured": true,
                    "vpcDomain": 1,
                    "role": "Primary",
                    "peer": "VP4",
                    "peerSerialNumber": "9XUGSGI5J1O",
                    "peerSwitchDbId": 30780,
                    "peerlinkState": "Peer is OK",
                    "keepAliveState": "Peer is alive",
                    "consistencyState": true,
                    "sendIntf": "Eth1/1",
                    "recvIntf": "Lo0",
                    "interfaces": null,
                    "elementType": null,
                    "monitorMode": null,
                    "freezeMode": null,
                    "cfsSyslogStatus": 1,
                    "isNonNexus": false,
                    "swUUIDId": 30670,
                    "swUUID": "DCNM-UUID-30670",
                    "swType": null,
                    "ccStatus": "In-Sync",
                    "operStatus": "Minor",
                    "intentedpeerName": "VP4",
                    "sharedBorder": false,
                    "isSharedBorder": false
                },
                "switch2": {
                    switch_details
                }
            }
        """
        # pylint: disable=no-member
        instance = FabricInventory()
        instance.fabric_name = self.fabric_name
        instance.rest_send = self.rest_send  # type: ignore[attr-defined]
        instance.results = self.results  # type: ignore[attr-defined]
        instance.commit()
        self.fabric_switches = copy.deepcopy(instance.inventory)
        # pylint: enable=no-member

    def _switch_name_to_serial_number(self, switch_name: str) -> str:
        """
        Convert a switch name to a serial number.
        """
        if not self.fabric_switches:
            self.populate_fabric_switches()
        switch = self.fabric_switches.get(switch_name)
        if switch is None:
            msg = f"Switch name {switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        serial_number = switch.get("serialNumber")
        if serial_number is None:
            msg = f"Switch name {switch_name} has no serial number in fabric {self.fabric_name}."
            raise ValueError(msg)
        return serial_number

    def _build_lan_attach_list_item(self, switch_name: str) -> dict:
        """
        Build the lanAttachList item for the payload.
        """
        _lan_attach_list_item = {}
        _lan_attach_list_item["deployment"] = True
        _lan_attach_list_item["extensionValues"] = self.extension_values
        _lan_attach_list_item["fabric"] = self.fabric_name
        _lan_attach_list_item["freeformConfig"] = self.freeform_config
        _lan_attach_list_item["instanceValues"] = self.instance_values
        _lan_attach_list_item["serialNumber"] = self._switch_name_to_serial_number(switch_name)
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
    def extension_values(self) -> str:
        """
        return the current value of extensionValues
        """
        return self.properties.get("extensionValues")

    @extension_values.setter
    def extension_values(self, value: list) -> None:
        vrf_lite_conn_list = []
        for item in value:
            if item.get("IF_NAME") is None or item.get("IF_NAME") == "":
                continue
            vrf_lite_conn_item: dict = item.copy()
            vrf_lite_conn_item["AUTO_VRF_LITE_FLAG"] = str(vrf_lite_conn_item.get("AUTO_VRF_LITE_FLAG", True)).lower()
            vrf_lite_conn_list.append(vrf_lite_conn_item)
        outer = {}
        outer["VRF_LITE_CONN"] = json.dumps({"VRF_LITE_CONN": vrf_lite_conn_list})
        outer["MULTISITE_CONN"] = json.dumps({"MULTISITE_CONN": []})
        self.properties["extensionValues"] = json.dumps(outer)

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
        return self.properties.get("instanceValues")

    @instance_values.setter
    def instance_values(self, value: dict) -> None:
        self.properties["instanceValues"] = json.dumps(value)

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
