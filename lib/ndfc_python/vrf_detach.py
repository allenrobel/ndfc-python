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
from ndfc_python.common.properties import Properties
from ndfc_python.validations import Validations


class VrfDetach:
    """
    # Summary

    Detach VRFs

    ## Raises

    - ValueError
        - If any required parameter is missing or invalid
        - Unable to populate fabric inventory for fabric {self.fabric_name}
        - Unable to send GET request to the controller
        - Unable to get serial number for switch_name {self.switch_name}
        - Unable to send POST request to the controller
        - vrf_name does not exist in fabric fabric_name

    ## Example VRF detach request

    ### See

    ./examples/vrf_detach.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.fabric_inventory = FabricInventory()

        self.properties = Properties()
        self.rest_send = self.properties.rest_send
        self.results = self.properties.results

        self.validations = Validations()

        self._fabric_name = ""
        self._fabric_inventory_populated = False
        self._switch_name = ""
        self._vrf_name = ""

    def _final_verification(self) -> None:
        """
        # Summary

        final verification of all parameters

        ## Raises

        ValueError
            If any required parameter is missing or invalid
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

        if not self.switch_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "switch_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if not self.vrf_name:
            msg = f"{self.class_name}.{method_name}: "
            msg += "vrf_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if not self._fabric_inventory_populated:
            self.populate_fabric_inventory()

        if self.vrf_name_exists_in_fabric() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"vrfName {self.vrf_name} does not exist "
            msg += f"in fabric {self.fabric_name}. "
            msg += f"Create it first before calling {self.class_name}.commit"
            raise ValueError(msg)

    def populate_fabric_inventory(self) -> None:
        """
        # Summary

        Get switch inventory for a specific fabric.

        ## Raises

        ValueError
            Unable to populate fabric inventory for fabric {self.fabric_name}
        """
        try:
            self.fabric_inventory.fabric_name = self.fabric_name
            self.fabric_inventory.rest_send = self.rest_send
            self.fabric_inventory.results = self.results
            self.fabric_inventory.commit()
        except ValueError as error:
            msg = f"{self.class_name}.populate_fabric_inventory: "
            msg += f"Unable to populate fabric inventory for fabric {self.fabric_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._fabric_inventory_populated = True

    def vrf_name_exists_in_fabric(self):
        """
        # Summary

        Return True if self.vrf exists in self.fabric_name.
        Else, return False

        ## Raises

        ValueError
            Unable to send GET request to the controller
        """
        method_name = inspect.stack()[0][3]
        # TODO: update when this path is added to ansible-dcnm
        path = f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{self.fabric_name}/vrfs"
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
            if item.get("fabric") != self.fabric_name:
                continue
            if item.get("vrfName") != self.vrf_name:
                continue
            return True
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
        try:
            _lan_attach_list_item["serialNumber"] = self.fabric_inventory.switch_name_to_serial_number(self.switch_name)
        except ValueError as error:
            msg = f"{self.class_name}._build_payload: "
            msg += f"Unable to get serial number for switch_name {self.switch_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
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
        self._final_verification()
        self.fabric_inventory.fabric_name = self.fabric_name
        self.fabric_inventory.rest_send = self.rest_send
        self.fabric_inventory.results = self.results
        self.fabric_inventory.commit()

        payload = self._build_payload()

        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/vrfs/attachments"
        verb = "POST"

        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.payload = payload
            self.rest_send.commit()
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
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value: str) -> None:
        self._fabric_name = value

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
    def vrf_name(self) -> str:
        """
        return the current value of vrfName
        """
        return self._vrf_name

    @vrf_name.setter
    def vrf_name(self, value: str) -> None:
        self._vrf_name = value
