#!/usr/bin/env python3
"""
# Name

discover_is_up.py

# Description

Check if switch is up from the controller's perspective.

# Usage

## 1. Set credentials for the Nexus Dashboard controller

Sender() reads credentials from environment variables unless
you override them on the command line (use --help for details):

Environment variables read by Sender()

export ND_DOMAIN=local
export ND_IP4=10.1.1.1
export ND_PASSWORD=MyNdfcPassword
export ND_USERNAME=MyNdfcUsername


## 2. Edit config file

Edit a YAML configuration file appropriately for your setup.
The contents should look like below.  An example is provided
in ndfc-python/examples/discover_config.yaml

```yaml
config:
  discover_password: MySwitchPassword
  discover_username: admin
  fabric_name: MyFabric
  seed_ip: 10.1.1.2
```

## 3. Execute this script

./discover_is_up.py --config discover_config.yaml
"""
# pylint: disable=duplicate-code
import argparse
import logging
import sys
from time import sleep

from ndfc_python.ndfc_discover import NdfcDiscover
from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_controller_domain import parser_controller_domain
from ndfc_python.parsers.parser_controller_ip4 import parser_controller_ip4
from ndfc_python.parsers.parser_controller_password import parser_controller_password
from ndfc_python.parsers.parser_controller_username import parser_controller_username
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.read_config import ReadConfig
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
        description="DESCRIPTION: Check if switch is up from the controller's perspective.",
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

instance = NdfcDiscover()
instance.rest_send = rest_send
instance.results = Results()
instance.fabric_name = config.get("fabric_name")
instance.seed_ip = config.get("seed_ip")
instance.discover_password = config.get("discover_password")
instance.discover_username = config.get("discover_username")
retries = 4
up = False
while up is False and retries > 0:
    try:
        up = instance.is_up()
    except ValueError as err:
        msg = f"exiting. {err}"
        log.error(msg)
        sys.exit(1)
    retries -= 1
    if up is not True:
        sleep(10)
if up is not True:
    msg = f"switch {instance.seed_ip} is not up."
    log.info(msg)
    sys.exit(0)
else:
    msg = f"switch {instance.seed_ip} is up."
    log.info(msg)
    sys.exit(0)
