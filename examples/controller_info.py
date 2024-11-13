#!/usr/bin/env python
"""
# [controller_info.py]

[controller_info.py]: https://github.com/allenrobel/ndfc-python/blob/main/examples/controller_info.py

## Description

Return controller information (version, etc).

## Usage

1. See credentials.py for various options to set credentials.
2. Run the script (we're using command-line for credentials below).

``` bash
./controller_info.py --nd_username admin --nd_password MyPassword --nd_domain local --nd_ip4 10.1.1.1
```
"""
# pylint: disable=duplicate-code
import argparse
import json
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.parsers.parser_nxos_password import parser_nxos_password
from ndfc_python.parsers.parser_nxos_username import parser_nxos_username
from plugins.module_utils.common.controller_version import ControllerVersion
from plugins.module_utils.common.exceptions import ControllerResponseError
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        parents=[
            parser_ansible_vault,
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
            parser_nxos_password,
            parser_nxos_username,
            parser_loglevel,
        ],
        description="DESCRIPTION: Print controller version information.",
    )
    return parser.parse_args()


args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

try:
    ndfc_sender = NdfcPythonSender()
    ndfc_sender.args = args
    ndfc_sender.commit()
except ValueError as error:
    msg = f"Exiting.  Error detail: {error}"
    print(msg)
    log.error(msg)
    sys.exit(1)

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()
rest_send.results = Results()

controller_version = ControllerVersion()
controller_version.rest_send = rest_send
try:
    controller_version.refresh()
except ControllerResponseError as error:
    msg = f"Exiting.  Error detail: {error}"
    print(msg)
    log.error(msg)
    sys.exit(1)

padding = 10
print("Controller information:")
print(f"{controller_version.version:<15} Full version")
print(f"{controller_version.version_major:<15} Major version")
print(f"{controller_version.version_minor:<15} Minor version")
print(f"{controller_version.version_patch:<15} Patch version")
if controller_version.dev is not None:
    print(f"{str(controller_version.dev):<15} Development version")
if controller_version.uuid is not None:
    print(f"{controller_version.uuid:<15} UUID")
if controller_version.mode is not None:
    print(f"{controller_version.mode:<15} Mode")
if controller_version.is_upgrade_inprogress is not None:
    print(f"{str(controller_version.is_upgrade_inprogress):<15} Upgrade in progress")
if controller_version.is_media_controller is not None:
    print(f"{str(controller_version.is_media_controller):<15} Media Controller")
if controller_version.is_ha_enabled is not None:
    print(f"{str(controller_version.is_ha_enabled):<15} High Availability enabled")
if controller_version.install is not None:
    print(f"{controller_version.install:<15} Install")
print("Raw response:")
print(json.dumps(controller_version.response_data, indent=4, sort_keys=True))
