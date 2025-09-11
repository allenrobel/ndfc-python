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

import argparse
import json
import logging
import sys

from ndfc_python.common.fabric.fabric_inventory import FabricInventory
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
from ndfc_python.validators.bootflash_files_info import BootflashFilesInfoConfigValidator, SwitchSpec
from plugins.module_utils.bootflash.bootflash_info import BootflashInfo
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.common.switch_details import SwitchDetails
from pydantic import ValidationError


def get_switch_ip_address(switch_name: str, inventory: dict) -> str:
    """
    Get the IP address of a switch.

    Args:
        switch_name (str): The name of the switch.
        inventory (dict): The fabric inventory

    Returns:
        ipv4 address (str) of switch_name
    """
    if switch_name not in inventory:
        errmsg = f"Switch {switch_name} not found in inventory."
        log.error(errmsg)
        print(errmsg)
        sys.exit(1)
    switch_ip4 = inventory[switch_name].get("ipAddress")
    if not switch_ip4:
        errmsg = f"Switch {switch_name} has no ipAddress."
        log.error(errmsg)
        print(errmsg)
        sys.exit(1)
    return switch_ip4


def get_fabric_inventories(switches: list[SwitchSpec], send: RestSend) -> dict:
    """
    Get the fabric inventories associated with the switches in SwitchSpec.

    Args:
        switches (list[SwitchSpec]): The switch specifications, each consisting of fabric_name and switch_name.
        rest_send (RestSend): The REST send object.

    Returns:
        dict: The fabric inventories, keyed by fabric name, then by switch name.
    """
    instance = FabricInventory()
    instance.rest_send = send
    instance.results = Results()
    # Build a set of unique fabric names from the switches list
    fabric_names = set(switch.get("fabric_name") for switch in switches)
    fabric_inventories = {}
    for fabric_name in fabric_names:
        instance.fabric_name = fabric_name
        instance.commit()
        fabric_inventories[fabric_name] = instance.inventory
    return fabric_inventories


def print_files(bootflash_info: BootflashInfo, switch_ip_addresses: dict, cfg: BootflashFilesInfoConfigValidator) -> None:
    """Print the bootflash files information for the specified switches.

    Args:
        bootflash_info (BootflashInfo): The BootflashInfo instance containing the file information from the switches.
        switch_ip_addresses (dict): A dictionary mapping switch names to their IP addresses and fabric names.
        cfg (BootflashFilesInfoConfigValidator): The configuration validator containing target information.
    """
    for switch_name, switch_info in switch_ip_addresses.items():
        bootflash_info.filter_switch = switch_info["ip_address"]
        for target in cfg.targets:
            bootflash_info.filter_filepath = target.filepath
            bootflash_info.filter_supervisor = target.supervisor.value
            msg = f"Filtering on fabric_name {switch_info['fabric_name']}, "
            msg += f"switch_name {switch_name}, "
            msg += f"supervisor {target.supervisor.value}, "
            msg += f"filepath {target.filepath}\n"
            msg += f"{json.dumps(bootflash_info.matches, sort_keys=True, indent=4)}"
            print(msg)


def build_switch_ip_addresses(cfg: BootflashFilesInfoConfigValidator, send: RestSend) -> dict:
    """Build a mapping of switch names to their IP addresses and fabric names.

    Args:
        cfg (BootflashFilesInfoConfigValidator): The configuration validator containing switch information.
        send (RestSend): The RestSend instance for making API calls.

    Returns:
        dict: A mapping of switch names to their IP addresses and fabric names.

    Raises:
        ValueError: If a fabric name is missing or if a fabric associated with a switch is not found.
    """
    inventories = get_fabric_inventories(cfg.switches, send)
    switch_ip_addresses = {}
    for switch in cfg.switches:
        fabric_name = switch.get("fabric_name")
        switch_name = switch.get("switch_name")
        if not fabric_name:
            errmsg = f"fabric_name missing from switch entry {switch}"
            raise ValueError(errmsg)
        if fabric_name not in inventories:
            errmsg = f"Fabric {fabric_name} "
            errmsg += f"associated with switch {switch_name} "
            errmsg += "not found on the controller."
            raise ValueError(errmsg)
        switch_ip = get_switch_ip_address(switch_name, inventories[fabric_name])
        switch_ip_addresses[switch_name] = {"fabric_name": fabric_name, "ip_address": switch_ip}
    return switch_ip_addresses


def prepare_bootflash_info(switch_ip_addresses: dict, send: RestSend) -> BootflashInfo:
    """
    Instantiate the BootflashInfo instance and inject mandatory dependencies.

    Args:
        switch_ip_addresses (dict): A mapping of switch names to their IP addresses and fabric names.
        send (RestSend): The RestSend instance for making API calls.

    Returns:
        BootflashInfo: The prepared BootflashInfo instance.
    """
    bootflash_info = BootflashInfo()
    bootflash_info.results = Results()
    bootflash_info.switch_details = SwitchDetails()
    bootflash_info.switch_details.results = Results()
    bootflash_info.switches = [switch_data["ip_address"] for switch_data in switch_ip_addresses.values()]

    send.state = "query"
    bootflash_info.rest_send = send
    bootflash_info.refresh()
    return bootflash_info


def action(cfg: BootflashFilesInfoConfigValidator, send: RestSend) -> None:
    """
    Given a bootflash files info validator object and a RestSend object,
    query the bootflash files on the switches specified in the validator object
    and print the results.

    Raises:
        ValueError: If there is an error in processing.
    """
    try:
        switch_ip_addresses = build_switch_ip_addresses(cfg, send)
        bootflash_info = prepare_bootflash_info(switch_ip_addresses, send)
        print_files(bootflash_info, switch_ip_addresses, cfg)
    except ValueError as error:
        raise ValueError from error


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


args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel(args.loglevel)

try:
    user_config = ReadConfig()
    user_config.filename = args.config
    user_config.commit()
except ValueError as error:
    err_msg = f"Exiting: Error detail: {error}"
    log.error(err_msg)
    print(err_msg)
    sys.exit(1)

try:
    validator = BootflashFilesInfoConfigValidator(**user_config.contents)
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

rest_send = RestSend({})
rest_send.send_interval = 3
rest_send.timeout = 9
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()
rest_send.results = Results()

try:
    action(validator, rest_send)
except ValueError as error:
    err_msg = f"Exiting.  Error detail: {error}"
    log.error(err_msg)
    print(err_msg)
    sys.exit(1)
