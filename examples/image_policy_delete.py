#!/usr/bin/env python
#
# Copyright (c) 2024 Cisco and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=wrong-import-position
from __future__ import absolute_import, division, print_function

__metaclass__ = type
__author__ = "Allen Robel"

import argparse
import copy
import inspect
import json
import logging
import sys
from typing import Any

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.parsers.parser_nxos_password import parser_nxos_password
from ndfc_python.parsers.parser_nxos_username import parser_nxos_username
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.image_policy_delete import ImagePolicyDeleteConfigValidator
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.image_policy.delete import ImagePolicyDelete
from plugins.module_utils.image_policy.payload import Config2Payload
from pydantic import ValidationError


@Properties.add_rest_send
class Deleted:
    """
    Handle deleted state
    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        method_name = inspect.stack()[0][3]

        self.state = "deleted"
        self.check_mode = False

        self.delete = ImagePolicyDelete()

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def get_want(self) -> None:
        """
        # Summary

        Modify the configurations in self.want["config"] by converting them
        to payloads to more easily compare them to self.have (the current image
        policies on the controller).

        # Raises

        `ValueError` if:
            - `Config2Payload` raises `ValueError`
        """
        method_name = inspect.stack()[0][3]

        new_want: dict[Any, Any] = {}
        new_want["config"] = []
        for config in self.want.get("config", []):
            payload = Config2Payload()
            payload.config = config
            payload.params = self.rest_send.params  # type: ignore[attr-defined]
            try:
                payload.commit()
            except ValueError as error:
                msg = f"{self.class_name}.{method_name}: "
                msg += "Error while converting config to payload. "
                msg += f"Error detail: {error}"
                self.log.error(msg)
                print(msg)
            new_want["config"].append(payload.payload)
        self.want = copy.deepcopy(new_want)

    def commit(self) -> None:
        """
        If config is present, delete all policies in self.want that exist on the controller
        If config is not present, delete all policies on the controller
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        if self.rest_send is None:  # type: ignore[attr-defined]
            msg = f"{self.class_name}.{method_name}: "
            msg += f"rest_send must be set before calling {method_name}."
            raise ValueError(msg)

        self.rest_send.params["state"] = self.state  # type: ignore[attr-defined]
        self.rest_send.results.state = self.state  # type: ignore[attr-defined]
        self.rest_send.results.check_mode = self.check_mode  # type: ignore[attr-defined]

        self.rest_send.results.state = self.state  # type: ignore[attr-defined]
        self.rest_send.results.check_mode = self.check_mode  # type: ignore[attr-defined]
        self.delete.policy_names = self.get_policies_to_delete()
        self.delete.results = self.rest_send.results  # type: ignore[attr-defined]
        self.delete.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.delete.params = self.rest_send.params  # type: ignore[attr-defined]
        self.delete.commit()

    def get_policies_to_delete(self) -> list[str]:
        """
        Return a list of policy names to delete

        -   In config is present, return list of image policy names
            in self.want.
        -   If want["config"] is not present, return ["delete_all_image_policies"],
            which ``ImagePolicyDelete()`` interprets as "delete all image
            policies on the controller".
        """
        if self.want.get("config") is None:
            return ["delete_all_image_policies"]
        self.get_want()
        policy_names_to_delete = []
        for want in self.want.get("config", {}):
            policy_names_to_delete.append(want["policyName"])
        return policy_names_to_delete

    @property
    def want(self) -> dict:
        """
        ### Summary
        Return the playbook configuration.

        ### Returns
        -   list: The playbook configuration.
        """
        return self._want

    @want.setter
    def want(self, value: dict):
        """
        ### Summary
        Set the playbook configuration.

        ### Parameters
        -   value: The playbook configuration.
        """
        self._want = value


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    description = "DESCRIPTION: "
    description += "Delete image policies on one or more switches."
    parser = argparse.ArgumentParser(
        parents=[
            parser_ansible_vault,
            parser_config,
            parser_loglevel,
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
            parser_nxos_password,
            parser_nxos_username,
        ],
        description=description,
    )
    return parser.parse_args()


def main():
    """
    main entry point for module execution
    """
    args = setup_parser()
    NdfcPythonLogger()
    log = logging.getLogger("ndfc_python.main")
    log.setLevel = args.loglevel

    try:
        ndfc_config = ReadConfig()
        ndfc_config.filename = args.config
        ndfc_config.commit()
    except ValueError as error:
        err_msg = f"Exiting: Error detail: {error}"
        log.error(err_msg)
        print(err_msg)
        sys.exit(1)

    try:
        validated_config = ImagePolicyDeleteConfigValidator(**ndfc_config.contents)
    except ValidationError as error:
        err_msg = f"{error}"
        log.error(err_msg)
        print(err_msg)
        sys.exit(1)

    try:
        ndfc_sender = NdfcPythonSender()
        ndfc_sender.args = args
        ndfc_sender.commit()
    except ValueError as error:
        err_msg = f"Exiting.  Error detail: {error}"
        log.error(err_msg)
        print(err_msg)
        sys.exit(1)

    params = {}
    params["check_mode"] = False
    params["state"] = "deleted"
    rest_send = RestSend(params)
    rest_send.send_interval = 3
    rest_send.timeout = 9
    rest_send.sender = ndfc_sender.sender
    rest_send.response_handler = ResponseHandler()
    rest_send.results = Results()

    try:
        task = Deleted()
        # pylint: disable=attribute-defined-outside-init
        task.rest_send = rest_send  # type: ignore[attr-defined]
        task.want = json.loads(validated_config.model_dump_json())
        task.commit()
    except ValueError as error:
        err_msg = f"Exiting.  Error detail: {error}"
        log.error(err_msg)
        print(err_msg)
        sys.exit(1)

    task.rest_send.results.build_final_result()  # type: ignore[attr-defined]
    # pylint: disable=unsupported-membership-test
    if True in task.rest_send.results.failed:  # type: ignore[attr-defined]
        err_msg = "unable to delete image policies"
        log.error(err_msg)
        print(err_msg)
    print(json.dumps(task.rest_send.results.final_result, indent=4, sort_keys=True))  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
