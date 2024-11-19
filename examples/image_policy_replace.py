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
from ndfc_python.validators.image_policy_create import ImagePolicyCreateConfigValidator
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.image_policy.image_policies import ImagePolicies
from plugins.module_utils.image_policy.payload import Config2Payload
from plugins.module_utils.image_policy.replace import ImagePolicyReplaceBulk
from pydantic import ValidationError


@Properties.add_rest_send
class Replaced:
    """
    Replace any policies on the controller that are in the config file with
    the configuration given in the config file.  Policies not listed in the
    config file are not modified and are not deleted.
    """

    def __init__(self, params) -> None:
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        method_name = inspect.stack()[0][3]

        self._rest_send = None
        self.have = ImagePolicies()
        self.need: list[dict[Any, Any]] = []
        self._want: dict[Any, Any] = {}

        self.state = "replaced"
        self.check_mode = params.get("check_mode")

        self.replace = ImagePolicyReplaceBulk()

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def get_have(self) -> None:
        """
        Caller: main()

        self.have consists of the current image policies on the controller
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}"
        self.log.debug(msg)

        self.have = ImagePolicies()
        # pylint: disable=no-member
        self.have.results = self.rest_send.results  # type: ignore[attr-defined]
        self.have.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.have.refresh()
        # pylint: enable=no-member

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
        Replace all policies on the controller that are in want
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

        self.rest_send.results.state = self.state  # type: ignore[attr-defined]
        self.rest_send.results.check_mode = self.check_mode  # type: ignore[attr-defined]

        self.get_want()
        self.get_have()

        self.replace.results = self.rest_send.results  # type: ignore[attr-defined]
        self.replace.payloads = self.want.get("config")
        self.replace.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.replace.params = self.rest_send.params  # type: ignore[attr-defined]
        self.replace.commit()

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
    description += "Replace image policies on one or more switches."
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
    Replace any policies on the controller that are in the config file with
    the configuration given in the config file.  Policies not listed in the
    config file are not modified and are not deleted.
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
        validated_config = ImagePolicyCreateConfigValidator(**ndfc_config.contents)
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
    params["state"] = "replaced"
    rest_send = RestSend(params)
    rest_send.send_interval = 3
    rest_send.timeout = 9
    rest_send.sender = ndfc_sender.sender
    rest_send.response_handler = ResponseHandler()
    rest_send.results = Results()

    try:
        task = Replaced(params)
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
        err_msg = "unable to replace image policy configuration(s)"
        log.error(err_msg)
        print(err_msg)
    print(json.dumps(task.rest_send.results.final_result, indent=4, sort_keys=True))  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
