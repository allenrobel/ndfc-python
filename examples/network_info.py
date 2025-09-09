#!/usr/bin/env python3
"""
# network_info.py

## Description

Retrieve information for networks

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible/collections/ansible_collections/cisco/dcnm
```

2. Optional, to enable logging.

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

3. Edit ./examples/config/network_info.yaml with desired network values

4. Set credentials via script command line, environment variables, or Ansible Vault

5. Run the script (below we're using command line for credentials)

``` bash
./examples/network_info.py \
    --config ./examples/config/network_info.yaml \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin

```

"""
# pylint: disable=duplicate-code
import argparse
import json
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.network_info import NetworkInfo
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.network_info import NetworkInfoConfig, NetworkInfoConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def action(cfg: NetworkInfoConfig) -> None:
    """
    Given a network configuration, retrieve information for the specified network.
    """
    # Prepopulate error message
    fabric_name = cfg.fabric_name
    network_name = cfg.network_name
    errmsg = "Error retrieving network information for "
    errmsg += f"fabric_name {fabric_name} "
    errmsg += f"network_name {network_name}. "
    try:
        instance = NetworkInfo()
        instance.rest_send = rest_send
        instance.results = Results()
        instance.fabric_name = fabric_name
        instance.network_name = network_name
        instance.commit()
        data = instance.rest_send.response_current.get("DATA", {})
    except ValueError as error:
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    if instance.rest_send.response_current.get("RETURN_CODE") not in (200, 201):
        if instance.rest_send.response_current.get("DATA", {}).get("message"):
            errmsg = instance.rest_send.response_current.get("DATA", {}).get("message")
        else:
            errmsg = "Error retrieving network information. "
            errmsg += f"Controller response: {instance.rest_send.response_current}"
        log.error(errmsg)
        print(errmsg)
        return
    result_msg = f"fabric_name {instance.fabric_name}, "
    result_msg += f"network_name {instance.network_name} info\n"
    result_msg += f"{json.dumps(sort_keys=True, indent=4, obj=data)}."
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
        description="DESCRIPTION: Retrieve information for networks.",
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
    validator = NetworkInfoConfigValidator(**user_config.contents)
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
rest_send.timeout = 2
rest_send.send_interval = 5

for item in validator.config:
    action(item)
