#!/usr/bin/env python3
"""
Name: rm_switch_resource_usage.py
Description: Get switch resource usage from Nexus Dashboard Resource Manager

NOTES:

1.  Set the following environment variables before running this script
    (edit appropriately for your setup)

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible/collections/ansible_collections/cisco/dcnm
```

Optional, to enable logging:

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
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
from ndfc_python.rm_switch_resource_usage import RmSwitchResourceUsage
from ndfc_python.validators.rm_switch_resource_usage import RmSwitchResourceUsageConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def rm_switch_resource_usage(config):
    """
    Given a switch resource usage configuration, get the resource usage.
    """
    try:
        instance.switch_name = config.get("switch_name", "")
        instance.fabric_name = config.get("fabric_name", "")
        instance.filter = config.get("pool_name", "ALL")
        instance.commit()
    except ValueError as error:
        errmsg = "Error retrieving switch resource usage. "
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    result_msg = f"fabric_name {instance.fabric_name}, "
    result_msg += f"switch_name {instance.switch_name} ({instance.serial_number}), "
    result_msg += f"filter {instance.filter}, resource usage:\n"
    result_msg += json.dumps(instance.resource_usage, indent=4)
    log.info(result_msg)
    print(result_msg)


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
        description="DESCRIPTION: Retrieve switch resource usage.",
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
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    validator = RmSwitchResourceUsageConfigValidator(**user_config.contents)
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

instance = RmSwitchResourceUsage()
instance.rest_send = rest_send
instance.results = Results()

params_list = json.loads(validator.model_dump_json()).get("config", {})

for params in params_list:
    rm_switch_resource_usage(params)
