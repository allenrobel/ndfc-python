#!/usr/bin/env python3
"""
# recalculate_and_deploy.py

## Description

Trigger a Recalculate and Deploy on one or more fabrics in NDFC.

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible-dcnm
```

2. Optional, to enable logging.

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

3. Edit ./examples/config/config_recalculate_and_deploy.yaml with desired fabric names

4. Set credentials via script command line, environment variables, or Ansible Vault

5. Run the script (below we're using command line for credentials)

``` bash
./examples/recalculate_and_deploy.py \
    --config ./examples/config/config_recalculate_and_deploy.yaml \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin
```
"""

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
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend

def setup_parser() -> argparse.Namespace:
    """
    Setup script-specific parser
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
        description="DESCRIPTION: Trigger Recalculate and Deploy on one or more fabrics.",
    )
    return parser.parse_args()

args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel(args.loglevel)

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
rest_send.timeout = 10
rest_send.send_interval = 2

# Expecting config file like:
# config:
#   - fabric_name: MyFabric1
#   - fabric_name: MyFabric2
fabrics = ndfc_config.contents.get("config", [])

for fabric in fabrics:
    fabric_name = fabric.get("fabric_name")
    if not fabric_name:
        log.error("Missing fabric_name in config entry: %s", fabric)
        continue
    path = f"/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_name}/recalculateAndDeploy"
    try:
        rest_send.path = path
        rest_send.verb = "POST"
        rest_send.payload = {}  # No payload required
        rest_send.commit()
        msg = f"Triggered Recalculate and Deploy for fabric '{fabric_name}':\n{json.dumps(rest_send.response_current, indent=4)}"
        log.info(msg)
        print(msg)
    except (TypeError, ValueError) as error:
        msg = f"Error triggering Recalculate and Deploy for fabric '{fabric_name}'. Error detail: {error}"
        log.error(msg)
        print(msg)
