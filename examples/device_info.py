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
./device_info.py --config config/device_info.yaml
```

You can override the environment variables like so:

```bash
./device_info.py --config config/device_info.yaml --nd-username admin --nd-password MyPassword --nd-domain local --nd-ip4 10.1.1.2
```

"""
# pylint: disable=duplicate-code
import argparse
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
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.device_info import DeviceInfoConfig, DeviceInfoConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.common.switch_details import SwitchDetails
from pydantic import ValidationError


def get_fabric_inventory(fabric_name: str, restsend: RestSend, results: Results) -> dict:
    """
    Given a fabric name, return the fabric inventory as a dictionary.

    Args:
        fabric_name (str): fabric name
        rest_send (RestSend): REST send object
        results (Results): results object

    Returns:
        dict: fabric inventory
    """
    fabric_inventory = FabricInventory()
    fabric_inventory.fabric_name = fabric_name
    fabric_inventory.rest_send = restsend
    fabric_inventory.results = results
    fabric_inventory.commit()
    return fabric_inventory.inventory


def action(cfg: DeviceInfoConfig, switch_details_instance: SwitchDetails) -> None:
    """
    Given an instance of SwitchDetails, which has its filter set
    to a switch ip address, print information about the switch.
    """
    inventory = get_fabric_inventory(cfg.fabric_name, switch_details_instance.rest_send, switch_details_instance.results)
    if cfg.switch_name not in inventory:
        errmsg = f"Switch {cfg.switch_name} not found in fabric {cfg.fabric_name} inventory."
        log.error(errmsg)
        print(errmsg)
        return

    switch_ip4 = inventory[cfg.switch_name].get("ipAddress")
    if not switch_ip4:
        errmsg = f"Switch {cfg.switch_name} in fabric {cfg.fabric_name} has no ipAddress."
        log.error(errmsg)
        print(errmsg)
        return

    try:
        switch_details_instance.filter = switch_ip4
        switch_details_instance.refresh()
    except ValueError as error:
        errmsg = "Unable to get switch details. "
        errmsg += f"Error details: {error}"
        log.error(errmsg)
        print(errmsg)
        return
    try:
        print(f"{switch_details_instance.logical_name}")
        print(f"  ipv4_address {switch_details_instance.filter}")
        print(f"  serial_number: {switch_details_instance.serial_number}")
        print(f"  fabric_name: {switch_details_instance.fabric_name}")
        print(f"  role: {switch_details_instance.role}")
        print(f"  status: {switch_details_instance.status}")
        print(f"  model: {switch_details_instance.model}")
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
    user_config = ReadConfig()
    user_config.filename = args.config
    user_config.commit()
    config = user_config.contents["config"]
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit()

try:
    validator = DeviceInfoConfigValidator(**user_config.contents)
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

for item in validator.config:
    action(item, instance)
