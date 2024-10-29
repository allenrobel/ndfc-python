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

from ndfc_python.credentials.credentials_ansible_vault import CredentialsAnsibleVault
from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_controller_domain import parser_controller_domain
from ndfc_python.parsers.parser_controller_ip4 import parser_controller_ip4
from ndfc_python.parsers.parser_controller_password import parser_controller_password
from ndfc_python.parsers.parser_controller_username import parser_controller_username
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.reachability import Reachability
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators import ReachabilityConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


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
            parser_controller_domain,
            parser_controller_ip4,
            parser_controller_password,
            parser_controller_username,
        ],
        description="DESCRIPTION: Display reachability information for a switch.",
    )
    return parser.parse_args()


args = setup_parser()

# TODO: 2024-10-28 Modify once we've added support for ENV, CLI credential sources.
if args.ansible_vault is None:
    msg = "Usage: reachability.py --ansible-vault /path/to/ansible/vault"
    print(msg)
    sys.exit(1)

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
    config = ReachabilityConfigValidator(**ndfc_config.contents)
except ValidationError as error:
    msg = f"{error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

params = json.loads(config.model_dump_json()).get("config", {})

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
    cav = CredentialsAnsibleVault()
    cav.ansible_vault = args.ansible_vault
    cav.commit()
except ValueError as error:
    msg = f"Exiting. Error detail: {error}"
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
    instance.seed_ip = params.get("seed_ip")
    instance.fabric_name = params.get("fabric_name")

    # For EasyFabric, if overlay_mode is "config-profile" (the default),
    # it's recommended that preserve_config be set to False.  If it's
    # desired to preserve the config, then set overlay_mode to "cli"
    # and set preserve_config to True.
    # instance.overlay_mode = "cli"
    instance.preserve_config = False
    instance.max_hops = 0
    instance.nxos_username = cav.nxos_username
    instance.nxos_password = cav.nxos_password
    instance.commit()
except ValueError as error:
    msg = f"Exiting. Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

print(f"auth: {instance.auth}")
print(f"device_index: {instance.device_index}")
print(f"hop_count: {instance.hop_count}")
print(f"ip_addr: {instance.ip_addr}")
print(f"known: {instance.known}")
print(f"last_change: {instance.last_change}")
print(f"platform: {instance.platform}")
print(f"reachable: {instance.reachable}")
print(f"selectable: {instance.selectable}")
print(f"serial_number: {instance.serial_number}")
print(f"status_reason: {instance.status_reason}")
print(f"switch_role: {instance.switch_role}")
print(f"sys_name: {instance.sys_name}")
print(f"valid: {instance.valid}")
print(f"vdc_id: {instance.vdc_id}")
print(f"vdc_mac: {instance.vdc_mac}")
print(f"vendor: {instance.vendor}")
print(f"version: {instance.version}")
