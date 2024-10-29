#!/usr/bin/env python3
"""
# Name

device_info.py

# Description

Retrieve various information about a device, given its ip address.

#Usage

Edit ``device_info_config.yaml`` appropriately for your setup.

```yaml
config:
  switch_ip4: 10.1.1.1
  fabric_name: MyFabric
```

If you've set the standard Nexus Dashboard credentials environment variables
(ND_DOMAIN, ND_IP4, ND_PASSWORD, ND_USERNAME) then you're good to go.

```bash
./device_info.py --config device_info_config.yaml
```

You can override the environment variables like so:

```bash
./device_info.py --config device_info_config.yaml --nd-username admin --nd-password MyPassword --nd-domain local --nd-ip4 10.1.1.2
```

"""
# pylint: disable=duplicate-code
import argparse
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.read_config import ReadConfig
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.common.switch_details import SwitchDetails


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
        ],
        description="DESCRIPTION: Print information about a switch.",
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
    config = ndfc_config.contents["config"]
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit()

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()

try:
    instance = SwitchDetails()
    instance.results = Results()
    instance.rest_send = rest_send
    instance.refresh()
except ValueError as error:
    msg = "Unable to get switch details. "
    msg += f"Error details: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

instance.filter = config.get("switch_ip4")
try:
    print(f"fabric_name: {instance.fabric_name}")
    print(f"serial_number: {instance.serial_number}")
    print(f"status: {instance.status}")
    print(f"model: {instance.model}")
    # etc, see additional properties in SwitchDetails()
except ValueError as error:
    msg = "Unable to get switch details. "
    msg += f"Error details: {error}"
    log.error(msg)
    print(msg)
