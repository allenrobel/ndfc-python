#!/usr/bin/env python3
"""
# Name

vrf_delete.py

# Description

Delete one or more VRFs from a fabric

# Usage

Edit ``examples/config/config_vrf_delete.yaml`` appropriately for your setup.

```yaml
---
config:
  - fabric_name: MyFabric_1
    vrf_names:
    - MyVrf1
    - MyVrf2
  - fabric_name: MyFabric_2
    vrf_names:
    - MyVrf3
    - MyVrf4
```

If you've set the standard ndfc-python Nexus Dashboard credentials
environment variables (ND_DOMAIN, ND_IP4, ND_PASSWORD, ND_USERNAME)
then you're good to go.

```bash
./vrf_delete.py --config config_vrf_create.yaml
```

If you haven't set the standard ndfc-python Nexus Dashboard credentials
environment variables, you can override them like so:

```bash
./vrf_delete.py --config config/config_vrf_create.yaml --nd-username admin --nd-password MyPassword --nd-domain local --nd-ip4 10.1.1.2
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
from ndfc_python.validators.vrf_delete import VrfDeleteConfigValidator
from ndfc_python.vrf_delete import VrfDelete
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def vrf_delete(config):
    """
    Given a VRF configuration, delete the VRF.
    """
    try:
        instance = VrfDelete()
        instance.rest_send = rest_send
        instance.results = Results()
        instance.fabric_name = config.get("fabric_name")
        instance.vrf_names = config.get("vrf_names")
        instance.commit()
    except (TypeError, ValueError) as error:
        errmsg = f"Error deleting vrfs {instance.vrf_names} "
        errmsg += f"from fabric {instance.fabric_name}. "
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    vrf_names = ",".join(sorted(instance.vrf_names))
    result_msg = f"Deleted vrfs {vrf_names} "
    result_msg += f"from fabric {instance.fabric_name}"
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
        description="DESCRIPTION: Create a vrf.",
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
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    ndfc_config = ReadConfig()
    ndfc_config.filename = args.config
    ndfc_config.commit()
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit()

try:
    validator = VrfDeleteConfigValidator(**ndfc_config.contents)
except ValidationError as error:
    msg = f"{error}"
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
    vrf_delete(params)
