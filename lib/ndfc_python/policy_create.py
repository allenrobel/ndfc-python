"""
Name: ndfc_policy.py
Description:

Create ND policies
"""

# We use isort for import linting
# pylint: disable=wrong-import-order
import inspect
import json
import logging
import sys

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
from ndfc_python.common.fabric.fabrics_info import FabricsInfo
from ndfc_python.common.properties import Properties
from ndfc_python.policy_info_switch import PolicyInfoSwitch

OUR_VERSION = 106


class PolicyCreate:
    """
    create policies

    Example create operation:

    See `action()` in examples/policy_create.py

    NOTES:

    1. This class assumes that input validation has already been performed.  See
    for example, examples/policy_create.py
    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self._fabric_inventory_populated = False
        self.policies = []
        self._policies_populated = False
        self._fabric_name = ""
        self._nv_pairs = {}
        self.fabric_inventory = FabricInventory()
        self.fabrics_info = FabricsInfo()
        self.properties = Properties()
        self.policy_info_switch = PolicyInfoSwitch()

        self.payload = {}
        self._fabric_inventory_populated = False
        self.rest_send = self.properties.rest_send

    def _build_payload(self) -> None:
        """
        build the payload from the current property values
        """
        method_name = inspect.stack()[0][3]
        self.payload["description"] = self.description
        self.payload["entityName"] = self.entity_name
        self.payload["entityType"] = self.entity_type
        self.payload["ipAddress"] = self.fabric_inventory.switch_name_to_ipv4_address(self.switch_name)
        self.payload["nvPairs"] = self.nv_pairs
        self.payload["priority"] = self.priority
        self.payload["serialNumber"] = self.fabric_inventory.switch_name_to_serial_number(self.switch_name)
        self.payload["source"] = self.source
        self.payload["templateName"] = self.template_name
        self.payload["templateContentType"] = self.template_content_type
        msg = f"{self.class_name}.{method_name}: "
        msg += f"payload: {json.dumps(self.payload, indent=4, sort_keys=True)}"
        self.log.debug(msg)

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

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        if not self._fabric_inventory_populated:
            self.populate_fabric_inventory()

    def commit(self):
        """
        Create a policy
        """
        method_name = inspect.stack()[0][3]

        self._final_verification()
        self._populate_policies_switch()
        self._validate_no_policy_name_conflict()
        self._build_payload()

        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies"
        verb = "POST"

        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.payload = self.payload
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        msg = f"{self.class_name}.{method_name}: "
        msg += f"Sent {self.rest_send.verb} request to {self.rest_send.path}. "
        msg += f"Response: {self.rest_send.response_current}"
        self.log.debug(msg)
        if self.rest_send.result_current.get("success") is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Request unsuccessful. "
            msg += f"{self.rest_send.result_current}. "
            msg += "More detail (if any): "
            msg += f"{self.rest_send.response_current.get('DATA', {}).get('error')}"
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

    def _validate_no_policy_name_conflict(self) -> None:
        """
        # Summary

        Validate that the policy description does not already exist on switch_name.

        Validation is performed using description (which must be unique per switch)

        ## Raises

        - ValueError: if the policy already exists on the switch

        """
        method_name = inspect.stack()[0][3]
        for policy in self.policies:
            if policy.get("description") == self.description:
                policy_id = policy.get("policyId", "N/A")
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Policy ID {policy_id} with description '{self.description}' already exists on switch {self.switch_name} "
                msg += f"in fabric {self.fabric_name}. "
                msg += "Use a unique policy description or delete the existing policy."
                raise ValueError(msg)

    def _populate_policies_switch(self) -> None:
        """
        # Summary

        Populate policies for switch_name.

        ## Raises

        - ValueError: if FabricInventory raises

        """
        method_name = inspect.stack()[0][3]
        if not self._fabric_inventory_populated:
            self.populate_fabric_inventory()

        self.policy_info_switch.rest_send = self.rest_send
        self.policy_info_switch.fabric_name = self.fabric_name
        self.policy_info_switch.switch_name = self.switch_name
        try:
            self.policy_info_switch.commit()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to populate switch policies for switch {self.switch_name} "
            msg += f"in fabric {self.fabric_name}. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        self.policies = self.policy_info_switch.switch_policies
        self._policies_populated = True

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

    @property
    def description(self):
        """
        The description of the policy.  Description is mandatory and MUST be unique.

        Set (setter) or return (getter) the current payload value of description
        """
        return self.payload["description"]

    @description.setter
    def description(self, param):
        self.payload["description"] = param

    @property
    def entity_name(self):
        """
        Set (setter) or return (getter) the current payload value of entity_name
        """
        return self.payload["entityName"]

    @entity_name.setter
    def entity_name(self, param):
        self.payload["entityName"] = param

    @property
    def entity_type(self):
        """
        Set (setter) or return (getter) the current payload value of entity_type
        """
        return self.payload["entityType"]

    @entity_type.setter
    def entity_type(self, param):
        self.payload["entityType"] = param

    @property
    def fabric_name(self) -> str:
        """
        Fabric in which the switch resides

        Set (setter) or return (getter) the current value of fabric

        NOTES:

        1. fabric_name is required to populate the fabric inventory for switch_name to
        ip_address and serial_number conversion, but is not included in the payload sent
        to the controller.
        """
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value: str) -> None:
        self._fabric_name = value

    @property
    def nv_pairs(self) -> dict:
        """
        Set (setter) or return (getter) the current value of nv_pairs
        """
        return self._nv_pairs

    @nv_pairs.setter
    def nv_pairs(self, param: dict) -> None:
        if not isinstance(param, dict):
            msg = f"exiting. expected dict(), got {param} with type "
            msg += f"{type(param).__name__}"
            self.log.error(msg)
            sys.exit(1)
        self._nv_pairs = param

    @property
    def switch_name(self):
        """
        Set (setter) or return (getter) the current payload value of switch_name
        """
        return self.payload["switchName"]

    @switch_name.setter
    def switch_name(self, param):
        self.payload["switchName"] = param

    @property
    def template_content_type(self):
        """
        Set (setter) or return (getter) the current payload value of template_content_type
        """
        return self.payload["templateContentType"]

    @template_content_type.setter
    def template_content_type(self, param):
        self.payload["templateContentType"] = param

    @property
    def template_name(self):
        """
        Set (setter) or return (getter) the current payload value of template_name
        """
        return self.payload["templateName"]

    @template_name.setter
    def template_name(self, param):
        self.payload["templateName"] = param

    @property
    def priority(self):
        """
        Set (setter) or return (getter) the current payload value of priority
        """
        return self.payload["priority"]

    @priority.setter
    def priority(self, param):
        self.payload["priority"] = param

    @property
    def source(self):
        """
        Set (setter) or return (getter) the current payload value of source
        """
        return self.payload["source"]

    @source.setter
    def source(self, param):
        self.payload["source"] = param
