"""
# Name

vrf_detach.py

# Description

Send vrf detach POST requests to the controller

## Caveats

- VRF Lite currently not supported

# Payload Example

```json
[
    {
        "lanAttachList": [
            {
                "deployment": "false",
                "fabric": SITE1,
                "serialNumber": 96KWEIQE2HC,
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
import logging

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
from ndfc_python.validations import Validations
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.fabric.fabric_details_v2 import FabricDetailsByName


@Properties.add_rest_send
@Properties.add_results
class VrfDetach:
    """
    # Summary

    Detach VRFs

    ## Example VRF detach request

    ### See

    ./examples/vrf_detach.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.fabric_inventory = FabricInventory()
        self.validations = Validations()

        self.properties = {}

    def _final_verification(self) -> None:
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        # pylint: disable=no-member
        if self.rest_send is None:  # type: ignore[attr-defined]
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.rest_send must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)
        if self.results is None:  # type: ignore[attr-defined]
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
        path = f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{self.fabric_name}/vrfs"
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

    def _build_payload(self) -> list[dict]:
        """
        Build and return the payload for the API request
        """
        _payload = []
        _payload_item = {}
        _payload_item["vrfName"] = self.vrf_name
        _lan_attach_list_item = {}
        _lan_attach_list_item["deployment"] = False
        _lan_attach_list_item["fabric"] = self.fabric_name
        _lan_attach_list_item["serialNumber"] = self.fabric_inventory.switch_name_to_serial_number(self.switch_name)
        _lan_attach_list_item["vrfName"] = self.vrf_name

        _lan_attach_list = []
        _lan_attach_list.append(_lan_attach_list_item)
        _payload_item["lanAttachList"] = _lan_attach_list
        _payload.append(_payload_item)
        return _payload

    def commit(self) -> None:
        """
        Detach a vrf from a switch
        """
        method_name = inspect.stack()[0][3]
        # pylint: disable=no-member
        self._final_verification()
        self.fabric_inventory.fabric_name = self.fabric_name
        self.fabric_inventory.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.fabric_inventory.results = self.results  # type: ignore[attr-defined]
        self.fabric_inventory.commit()

        payload = self._build_payload()

        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/vrfs/attachments"
        verb = "POST"

        try:
            self.rest_send.path = path  # type: ignore[attr-defined]
            self.rest_send.verb = verb  # type: ignore[attr-defined]
            self.rest_send.payload = payload  # type: ignore[attr-defined]
            self.rest_send.commit()  # type: ignore[attr-defined]
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

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
    def switch_name(self) -> str:
        """
        return the current value of switch_name
        """
        return self.properties.get("switch_name")

    @switch_name.setter
    def switch_name(self, value: str) -> None:
        self.properties["switch_name"] = value

    @property
    def vrf_name(self) -> str:
        """
        return the current value of vrfName
        """
        return self.properties.get("vrfName")

    @vrf_name.setter
    def vrf_name(self, value: str) -> None:
        self.properties["vrfName"] = value
