#!/usr/bin/env python3
"""
# fabric_inventory.py
## Description
Get fabric inventory information
## Usage
1.  Modify PYTHONPATH appropriately for your setup before running this script
``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos
/ansible/collections/ansible_collections/cisco/dcnm
```
2. Optional, to enable logging.
``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```
3. Run the script
``` bash
./examples/fabric_inventory.py \
    --nd-domain local \
    --nd-ip4 192.168.1.1 \
    --nd-password password \
    --nd-username admin
```
"""
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
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.fabric_inventory import FabricInventoryConfig, FabricInventoryConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def fabric_inventory(config: FabricInventoryConfig) -> None:
    """
    ### Summary

    Retrieve fabric inventory information

    Args:
        config (dict): configuration dictionary

    Returns:
        None
    """
    instance = FabricInventory()
    instance.fabric_name = config.fabric_name
    instance.rest_send = rest_send
    instance.results = Results()
    instance.commit()
    if args.detailed:
        print(f"Fabric {config.fabric_name}:")
        for device in sorted(instance.devices):
            print(f"  {device}: {json.dumps(instance.inventory.get(device), sort_keys=True, indent=4)}")
    else:
        print(f"Fabric {config.fabric_name}: {sorted(instance.devices)}")


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
            parser_loglevel,
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
        ],
        description="DESCRIPTION: Retrieve fabric inventory.",
    )
    parser.add_argument("--detailed", action="store_true", help="Show detailed fabric inventory information")
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
    msg = f"Exiting: Error detail: {error}"
    print(msg)
    log.error(msg)
    sys.exit(1)

try:
    validator = FabricInventoryConfigValidator(**user_config.contents)
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
rest_send.results = Results()
rest_send.timeout = 2
rest_send.send_interval = 5

for item in validator.config:
    try:
        fabric_inventory(item)
    except ValueError as error:
        msg = f"Error processing {item}: {error}"
        print(msg)
        log.error(msg)
