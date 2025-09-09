#!/usr/bin/env python3
"""
Name: network_delete.py
Description: Delete a network

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

2. Edit the network values in the script below.

"""
# pylint: disable=duplicate-code
import argparse
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.network_delete import NetworkDelete
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.network_delete import NetworkDeleteConfig, NetworkDeleteConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def action(cfg: NetworkDeleteConfig):
    """
    Given a network configuration, delete the network.
    """
    # Prepopulate error message in case of failure
    errmsg = f"Error deleting fabric {cfg.fabric_name}, "
    errmsg += f"network {cfg.network_name}. "
    try:
        instance.fabric_name = cfg.fabric_name
        instance.network_name = cfg.network_name
        instance.commit()
    except ValueError as error:
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    result_msg = f"Network {cfg.network_name} "
    result_msg += f"deleted from fabric {cfg.fabric_name}"
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
        description="DESCRIPTION: Delete a network.",
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
    validator = NetworkDeleteConfigValidator(**ndfc_config.contents)
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

instance = NetworkDelete()
instance.rest_send = rest_send
instance.results = Results()

for item in validator.config:
    action(item)
