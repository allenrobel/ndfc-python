#!/usr/bin/env python3
"""
Name: network_create.py
Description: Create a network

NOTES:

1.  Set the following environment variables before running this script
    (edit appropriately for your setup)

export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible-dcnm

Optional, to enable logging:
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json

2. Edit the network values in the script below.
"""
import argparse
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.network_create import NetworkCreate
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_controller_domain import \
    parser_controller_domain
from ndfc_python.parsers.parser_controller_ip4 import parser_controller_ip4
from ndfc_python.parsers.parser_controller_password import \
    parser_controller_password
from ndfc_python.parsers.parser_controller_username import \
    parser_controller_username
from ndfc_python.parsers.parser_loglevel import parser_loglevel
# We are using our local copy of log_v2.py which is modified to allow
# console logging.  The copy in the DCNM Ansible Collection specifically
# disallows console logging.
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators import NetworkCreateConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        parents=[
            parser_config,
            parser_loglevel,
            parser_controller_domain,
            parser_controller_ip4,
            parser_controller_password,
            parser_controller_username,
        ],
        description="DESCRIPTION: Create a network.",
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
    config = ndfc_config.contents["config"]
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit()

try:
    config = NetworkCreateConfigValidator(**ndfc_config.contents)
except ValidationError as error:
    msg = f"{error}"
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


rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()

try:
    instance = NetworkCreate()
    instance.rest_send = rest_send
    instance.results = Results()
    instance.fabric_name = config.get("fabric_name")
    instance.network_name = config.get("network_name")
    instance.enable_ir = config.get("enable_ir")
    instance.gateway_ip_address = config.get("gateway_ip_address")
    instance.network_id = config.get("network_id")
    instance.vlan_id = config.get("vlan_id")
    instance.vrf_name = config.get("vrf_name")
    instance.commit()
except ValueError as error:
    msg = "Error creating network. "
    msg += f"Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

msg = f"Network {config.get('network_name')} "
msg += f"created in fabric {config.get('fabric_name')}"
print(msg)
