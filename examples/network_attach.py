#!/usr/bin/env python3
"""
# network_attach.py

## Description

Attach a network

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible/collections/ansible_collections/cisco/dcnm
```

2. Optional, to enable logging.

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

3. Edit ./examples/config/network_attach.yaml with desired network values

4. Set credentials via script command line, environment variables, or Ansible Vault

5. Run the script (below we're using command line for credentials)

``` bash
./examples/network_attach.py \
    --config ./examples/config/network_attach.yaml \
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
from ndfc_python.network_attach import NetworkAttach
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.network_attach import NetworkAttachConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def network_attach(cfg: dict) -> None:
    """
    Given a network configuration, create the network.
    """
    try:
        instance = NetworkAttach()
        instance.rest_send = rest_send
        instance.results = Results()
        print(f"ZZZ network_attach: cfg {cfg}")
        instance.deployment = cfg.get("deployment")
        instance.detach_switch_ports = cfg.get("detachSwitchPorts", [])
        instance.dot1q_vlan = cfg.get("dot1qVlan")
        instance.extension_values = cfg.get("extensionValues", "")
        instance.fabric_name = cfg.get("fabric", "")
        instance.freeform_config = cfg.get("freeformConfig", [])
        instance.instance_values = cfg.get("instanceValues", "")
        instance.mso_created = cfg.get("msoCreated", False)
        instance.mso_set_vlan = cfg.get("msoSetVlan", False)
        instance.network_name = cfg.get("networkName")
        instance.serial_number = cfg.get("serialNumber")
        instance.switch_ports = cfg.get("switchPorts", [])
        instance.tor_ports = cfg.get("torPorts", [])
        instance.untagged = cfg.get("untagged", False)
        instance.vlan = cfg.get("vlan")
        instance.commit()
    except ValueError as error:
        errmsg = "Error attaching network. "
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    result_msg = f"Network {instance.network_name} "
    result_msg += f"attached to fabric {instance.fabric_name}, "
    result_msg += f"serial number {instance.serial_number}."
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
        description="DESCRIPTION: Create a network.",
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
    validator = NetworkAttachConfigValidator(**user_config.contents)
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

params_list = json.loads(validator.model_dump_json()).get("config", {})

for params in params_list:
    network_attach(params)
