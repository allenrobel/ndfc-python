#!/usr/bin/env python3
"""
# Name

vrf_create.py

# Description

Add a vrf to a fabric

#Usage

Edit ``examples/config_vrf_create.yaml`` appropriately for your setup.

```yaml
config:
  fabric_name: MyFabric
  vrf_display_name: MyVrf
  vrf_id: 50055
  vrf_name: MyVrf
  vrf_vlan_id: 2006
```

If you've set the standard ndfc-python Nexus Dashboard credentials
environment variables (ND_DOMAIN, ND_IP4, ND_PASSWORD, ND_USERNAME)
then you're good to go.

```bash
./vrf_create.py --config config_vrf_create.yaml
```

If you haven't set the standard ndfc-python Nexus Dashboard credentials
environment variables, you can override them like so:

```bash
./vrf_create.py --config device_info_config.yaml --nd-username admin --nd-password MyPassword --nd-domain local --nd-ip4 10.1.1.2
"""
# pylint: disable=duplicate-code
import argparse
import json
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_controller_domain import parser_controller_domain
from ndfc_python.parsers.parser_controller_ip4 import parser_controller_ip4
from ndfc_python.parsers.parser_controller_password import parser_controller_password
from ndfc_python.parsers.parser_controller_username import parser_controller_username
from ndfc_python.parsers.parser_loglevel import parser_loglevel

# We are using our local copy of log_v2.py which is modified to allow
# console logging.  The copy in the DCNM Ansible Collection specifically
# disallows console logging.
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators import VrfCreateConfigValidator
from ndfc_python.vrf_create import VrfCreate
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def vrf_create(config):
    """
    Given a VRF configuration, create the VRF.
    """
    try:
        instance = VrfCreate()
        instance.rest_send = rest_send
        instance.results = Results()
        instance.display_name = config.get("vrf_display_name")
        instance.fabric_name = config.get("fabric_name")
        instance.vrf_id = config.get("vrf_id")
        instance.vrf_name = config.get("vrf_name")
        instance.vrf_vlan_id = config.get("vrf_vlan_id")
        instance.commit()
    except (TypeError, ValueError) as error:
        errmsg = f"Error creating vrf {instance.vrf_name}. "
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    result_msg = f"Created vrf {instance.vrf_name} "
    result_msg += f"in fabric {instance.fabric_name}"
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
            parser_config,
            parser_loglevel,
            parser_controller_domain,
            parser_controller_ip4,
            parser_controller_password,
            parser_controller_username,
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
    validator = VrfCreateConfigValidator(**ndfc_config.contents)
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
    vrf_create(params)
