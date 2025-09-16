#!/usr/bin/env python

"""
Name: fabrics_info.py

Description:

Example script demonstrating usage for FabricsInfo (lib/ndfc_python/common/fabric/fabrics_info.py).

Given a configuration file, return information for each of the filtered fabrics.

Configuration file example:

``` yaml
---
config:
    - filter: NON_EXISTENT_FABRIC
    - filter: SITE1
    - filter: "" # All fabrics
```
"""

import argparse
import json
import logging
import sys

from ndfc_python.common.fabric.fabrics_info import FabricsInfo
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
from ndfc_python.validators.fabrics_info import FabricsInfoConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from pydantic import ValidationError


def action(cfg: FabricsInfoConfigValidator, instance: FabricsInfo) -> None:
    """Perform action based on the configuration and fabric instance.

    Args:
        cfg (FabricsInfoConfigValidator): An instance of FabricsInfoConfigValidator containing configuration details.
        instance (FabricsInfo): An instance of FabricsInfo.
    """
    instance.filter = cfg.filter

    if cfg.filter:
        fabric_exists = instance.fabric_exists
        print(f"Fabric {cfg.filter} exists: {fabric_exists}")
        if fabric_exists:
            print(f"Fabric {cfg.filter} details: ")
            print(f"{json.dumps(instance.fabric, indent=4, sort_keys=True)}")
    else:
        print("All Fabrics information: ")
        for fabric in instance.fabrics:
            print(f"{json.dumps(fabric, indent=4, sort_keys=True)}")


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
        description="DESCRIPTION: Retrieve fabrics information.",
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
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    validator = FabricsInfoConfigValidator(**user_config.contents)
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
fabrics_info = FabricsInfo()
fabrics_info.rest_send = rest_send
fabrics_info.commit()
for item in validator.config:
    action(item, fabrics_info)
