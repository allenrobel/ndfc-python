"""
Name: ndfc_policy.py
Description:

Create / delete NDFC policies

TODO: Add JSON payload example

For delete policies, three distinct scenarios exist:

1. User sets switch serial_number, entity_type, entity_name

The policies matching these property values will be deleted

2. User sets switch serial_number

All of the policies matching the serial_number will be deleted

3. User sets policy_ids property (a python list)

All the policy IDs in this list will be deleted.
"""

import sys

from ndfc_python.log import log
from ndfc_python.ndfc import NdfcRequestError
from ndfc_python.validations import Validations

OUR_VERSION = 105


class NdfcPolicy:
    """
    create / delete policies

    Example create operation:

        instance = NdfcPolicy(ndfc)
        instance.description = "TelemetryDst_EF policy"
        instance.entity_type = "SWITCH"
        instance.entity_name = "SWITCH"
        instance.ip_address = "10.1.150.99"
        instance.priority = 500
        instance.serial_number = "FDO2443096H"
        instance.source = ""
        instance.switch_name = "cvd-1112-bgw"
        instance.template_name = "TelemetryDst_EF"
        instance.template_content_type = "string"
        instance.nv_pairs = {
            "DSTGRP": "500",
            "IPADDR": "10.1.150.244",
            "PORT": "65535",
            "VRF": "management"
        }
        instance.create()

    Example delete operation using serial_number, entity_type, entity_name:

        instance = NdfcPolicy(ndfc)
        instance.serial_number = "FDO2443096H"
        instance.entity_type = "INTERFACE"
        instance.entity_name = "loopback1"
        instance.delete()

    Example delete operation using serial_number:

        instance = NdfcPolicy(ndfc)
        instance.serial_number = "FDO2443096H"
        instance.delete()

    Example delete operation using policy_ids:

        instance = NdfcPolicy(ndfc)
        instance.policy_ids = ["POLICY-1178150"]
        instance.delete()

    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__

        self.validations = Validations()

        # properties not passed to NDFC
        # order is important for these three
        self._internal_properties = {}
        self._init_default_logger()
        self._init_internal_properties()

        # post/get base headers
        self._headers = {}
        self._headers["Content-Type"] = "application/json"

        self._policy_ids = []

        self.delete_by_serial_entity_name_entity_type = set()

        self._init_payload_set()
        self._init_payload_set_mandatory()
        self._init_payload_default()
        self._init_payload_mapping_dict()
        self._init_payload()

    def _init_default_logger(self):
        """
        This logger will be active if the user hasn't set self.logger
        """
        self.logger = log("ndfc_policy_log")

    def _init_internal_properties(self):
        self._internal_properties["logger"] = self.logger
        self._internal_properties["ndfc"] = None

    def _init_payload_set(self):
        self._payload_set = set()
        self._payload_set.add("description")
        self._payload_set.add("entity_name")
        self._payload_set.add("entity_type")
        self._payload_set.add("ip_address")
        self._payload_set.add("priority")
        self._payload_set.add("serial_number")
        self._payload_set.add("switch_name")
        self._payload_set.add("source")
        self._payload_set.add("template_name")
        self._payload_set.add("template_content_type")

    def _init_payload_set_mandatory(self):
        self._payload_set_mandatory = set()
        self._payload_set_mandatory.add("entity_name")
        self._payload_set_mandatory.add("entity_type")
        self._payload_set_mandatory.add("ip_address")
        self._payload_set_mandatory.add("serial_number")
        self._payload_set_mandatory.add("switch_name")

    def _init_payload_default(self):
        self._payload_default = {}
        self._payload_default["source"] = ""
        self._payload_default["template_content_type"] = "string"

    def _init_payload(self):
        self.payload = {}
        for param in self._payload_set:
            if param in self._payload_default:
                value = self._payload_default[param]
                self.payload[self._payload_mapping_dict[param]] = value
            else:
                self.payload[self._payload_mapping_dict[param]] = None

    def _init_payload_mapping_dict(self):
        """
        see _map_payload_param()
        """
        self._payload_mapping_dict = {}
        self._payload_mapping_dict["description"] = "description"
        self._payload_mapping_dict["entity_name"] = "entityName"
        self._payload_mapping_dict["entity_type"] = "entityType"
        self._payload_mapping_dict["ip_address"] = "ipAddress"
        self._payload_mapping_dict["priority"] = "priority"
        self._payload_mapping_dict["serial_number"] = "serialNumber"
        self._payload_mapping_dict["source"] = "source"
        self._payload_mapping_dict["switch_name"] = "switchName"
        value = "templateContentType"
        self._payload_mapping_dict["template_content_type"] = value
        self._payload_mapping_dict["template_name"] = "templateName"

    def _map_payload_param(self, param):
        """
        Because payload keys are camel case, and pylint does
        not like camel case, we modified the corresponding
        properties to be snake case.  This method maps the
        camel case keys to their corresponding properties. It
        is used in _final_verification to provide the user with
        the correct property to call if there's a missing mandatory
        payload property.
        """
        if param not in self._payload_mapping_dict:
            self.logger.error("WARNING: param {} not in _payload_mapping_dict")
            return param
        return self._payload_mapping_dict[param]

    def _preprocess_request(self):
        """
        1. Set a default value for any properties that the caller
        has not set and that NDFC provides a default for.

        2. Any other fixup that may be required
        """
        # used in delete() as part of determination of delete request type
        self.delete_by_serial_entity_name_entity_type.add(self.serial_number)
        self.delete_by_serial_entity_name_entity_type.add(self.entity_name)
        self.delete_by_serial_entity_name_entity_type.add(self.entity_type)

    def _final_verification(self):
        """
        final verification of all parameters
        """
        for param in self._payload_set_mandatory:
            mapped_param = self._payload_mapping_dict[param]
            if self.payload[mapped_param] == "":
                msg = "exiting. call "
                msg += f"instance.{self._map_payload_param(param)} "
                msg += "before calling instance.create()"
                self.logger.error(msg)
                sys.exit(1)

    def create(self):
        """
        Create a policy
        """
        self._preprocess_request()
        self._final_verification()

        url = f"{self.ndfc.url_base}"
        url += "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/policies"

        headers = self._headers
        headers["Authorization"] = self.ndfc.bearer_token

        self.ndfc.post(url, headers, self.payload)

    def delete(self):
        """
        Delete a policy

        raise ValueError if the caller provided insufficient information to
        generate the request.

        raise NdfcRequestError if NDFC's response was anything other than 200
        """
        self._preprocess_request()

        headers = self._headers
        headers["Authorization"] = self.ndfc.bearer_token

        url = None
        if None not in self.delete_by_serial_entity_name_entity_type:
            url = f"{self.ndfc.url_control_policies_switches}"
            url += f"/{self.serial_number}/"
            url += f"{self.entity_type}/{self.entity_name}"
        elif self.serial_number is not None:
            url = f"{self.ndfc.url_control_policies_switches}"
            url += f"/{self.serial_number}"
        elif len(self.policy_ids) != 0:
            url = f"{self.ndfc.url_base}"
            url += "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control"
            url += "/policies"
            url += f"/policyIds?policyIds={','.join(self.policy_ids)}"
        else:
            msg = (
                "Skipping delete. ",
                "Insufficient information provided to build REST endpoint ",
                "for delete operation. To delete all policies associated ",
                "with a switch serial number, set at least serial_number. ",
                "To delete all policies matching serial number, entity type, ",
                "and entity name, set at least serial_number, entity_name, ",
                "and entity_type. To delete one or more specific policies, ",
                "set policy_ids to a python list of policy IDs e.g. ",
                "[POLICY-1173140, POLICY-1173150]",
            )
            raise ValueError(msg)

        try:
            self.ndfc.delete(url, headers)
        except NdfcRequestError as err:
            msg = f"Failure response from NDFC. Detail: {err}"
            raise NdfcRequestError(msg) from err

    # properties that are not passed to NDFC
    @property
    def logger(self):
        """
        return/set the current logger instance
        """
        return self._internal_properties["logger"]

    @logger.setter
    def logger(self, param):
        self._internal_properties["logger"] = param

    @property
    def ndfc(self):
        """
        return/set the current ndfc instance
        """
        return self._internal_properties["ndfc"]

    @ndfc.setter
    def ndfc(self, param):
        self._internal_properties["ndfc"] = param

    # top_level payload properties

    @property
    def description(self):
        """
        return the current payload value of description
        """
        return self.payload["description"]

    @description.setter
    def description(self, param):
        self.payload["description"] = param

    @property
    def entity_name(self):
        """
        return the current payload value of entity_name
        """
        return self.payload["entityName"]

    @entity_name.setter
    def entity_name(self, param):
        self.payload["entityName"] = param

    @property
    def entity_type(self):
        """
        return the current payload value of entity_type
        """
        return self.payload["entityType"]

    @entity_type.setter
    def entity_type(self, param):
        self.payload["entityType"] = param

    @property
    def ip_address(self):
        """
        return the current payload value of ip_address
        """
        return self.payload["ipAddress"]

    @ip_address.setter
    def ip_address(self, param):
        self.payload["ipAddress"] = param

    @property
    def nv_pairs(self):
        """
        return the current value of policy_ids
        """
        return self.payload["nvPairs"]

    @nv_pairs.setter
    def nv_pairs(self, param):
        if not isinstance(param, dict):
            msg = f"exiting. expected dict(), got {param} with type "
            msg += f"{type(param).__name__}"
            self.logger.error(msg)
            sys.exit(1)
        self.payload["nvPairs"] = param

    @property
    def policy_ids(self):
        """
        return the current value of policy_ids
        """
        return self._policy_ids

    @policy_ids.setter
    def policy_ids(self, param):
        if not isinstance(param, list):
            msg = f"exiting. expected list(), got {param} with type "
            msg += f"{type(param).__name__}"
            self.logger.error(msg)
            sys.exit(1)
        self._policy_ids = param

    @property
    def serial_number(self):
        """
        return the current payload value of serial_number
        """
        return self.payload["serialNumber"]

    @serial_number.setter
    def serial_number(self, param):
        self.payload["serialNumber"] = param

    @property
    def switch_name(self):
        """
        return the current payload value of switch_name
        """
        return self.payload["switchName"]

    @switch_name.setter
    def switch_name(self, param):
        self.payload["switchName"] = param

    @property
    def template_content_type(self):
        """
        return the current payload value of template_content_type
        """
        return self.payload["templateContentType"]

    @template_content_type.setter
    def template_content_type(self, param):
        self.payload["templateContentType"] = param

    @property
    def template_name(self):
        """
        return the current payload value of template_name
        """
        return self.payload["templateName"]

    @template_name.setter
    def template_name(self, param):
        self.payload["templateName"] = param

    @property
    def priority(self):
        """
        return the current payload value of priority
        """
        return self.payload["priority"]

    @priority.setter
    def priority(self, param):
        self.payload["priority"] = param

    @property
    def source(self):
        """
        return the current payload value of source
        """
        return self.payload["source"]

    @source.setter
    def source(self, param):
        self.payload["source"] = param
