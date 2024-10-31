#!/usr/bin/env python3
"""
Name: reachability.py
Description:

Test for device reachability (from controller perspective)
"""
# pylint: disable=duplicate-code
import argparse
import json
import logging
import sys

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
from ndfc_python.reachability import Reachability
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators import ReachabilityConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def reachability(config):
    """
    Given a reachability config, print reachability information for
    all switches in the config.
    """
    try:
        instance.seed_ip = config.get("seed_ip")
        instance.fabric_name = config.get("fabric_name")
        instance.commit()
    except ValueError as error:
        errmsg = f"Exiting. Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    print(f"sys_name: {instance.sys_name}")
    print(f"  auth: {instance.auth}")
    print(f"  device_index: {instance.device_index}")
    print(f"  hop_count: {instance.hop_count}")
    print(f"  ip_addr: {instance.ip_addr}")
    print(f"  known: {instance.known}")
    print(f"  last_change: {instance.last_change}")
    print(f"  platform: {instance.platform}")
    print(f"  reachable: {instance.reachable}")
    print(f"  selectable: {instance.selectable}")
    print(f"  serial_number: {instance.serial_number}")
    print(f"  status_reason: {instance.status_reason}")
    print(f"  switch_role: {instance.switch_role}")
    print(f"  valid: {instance.valid}")
    print(f"  vdc_id: {instance.vdc_id}")
    print(f"  vdc_mac: {instance.vdc_mac}")
    print(f"  vendor: {instance.vendor}")
    print(f"  version: {instance.version}")


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    ### Returns

    argparse.Namespace

    ### NOTES

    -   parser_controller_* are not currently used.  They'll be used later when
        we modify our libraries to support a combination of credential sources.
        For now, this script accepts only Ansible Vault as a credential source.
    """
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
        description="DESCRIPTION: Display reachability information for a switch.",
    )
    return parser.parse_args()


args = setup_parser()

NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

try:
    ndfc_config = ReadConfig()
    ndfc_config.filename = args.config
    ndfc_config.commit()
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    validator = ReachabilityConfigValidator(**ndfc_config.contents)
except ValidationError as error:
    msg = f"{error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    ndfc_sender = NdfcPythonSender()
    ndfc_sender.args = args
    ndfc_sender.commit()
except ValueError as error:
    msg = f"Exiting.  Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    rest_send = RestSend({})
    rest_send.sender = ndfc_sender.sender
    rest_send.response_handler = ResponseHandler()

    instance = Reachability()
    instance.rest_send = rest_send
    instance.results = Results()
    instance.nxos_username = ndfc_sender.nxos_username
    instance.nxos_password = ndfc_sender.nxos_password
    # For EasyFabric, if overlay_mode is "config-profile" (the default),
    # it's recommended that preserve_config be set to False.  If it's
    # desired to preserve the config, then set overlay_mode to "cli"
    # and set preserve_config to True.
    # instance.overlay_mode = "cli"
    instance.preserve_config = False
    instance.max_hops = 0
except ValueError as error:
    msg = f"Exiting. Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

params_list = json.loads(validator.model_dump_json()).get("config", {})

for params in params_list:
    reachability(params)
