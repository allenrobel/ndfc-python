#!/usr/bin/env python3
"""
# Name

device_info.py

# Description

Retrieve various information about a device, given its ip address.

#Usage

Edit ``device_info_config.yaml`` appropriately for your setup.

```yaml
config:
  switch_ip4: 10.1.1.1
  fabric_name: MyFabric
```

If you've set the standard Nexus Dashboard credentials environment variables
(ND_DOMAIN, ND_IP4, ND_PASSWORD, ND_USERNAME) then you're good to go.

```bash
./device_info.py --config device_info_config.yaml
```

You can override the environment variables like so:

```bash
./device_info.py --config device_info_config.yaml --nd-username admin --nd-password MyPassword --nd-domain local --nd-ip4 10.1.1.2
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
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.device_info import DeviceInfoConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.common.switch_details import SwitchDetails
from pydantic import ValidationError


def device_info(inst):
    """
    Given an instance of SwitchDetails, which has its filter set
    to a switch ip address, print information about the switch.
    """
    try:
        print(f"ipv4_address {inst.filter}")
        print(f"  serial_number: {inst.serial_number}")
        print(f"  fabric_name: {inst.fabric_name}")
        print(f"  status: {inst.status}")
        print(f"  model: {inst.model}")
        # etc, see additional properties in SwitchDetails()
    except ValueError as error:
        errmsg = "Unable to get switch details. "
        errmsg += f"Error details: {error}"
        log.error(errmsg)
        print(errmsg)


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
            parser_config,
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
            parser_loglevel,
        ],
        description="DESCRIPTION: Print information about one or more switches.",
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
    validator = DeviceInfoConfigValidator(**ndfc_config.contents)
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

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()

try:
    instance = SwitchDetails()
    instance.results = Results()
    instance.rest_send = rest_send
    instance.refresh()
except ValueError as error:
    msg = "Unable to get switch details. "
    msg += f"Error details: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

params_list = json.loads(validator.model_dump_json()).get("config", {})

for params in params_list:
    instance.filter = params.get("switch_ip4")
    device_info(instance)
