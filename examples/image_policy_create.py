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
from plugins.module_utils.common.merge_dicts_v2 import MergeDicts
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.image_policy.create import ImagePolicyCreateBulk
from plugins.module_utils.image_policy.image_policies import ImagePolicies
from plugins.module_utils.image_policy.payload import Config2Payload
from plugins.module_utils.image_policy.update import ImagePolicyUpdateBulk
from pydantic import ValidationError


@Properties.add_rest_send
class Merged:
    """
    # Summary

    Handle merged state

    # Raises

    -   ``ValueError`` if:
        -   ``params`` is missing ``config`` key.
        -   ``commit()`` is issued before setting mandatory properties
    """

    def __init__(self, params) -> None:
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        method_name = inspect.stack()[0][3]

        msg = f"ENTERED Merged.{method_name}: "
        self.log.debug(msg)

        self._rest_send = None
        self.have = ImagePolicies()
        self.need: list[dict[Any, Any]] = []
        self._want: dict[Any, Any] = {}
        self.state = params.get("state")
        self.check_mode = params.get("check_mode")

        self.create = ImagePolicyCreateBulk()
        self.update = ImagePolicyUpdateBulk()

        # new policies to be created
        self.need_create: list = []
        # existing policies to be updated
        self.need_update: list = []

        msg = f"ENTERED {self.class_name}().{method_name}: "
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

    def get_need(self):
        """
        # Summary

        Build self.need for merged state

        # Description

        -   Populate self.need_create with items from self.want that are
            not in self.have
        -   Populate self.need_update with updated policies.  Policies are
            updated as follows:
                -   If a policy is in both self.want amd self.have, and they
                    contain differences, merge self.want into self.have,
                    with self.want keys taking precedence and append the
                    merged policy to self.need_update.
                -   If a policy is in both self.want and self.have, and they
                    are identical, do not append the policy to self.need_update
                    (i.e. do nothing).
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        for want in self.want.get("config"):
            self.have.policy_name = want.get("policyName")

            # Policy does not exist on the controller so needs to be created.
            if self.have.policy is None:
                self.need_create.append(copy.deepcopy(want))
                continue

            # The policy exists on the controller.  Merge want parameters with
            # the controller's parameters and add the merged parameters to the
            # need_update list if they differ from the want parameters.
            have = copy.deepcopy(self.have.policy)
            merged, needs_update = self._merge_policies(have, want)

            if needs_update is True:
                self.need_update.append(copy.deepcopy(merged))

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
        Commit the merged state requests
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
        self.get_need()
        self.send_need_create()
        self.send_need_update()

    def _prepare_for_merge(self, have: dict, want: dict) -> tuple[dict[Any, Any], dict[Any, Any]]:
        """
        ### Summary
        -   Remove fields in "have" that are not part of a request payload i.e.
            imageName and ref_count.
        -   The controller returns "N9K/N3K" for the platform, but it expects
            "N9K" in the payload.  We change "N9K/N3K" to "N9K" in have so that
            the compare works.
        -   Remove all fields that are not set in both "have" and "want"
        """
        # Remove keys that the controller adds which are not part
        # of a request payload.
        for key in ["imageName", "ref_count", "platformPolicies"]:
            have.pop(key, None)

        # Change "N9K/N3K" to "N9K" in "have" to match the request payload.
        if have.get("platform", None) == "N9K/N3K":
            have["platform"] = "N9K"

        return (have, want)

    def _merge_policies(self, have: dict, want: dict) -> tuple[dict[Any, Any], bool]:
        """
        ### Summary
        Merge the parameters in want with the parameters in have.
        """
        method_name = inspect.stack()[0][3]
        (have, want) = self._prepare_for_merge(have, want)

        # Merge the parameters in want with the parameters in have.
        # The parameters in want take precedence.
        try:
            merge = MergeDicts()
            merge.dict1 = have
            merge.dict2 = want
            merge.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error during MergeDicts(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        merged = copy.deepcopy(merge.dict_merged)

        needs_update = False

        if have != merged:
            needs_update = True

        return (merged, needs_update)

    def send_need_create(self) -> None:
        """
        ### Summary
        Create the policies in self.need_create

        """
        self.create.results = self.rest_send.results  # type: ignore[attr-defined]
        self.create.payloads = self.need_create
        self.create.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.create.params = self.rest_send.params  # type: ignore[attr-defined]
        self.create.commit()

    def send_need_update(self) -> None:
        """
        ### Summary
        Update the policies in self.need_update

        """
        self.update.results = self.rest_send.results  # type: ignore[attr-defined]
        self.update.payloads = self.need_update
        self.update.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.update.params = self.rest_send.params  # type: ignore[attr-defined]
        self.update.commit()

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
    description += "Enable or disable maintenance mode on one or more switches."
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
    params["state"] = "merged"
    rest_send = RestSend(params)
    rest_send.send_interval = 3
    rest_send.timeout = 9
    rest_send.sender = ndfc_sender.sender
    rest_send.response_handler = ResponseHandler()
    rest_send.results = Results()

    try:
        task = Merged(params)
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
        err_msg = "unable to create/update image policies"
        log.error(err_msg)
        print(err_msg)
    print(json.dumps(task.rest_send.results.final_result, indent=4, sort_keys=True))  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
