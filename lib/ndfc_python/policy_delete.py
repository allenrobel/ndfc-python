"""
Name: policy_delete.py
Description:

Delete switch policies
"""

# We use isort for import linting
# pylint: disable=wrong-import-order
import inspect
import logging

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
from ndfc_python.common.fabric.fabrics_info import FabricsInfo
from ndfc_python.common.properties import Properties
from ndfc_python.policy_info_switch import PolicyInfoSwitch

OUR_VERSION = 100


class PolicyDeleteEndpoint:
    """
    PolicyDeleteEndpoint class to build the endpoint for the PolicyDelete API request

    /appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies/policyIds?policyIds=POLICY-159920
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.apiv1 = "/appcenter/cisco/ndfc/api/v1"
        self._path = f"{self.apiv1}/lan-fabric/rest/control/policies/policyIds?policyIds="
        self.policy_ids = []
        self._verb = "DELETE"
        self._committed = False

    def _final_verification(self) -> None:
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        if not self.policy_ids:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.policy_ids must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

    def commit(self) -> None:
        """
        Build the endpoint path for the API request
        """
        self._final_verification()

        ids = ",".join(self.policy_ids)
        self._path = f"{self._path}{ids}"
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
    def policy_ids(self) -> list:
        """
        Set (setter) or return (getter) the current value of policy_ids

        policy_ids is a list of policy IDs to delete
        """
        return self._policy_ids

    @policy_ids.setter
    def policy_ids(self, value: list) -> None:
        method_name = inspect.stack()[0][3]
        if not isinstance(value, list):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"exiting. expected type {type(value).__name__}, "
            msg += f"with value {value}."
            raise ValueError(msg)
        self._policy_ids = value


class PolicyDelete:
    """
    delete policies

    Example delete operation:

    See `action()` in examples/policy_delete.py

    NOTES:

    1. This class assumes that input validation has already been performed.  See
    for example, examples/policy_delete.py
    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.fabric_inventory = FabricInventory()
        self.fabrics_info = FabricsInfo()
        self.policy_delete_endpoint = PolicyDeleteEndpoint()
        self.policy_info_switch = PolicyInfoSwitch()
        self.properties = Properties()

        self.payload = {}
        self.policies = []
        self.policy_ids = []
        self.rest_send = self.properties.rest_send

        self._description = ""
        self._fabric_inventory_populated = False
        self._fabric_name = ""
        self._policies_populated = False
        self._switch_name = ""

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

        if not self.description:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.description must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        if not self._fabric_inventory_populated:
            self.populate_fabric_inventory()

        if self.switch_exists_in_fabric() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"switch_name {self.switch_name} "
            msg += "does not exist in the fabric."
            raise ValueError(msg)

    def commit(self):
        """
        Create a policy
        """
        method_name = inspect.stack()[0][3]

        self._final_verification()
        self._populate_policies_switch()

        self._set_policy_ids()
        self.policy_delete_endpoint.policy_ids = self.policy_ids
        self.policy_delete_endpoint.commit()

        try:
            self.rest_send.path = self.policy_delete_endpoint.path
            self.rest_send.verb = self.policy_delete_endpoint.verb
            self.rest_send.payload = None
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

    def _set_policy_ids(self) -> None:
        method_name = inspect.stack()[0][3]
        if not self._policies_populated:
            self._populate_policies_switch()

        self.policy_ids = [policy.get("policyId") for policy in self.policies if policy.get("description") == self.description]

        if len(self.policy_ids) == 0:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name}, switch_name {self.switch_name}: "
            msg += f"No policies found with description '{self.description}'"
            raise ValueError(msg)

        if len(self.policy_ids) > 1:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Expected to find exactly one policy with description '{self.description}' on switch {self.switch_name} "
            msg += f"in fabric {self.fabric_name}. "
            msg += f"Found {len(self.policy_ids)} policies with that description. "
            msg += "Cannot proceed with delete operation. "
            msg += "Manually delete the duplicate policies and try again. "
            msg += f"policy_ids: {self.policy_ids},"
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

    def switch_exists_in_fabric(self) -> bool:
        """
        Return True if self.switch_name exists in the fabric.
        Return False otherwise.
        """
        if self.switch_name not in self.fabric_inventory.devices:
            return False
        return True

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

        self.policies = self.policy_info_switch.policies
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
        return self._description

    @description.setter
    def description(self, param):
        self._description = param

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
    def switch_name(self):
        """
        Set (setter) or return (getter) the current payload value of switch_name
        """
        return self._switch_name

    @switch_name.setter
    def switch_name(self, param):
        self._switch_name = param
