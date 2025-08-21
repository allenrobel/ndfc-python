#!/usr/bin/env python3
"""
# interface_access_create.py

## Description

Create an access-mode interface.

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible/collections/ansible_collections/cisco/dcnm
```

2. Optional, to enable logging.

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

3. Edit ./examples/config/config_interface_access_create.yaml with desired interface values

4. Set credentials via script command line, environment variables, or Ansible Vault

5. Run the script (below we're using command line for credentials)

``` bash
./examples/interface_access_create.py \
    --config ./examples/config/config_interface_access_create.yaml \
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

from ndfc_python.interface_access import InterfaceAccessCreate
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
from ndfc_python.validators.interface_access import InterfaceAccessCreateConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def interface_access_create(config):
    """
    Given a network configuration, create the network.
    """
    try:
        instance = InterfaceAccessCreate()
        instance.rest_send = rest_send
        instance.results = Results()
        instance.access_vlan = config.get("access_vlan")
        instance.bpduguard_enabled = config.get("bpduguard_enabled")
        instance.conf = config.get("conf")
        instance.desc = config.get("desc")
        instance.enable_netflow = config.get("enable_netflow")
        instance.intf_name = config.get("intf_name")
        instance.if_name = config.get("intf_name")
        instance.mtu = config.get("mtu")
        instance.netflow_monitor = config.get("netflow_monitor")
        instance.porttype_fast_enabled = config.get("porttype_fast_enabled")
        instance.ptp = config.get("ptp")
        instance.serial_number = config.get("serial_number")
        instance.speed = config.get("speed")
        result = instance.commit()
    except ValueError as error:
        errmsg = "Error creating interface. "
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    if result["RETURN_CODE"] not in [200, 201] or result["MESSAGE"] != "OK":
        msg = f"Error creating interface {instance.intf_name} on switch {instance.serial_number}. "
        msg += f"Controller response: {result}"
        log.error(msg)
        print(msg)
        return
    result_msg = f"Interface {instance.intf_name} "
    result_msg += f"created on switch {instance.serial_number}"
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
        description="DESCRIPTION: Create an access-mode interface.",
    )
    return parser.parse_args()


args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

try:
    cfg = ReadConfig()
    cfg.filename = args.config
    cfg.commit()
except ValueError as error:
    message = f"Exiting: Error detail: {error}"
    log.error(message)
    print(message)
    sys.exit(1)

try:
    validator = InterfaceAccessCreateConfigValidator(**cfg.contents)
except ValidationError as error:
    message = f"{error}"
    log.error(message)
    print(message)
    sys.exit(1)

try:
    ndfc_sender = NdfcPythonSender()
    ndfc_sender.args = args
    ndfc_sender.commit()
except ValueError as error:
    message = f"Exiting.  Error detail: {error}"
    log.error(message)
    print(message)
    sys.exit(1)

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()
rest_send.timeout = 2
rest_send.send_interval = 5

params_list = json.loads(validator.model_dump_json()).get("config", {})

for params in params_list:
    interface_access_create(params)
