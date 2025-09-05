"""
# Name

rm_switch_resource_usage.py

## Description

Send GET request for switch resource usage

## Payload Example

Payload is not required for GET requests.

##
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
from ndfc_python.validations import Validations
from ndfc_python.validators.rm_switch_resource_usage import ResourcePool
from plugins.module_utils.common.properties import Properties


class Endpoint:
    """Generate endpoint for RmSwitchResourceUsage"""

    def __init__(self):
        self._serial_number = None
        self._path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/resource-manager/switchView"
        self._verb = "GET"

    @property
    def serial_number(self) -> str:
        """Set or retrieve the switch serial number."""
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value: str) -> None:
        self._serial_number = value

    @property
    def path(self) -> str:
        """Return the endpoint path."""
        if self._serial_number:
            return f"{self._path}/{self._serial_number}"
        raise ValueError("serial_number must be set before accessing path")

    @property
    def verb(self) -> str:
        """Return the HTTP verb for the request."""
        return self._verb


@Properties.add_rest_send
@Properties.add_results
class RmSwitchResourceUsage:
    """
    # Summary

    Get switch resource usage

    ## Example switch resource usage request

    ### See

    ./examples/rm_switch_resource_usage.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.fabric_inventory = FabricInventory()
        self.validations = Validations()
        self.endpoint = Endpoint()

        self._fabric_name = None
        self._inventory_populated = False
        self._rest_send = None
        self._results = None
        self._switch_name = None

        self.properties = {}

    def _validate_rest_send_requirements(self):
        method_name = inspect.stack()[0][3]
        # pylint: disable=no-member
        if self.rest_send is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.rest_send must be set before calling "
            msg += f"{self.class_name}.commit or accessing {self.class_name}.resource_usage"
            raise ValueError(msg)
        if self.results is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.results must be set before calling "
            msg += f"{self.class_name}.commit or accessing {self.class_name}.resource_usage"
            raise ValueError(msg)

    def _populate_fabric_inventory(self):
        """
        populate fabric inventory
        """
        method_name = inspect.stack()[0][3]
        # pylint: disable=no-member
        self._validate_rest_send_requirements()

        if self.fabric_name in (None, ""):
            msg = f"{self.class_name}.{method_name}: "
            msg += "fabric_name must be set before calling commit or accessing resource_usage."
            raise ValueError(msg)

        self.fabric_inventory.fabric_name = self.fabric_name
        self.fabric_inventory.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.fabric_inventory.results = self.results  # type: ignore[attr-defined]
        self.fabric_inventory.commit()
        self._inventory_populated = True
        # pylint: enable=no-member

    def _final_verification(self):
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        self._validate_rest_send_requirements()

        if self.switch_name in (None, ""):
            msg = f"{self.class_name}.{method_name}: "
            msg += "switch_name must be set before calling commit."
            raise ValueError(msg)

        if self.switch_name not in self.fabric_inventory.devices:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"switch_name {self.switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)

    def commit(self):
        """
        Retrieve switch resource usage by sending a GET request to the controller.
        """
        method_name = inspect.stack()[0][3]

        if not self._inventory_populated:
            self._populate_fabric_inventory()
        self._final_verification()
        # pylint: disable=no-member

        self.serial_number = self.fabric_inventory.switch_name_to_serial_number(self.switch_name)
        if self.serial_number is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"switch_name {self.switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        ep = Endpoint()
        ep.serial_number = self.serial_number

        try:
            self.rest_send.path = ep.path
            self.rest_send.verb = ep.verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

    @property
    def filter(self) -> str:
        """
        An optional filter to apply to the output results

        ## Valid values

        - ALL
        - DISCOVERED_VLAN
        - SERVICE_NETWORK_VLAN
        - TOP_DOWN_VRF_VLAN
        - TOP_DOWN_NETWORK_VLAN
        - VPC_PEER_LINK_VLAN
        """
        return self.properties.get("filter")

    @filter.setter
    def filter(self, value: str) -> None:
        """Optional.  If present, filter resource usage by pool name."""
        if value not in [item.value for item in ResourcePool]:
            msg = f"{self.class_name}.filter: Invalid filter value: {value}. "
            msg += "Valid values are: "
            msg += ", ".join([item.value for item in ResourcePool])
            raise ValueError(msg)
        self.properties["filter"] = value

    @property
    def resource_usage(self) -> list:
        """Return a list of resource usage information."""
        self._validate_rest_send_requirements()
        if not self._inventory_populated:
            self._populate_fabric_inventory()
        # pylint: disable=no-member
        data: list = self.rest_send.response_current.get("DATA")  # type: ignore[attr-defined]
        # pylint: enable=no-member
        if self.filter == ResourcePool.ALL.value or self.filter is None:
            return data

        # Example data structure:
        # [
        #     {
        #         "id": 96,
        #         "resourcePool": {
        #             "id": 0,
        #             "poolName": "TOP_DOWN_NETWORK_VLAN",
        #             "fabricName": null,
        #             "vrfName": null,
        #             "poolType": "ID_POOL",
        #             "dynamicSubnetRange": null,
        #             "targetSubnet": 0,
        #             "overlapAllowed": false,
        #             "hierarchicalKey": null
        #         },
        #         "entityType": "Device",
        #         "entityName": "v0n0",
        #         "allocatedIp": "2301",
        #         "allocatedOn": 1755817858702,
        #         "allocatedFlag": true,
        #         "allocatedScopeValue": "9OW9132EH2M",
        #         "ipAddress": "192.168.12.152",
        #         "switchName": "LE2",
        #         "hierarchicalKey": "0"
        #     }
        # ]
        filtered_data = []
        for item in data:
            if item.get("resourcePool", {}).get("poolName") == self.filter:
                filtered_data.append(item)
        return filtered_data

    @property
    def fabric_name(self):
        """
        return the current payload value of fabric
        """
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value):
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
    def serial_number(self) -> str:
        """
        return the current value of serialNumber
        """
        return self.properties.get("serialNumber")

    @serial_number.setter
    def serial_number(self, value: str) -> None:
        self.properties["serialNumber"] = value
