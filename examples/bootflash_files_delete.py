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
from ndfc_python.validators.bootflash_files_info import BootflashFilesInfoConfigValidator
from plugins.module_utils.bootflash.bootflash_files import BootflashFiles
from plugins.module_utils.bootflash.bootflash_info import BootflashInfo
from plugins.module_utils.bootflash.convert_target_to_params import ConvertTargetToParams
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.common.switch_details import SwitchDetails
from pydantic import ValidationError


@Properties.add_rest_send
class Common:
    """
    Common methods for all states
    """

    def __init__(self, params) -> None:
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]

        self.log = logging.getLogger(f"dcnm.{self.class_name}")

        # Initialize the Results() object temporarily here
        # in case we hit any errors below.  We will reinitialize
        # below after we are sure we have valid params.  This is
        # to avoid Results() being null in main() if we hit an
        # error here.
        self.results = Results()
        self.results.state = "deleted"
        self.results.check_mode = False

        self.params = params

        def raise_error(msg):
            raise ValueError(f"{self.class_name}.{method_name}: {msg}")

        self.check_mode = self.params.get("check_mode", None)
        if self.check_mode is None:
            msg = "params is missing mandatory key: check_mode."
            raise_error(msg)

        if self.check_mode not in [True, False]:
            msg = "check_mode must be True or False. "
            msg += f"Got {self.check_mode}."
            raise_error(msg)

        self._valid_states = ["deleted", "query"]

        self.state = self.params.get("state", None)
        if self.state is None:
            msg = "params is missing mandatory key: state."
            raise_error(msg)
        if self.state not in self._valid_states:
            msg = f"Invalid state: {self.state}. "
            msg += f"Expected one of: {','.join(self._valid_states)}."
            raise_error(msg)

        self.config = self.params.get("config", {}).get("config", None)
        if not isinstance(self.config, dict):
            msg = "Expected dict for config. "
            msg += f"Got {type(self.config).__name__}."
            raise_error(msg)

        self.targets = self.config.get("targets", None)
        if not isinstance(self.targets, list):
            self.targets = []

        if len(self.targets) > 0:
            for item in self.targets:
                if not isinstance(item, dict):
                    msg = "Expected list of dict for params.config.targets. "
                    msg += f"Got list element of type {type(item).__name__}."
                    raise_error(msg)

        self.switches = self.config.get("switches", None)
        if not isinstance(self.switches, list):
            msg = "Expected list of dict for params.config.switches. "
            msg += f"Got {type(self.switches).__name__}."
            raise_error(msg)

        for item in self.switches:
            if not isinstance(item, dict):
                msg = "Expected list of dict for params.config.switches. "
                msg += f"Got list element of type {type(item).__name__}."
                raise_error(msg)

        self._rest_send = None

        self.bootflash_info = BootflashInfo()
        self.convert_target_to_params = ConvertTargetToParams()
        self.results = Results()
        self.results.state = self.state
        self.results.check_mode = self.check_mode
        self.want: list[Any] = []

        msg = f"ENTERED Common().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def get_want(self) -> None:
        """
        ### Summary
        1.  Validate the playbook configs
        2.  Convert the validated configs to the structure required by the
            the Delete() and Query() classes.
        3.  Update self.want with this list of payloads

        If a switch in the switches list does not have a targets key, add the
        targets key with the value of the global targets list from the
        playbook.  Else, use the switch's targets info (i.e. the switch's
        targets info overrides the global targets info).

        ### Raises
        -   ValueError if:
            -   ``ip_address`` is missing from a switch dict.
            -   ``filepath`` is missing from a target dict.
        -   TypeError if:
            -   The value of ``targets`` is not a list of dictionaries.

        ### ``want`` Structure
        -   A list of dictionaries.  Each dictionary contains the following keys:
            -   ip_address: The ip address of the switch.
            -   targets: A list of dictionaries.  Each dictionary contains the
                following keys:
                -   filepath: The path to the file to be deleted or queried.
                -   supervisor: The supervisor containing the filepath.

        ### Example ``want`` Structure
        ```json
        [
            {
                "ip_address": "192.168.1.1",
                "targets": [
                    {
                        "filepath": "bootflash:/foo.txt",
                        "supervisor": "active"
                    },
                    {
                        "filepath": "bar",
                        "supervisor": "standby"
                    }
                ]
            }
        ]
        ```

        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}"
        self.log.debug(msg)

        def raise_value_error(msg):
            raise ValueError(f"{self.class_name}.{method_name}: {msg}")

        def raise_type_error(msg):
            raise TypeError(f"{self.class_name}.{method_name}: {msg}")

        for switch in self.switches:
            if switch.get("ip_address", None) is None:
                msg = "Expected ip_address in switch dict. "
                msg += f"Got {switch}."
                raise_value_error(msg)

            if switch.get("targets", None) is None:
                switch["targets"] = self.targets
            if not isinstance(switch["targets"], list):
                msg = "Expected list of dictionaries for switch['targets']. "
                msg += f"Got {type(switch['targets']).__name__}."
                raise_type_error(msg)

            for target in switch["targets"]:
                if target.get("filepath", None) is None:
                    msg = "Expected filepath in target dict. "
                    msg += f"Got {target}."
                    raise_value_error(msg)
                if target.get("supervisor", None) is None:
                    msg = "Expected supervisor in target dict. "
                    msg += f"Got {target}."
                    raise_value_error(msg)
            self.want.append(copy.deepcopy(switch))


class Deleted(Common):
    """
    ### Summary
    Handle deleted state

    ### Raises
    -   ValueError if:
        -   ``Common.__init__()`` raises TypeError or ValueError.
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]
        try:
            super().__init__(params)
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error during super().__init__(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        self.bootflash_files = BootflashFiles()
        self.files_to_delete = {}

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def populate_files_to_delete(self, switch) -> None:
        """
        ### Summary
        Populate the ``files_to_delete`` dictionary with files
        the user intends to delete.

        ### Raises
        -   ``ValueError`` if:
            -    ``supervisor`` is not one of:
                    -   active
                    -   standby

        ### ``files_to_delete`` Structure
        files_to_delete is a dictionary containing
        -   key: switch ip address.
        -   value: a list of dictionaries containing the files to delete.

        ### ``files_to_delete`` Example
        ```json
        {
            "10.1.1.2": [
                {
                    "date": "2024-08-05 19:23:24",
                    "device_name": "cvd-1211-spine",
                    "filepath": "bootflash:/foo.txt",
                    "ip_address": "10.1.1.2",
                    "serial_number": "FOX12345ABC",
                    "size": "2",
                    "supervisor": "active"
                }
            ]
        }
        ```
        """
        method_name = inspect.stack()[0][3]
        self.bootflash_info.filter_switch = switch["ip_address"]
        if switch["ip_address"] not in self.files_to_delete:
            self.files_to_delete[switch["ip_address"]] = []

        for target in switch["targets"]:
            self.bootflash_info.filter_filepath = target.get("filepath")
            try:
                self.bootflash_info.filter_supervisor = target.get("supervisor")
            except ValueError as error:
                msg = f"{self.class_name}.{method_name}: "
                msg += "Error assigning BootflashInfo.filter_supervisor. "
                msg += f"Error detail: {error}"
                raise ValueError(msg) from error
            self.files_to_delete[switch["ip_address"]].extend(self.bootflash_info.matches)

    def update_bootflash_files(self, ip_address, target) -> None:
        """
        ### Summary
        Call ``BootflashFiles().add_file()`` to add the file associated with
        ``ip_address`` and ``target`` to the list of files to be deleted.

        ### Raises
        -    ``TypeError`` if:
                -   ``target`` is not a dictionary.
        -    ``ValueError`` if:
                -   ``BootflashFiles().add_file`` raises ``ValueError``.
        """
        method_name = inspect.stack()[0][3]

        try:
            self.convert_target_to_params.target = target
            self.convert_target_to_params.commit()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error converting target to params. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        try:
            self.bootflash_files.filename = self.convert_target_to_params.filename
            self.bootflash_files.filepath = self.convert_target_to_params.filepath
            self.bootflash_files.ip_address = ip_address
            self.bootflash_files.partition = self.convert_target_to_params.partition
            self.bootflash_files.supervisor = self.convert_target_to_params.supervisor
            # we want to use the target as the diff, rather than the
            # payload, because it contains better information than
            # the payload. See BootflashFiles() class docstring and
            # BootflashFiles().target property docstring.
            self.bootflash_files.target = target
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error assigning BootflashFiles properties. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        try:
            self.bootflash_files.add_file()
        except ValueError as error:
            msg = f"{self.class_name}.{inspect.stack()[0][3]}: "
            msg += "Error adding file to bootflash_files. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

    def commit(self) -> None:
        """
        ### Summary
        Delete the specified files if they exist.

        ### Raises
        None.  While this method does not directly raise exceptions, it
        calls other methods that may raise the following exceptions:

        -   ControllerResponseError
        -   TypeError
        -   ValueError
        """
        # Populate self.switches
        self.get_want()

        # Prepare BootflashInfo()
        self.bootflash_info.results = Results()
        # pylint: disable=no-member
        self.bootflash_info.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.bootflash_info.switch_details = SwitchDetails()

        # Retrieve bootflash contents for the user's switches.
        switch_list = []
        for switch in self.switches:
            switch_list.append(switch["ip_address"])
        self.bootflash_info.switches = switch_list
        self.bootflash_info.refresh()

        # Prepare BootflashFiles()
        self.results.state = self.state
        self.results.check_mode = self.check_mode
        self.bootflash_files.results = self.results
        self.bootflash_files.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.bootflash_files.switch_details = SwitchDetails()
        self.bootflash_files.switch_details.results = Results()

        # Update BootflashFiles() with the files to delete
        self.files_to_delete = {}
        for switch in self.switches:
            self.populate_files_to_delete(switch)
        for ip_address, targets in self.files_to_delete.items():
            for target in targets:
                self.update_bootflash_files(ip_address, target)

        # Delete the files
        self.bootflash_files.commit()


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    description = "DESCRIPTION: "
    description += "Query bootflash files on one or more switches."
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
        validated_config = BootflashFilesInfoConfigValidator(**ndfc_config.contents)
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
    params["config"] = json.loads(validated_config.model_dump_json())

    rest_send = RestSend(params)
    rest_send.send_interval = 3
    rest_send.timeout = 9
    rest_send.sender = ndfc_sender.sender
    rest_send.response_handler = ResponseHandler()
    rest_send.results = Results()

    try:
        task = Deleted(params)
        # pylint: disable=attribute-defined-outside-init
        task.rest_send = rest_send  # type: ignore[attr-defined]
        task.commit()
    except ValueError as error:
        err_msg = f"Exiting.  Error detail: {error}"
        log.error(err_msg)
        print(err_msg)
        sys.exit(1)

    task.results.build_final_result()  # type: ignore[attr-defined]
    # pylint: disable=unsupported-membership-test
    if True in task.results.failed:  # type: ignore[attr-defined]
        err_msg = "unable to delete bootflash files"
        log.error(err_msg)
        print(err_msg)
    print(json.dumps(task.results.final_result, indent=4, sort_keys=True))  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
