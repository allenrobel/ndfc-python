#!/usr/bin/env python3
"""
# Name

vrf_add.py

# Description

Add a vrf to a fabric

#Usage

Edit ``examples/config_vrf_add.yaml`` appropriately for your setup.

```yaml
config:
  fabric_name: MyFabric
  vrf_display_name: MyVrf
  vrf_id: 50055
  vrf_name: MyVrf
  vrf_vlan_id: 2006
```

If you've set the standard ndfc-python Nexus Dashboard credentials
environment variables (NDFC_DOMAIN, NDFC_IP4, NDFC_PASSWORD, NDFC_USERNAME)
then you're good to go.

```bash
./vrf_add.py --config config_vrf_add.yaml
```

If you haven't set the standard ndfc-python Nexus Dashboard credentials
environment variables, you can override them like so:

```bash
./vrf_add.py --config device_info_config.yaml --username admin --password MyPassword --domain local --ip4 10.1.1.2
"""
import argparse
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_controller_domain import \
    parser_controller_domain
from ndfc_python.parsers.parser_controller_ip4 import parser_controller_ip4
from ndfc_python.parsers.parser_controller_password import \
    parser_controller_password
from ndfc_python.parsers.parser_controller_username import \
    parser_controller_username
from ndfc_python.parsers.parser_loglevel import parser_loglevel
# We are using our local copy of log_v2.py which is modified to allow
# console logging.  The copy in the DCNM Ansible Collection specifically
# disallows console logging.
from ndfc_python.read_config import ReadConfig
from ndfc_python.vrf_create import VrfCreate
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results


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
    sys.exit(1)

try:
    ndfc_config = ReadConfig()
    ndfc_config.filename = args.config
    ndfc_config.commit()
    config = ndfc_config.contents["config"]
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    sys.exit()

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()

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
except ValueError as error:
    msg = "Error creating vrf. "
    msg += f"Error detail: {error}"
    log.error(msg)
