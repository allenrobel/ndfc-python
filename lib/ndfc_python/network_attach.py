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

from ndfc_python.validations import Validations
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.fabric.fabric_details_v2 import FabricDetailsByName


@Properties.add_rest_send
@Properties.add_results
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

        self.validations = Validations()

        self._rest_send = None
        self._results = None

        self._payload_set = set()
        self._payload_set_mandatory = set()
        self._payload_default = {}
        self.properties = {}

        self._init_payload_set()
        self._init_payload_default()
        self._init_payload()

    def _init_payload_set(self):
        """
        set of all payload keys
        """
        self._payload_set.add("deployment")
        self._payload_set.add("detachSwitchPorts")
        self._payload_set.add("dot1QVlan")
        self._payload_set.add("extensionValues")
        self._payload_set.add("fabric")
        self._payload_set.add("freeformConfig")
        self._payload_set.add("instanceValues")
        self._payload_set.add("msoCreated")
        self._payload_set.add("networkName")
        self._payload_set.add("serialNumber")
        self._payload_set.add("switchPorts")
        self._payload_set.add("torPorts")
        self._payload_set.add("untagged")
        self._payload_set.add("vlan")

    def _init_payload_default(self):
        """
        set of all default payload keys

        These are keys for which the caller does not have to provide a value
        unless they specifically want to change them.
        """
        # fmt: off
        self._payload_default["deployment"] = True
        self._payload_default["detachSwitchPorts"] = ""
        self._payload_default["dot1QVlan"] = ""
        self._payload_default["extensionValues"] = ""
        self._payload_default["freeformConfig"] = ""
        self._payload_default["instanceValues"] = ""
        self._payload_default["msoCreated"] = False
        self._payload_default["msoSetVlan"] = False
        self._payload_default["switchPorts"] = ""
        self._payload_default["torPorts"] = ""
        self._payload_default["untagged"] = True
        self._payload_default["vlan"] = ""
        # fmt: on

    def _init_payload(self):
        self.payload = []

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

        if self.network_name_exists_in_fabric() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"networkName {self.network_name} does not exist "
            msg += f"in fabric {self.fabric_name}. "
            msg += f"Create it first before calling {self.class_name}.commit"
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
            if "networkName" not in item:
                continue
            if item["networkName"] == self.network_name:
                return True
        return False

    def _build_payload(self) -> list[dict]:
        """
        Build and return the payload for the API request
        """
        _payload = []
        _payload_item = {}
        _payload_item["networkName"] = self.network_name
        _lan_attach_list_item = {}
        _lan_attach_list_item["deployment"] = self.deployment
        _lan_attach_list_item["detachSwitchPorts"] = self.detach_switch_ports
        _lan_attach_list_item["dot1QVlan"] = self.dot1q_vlan
        _lan_attach_list_item["extensionValues"] = self.extension_values
        _lan_attach_list_item["fabric"] = self.fabric_name
        _lan_attach_list_item["freeformConfig"] = self.freeform_config
        _lan_attach_list_item["instanceValues"] = self.instance_values
        _lan_attach_list_item["msoCreated"] = self.mso_created
        _lan_attach_list_item["msoSetVlan"] = self.mso_set_vlan
        _lan_attach_list_item["networkName"] = self.network_name
        _lan_attach_list_item["serialNumber"] = self.serial_number
        _lan_attach_list_item["switchPorts"] = self.switch_ports
        _lan_attach_list_item["torPorts"] = self.tor_ports
        _lan_attach_list_item["untagged"] = self.untagged
        _lan_attach_list_item["vlan"] = self.vlan

        _lan_attach_list = []
        _lan_attach_list.append(_lan_attach_list_item)
        _payload_item["lanAttachList"] = _lan_attach_list
        _payload.append(_payload_item)
        return _payload

    def commit(self):
        """
        Attach a network to a switch
        """
        method_name = inspect.stack()[0][3]
        payload = self._build_payload()
        self._final_verification()

        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/networks/attachments"
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
    def deployment(self) -> bool:
        """
        return the current value of deployment
        """
        return self.properties.get("deployment")

    @deployment.setter
    def deployment(self, value: bool) -> None:
        self.properties["deployment"] = value

    @property
    def detach_switch_ports(self) -> str:
        """
        return the current value of detachSwitchPorts

        detachSwitchPorts is converted from a list to a comma-separated string in the setter.
        """
        return self.properties.get("detachSwitchPorts")

    @detach_switch_ports.setter
    def detach_switch_ports(self, value: list[str]) -> None:
        self.properties["detachSwitchPorts"] = self._list_to_string(value)

    @property
    def dot1q_vlan(self) -> str:
        """
        return the current value of dot1QVlan
        """
        return self.properties.get("dot1QVlan")

    @dot1q_vlan.setter
    def dot1q_vlan(self, value: str) -> None:
        self.properties["dot1QVlan"] = value

    @property
    def extension_values(self) -> str:
        """
        return the current value of extensionValues
        """
        return self.properties.get("extensionValues")

    @extension_values.setter
    def extension_values(self, value: str) -> None:
        self.properties["extensionValues"] = value

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
    def instance_values(self, value: str) -> None:
        self.properties["instanceValues"] = value

    @property
    def mso_created(self) -> bool:
        """
        return the current value of msoCreated
        """
        return self.properties.get("msoCreated")

    @mso_created.setter
    def mso_created(self, value: bool) -> None:
        self.properties["msoCreated"] = value

    @property
    def mso_set_vlan(self) -> bool:
        """
        return the current value of msoSetVlan
        """
        return self.properties.get("msoSetVlan")

    @mso_set_vlan.setter
    def mso_set_vlan(self, value: bool) -> None:
        self.properties["msoSetVlan"] = value

    @property
    def network_name(self) -> str:
        """
        return the current value of networkName
        """
        return self.properties.get("networkName")

    @network_name.setter
    def network_name(self, value: str) -> None:
        self.properties["networkName"] = value

    @property
    def serial_number(self) -> str:
        """
        return the current value of serialNumber
        """
        return self.properties.get("serialNumber")

    @serial_number.setter
    def serial_number(self, value: str) -> None:
        self.properties["serialNumber"] = value

    @property
    def switch_ports(self) -> str:
        """
        return the current value of switchPorts
        """
        return self.properties.get("switchPorts")

    @switch_ports.setter
    def switch_ports(self, value: list[str]) -> None:
        self.properties["switchPorts"] = self._list_to_string(value)

    @property
    def tor_ports(self) -> str:
        """
        return the current value of torPorts

        torPorts is converted from a list to a comma-separated string in the setter.
        """
        return self.properties.get("torPorts")

    @tor_ports.setter
    def tor_ports(self, value: list[str]) -> None:
        self.properties["torPorts"] = self._list_to_string(value)

    @property
    def untagged(self) -> bool:
        """
        return the current value of untagged
        """
        return self.properties.get("untagged")

    @untagged.setter
    def untagged(self, value: bool) -> None:
        self.properties["untagged"] = value

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
