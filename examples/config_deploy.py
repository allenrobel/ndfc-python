#!/usr/bin/env python3
"""
# config_deploy.py

## Description

Trigger a Nexus Dashboard Config Deploy for one or more fabrics.

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible/collections/ansible_collections/cisco/dcnm
```

2. Optional, to enable logging.

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

3. Edit ./examples/config/config_recalculate_and_deploy.yaml with desired fabric names

4. Set credentials via script command line, environment variables, or Ansible Vault

5. Run the script (below we're using command line for credentials)

``` bash
./examples/config_deploy.py \
    --config ./examples/config/config_deploy.yaml \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin
```
"""

import argparse
import logging
import sys

from ndfc_python.config_deploy import ConfigDeploy
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
from ndfc_python.validators.config_deploy import ConfigDeployConfig, ConfigDeployConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def action(cfg: ConfigDeployConfig) -> None:
    """
    Trigger a Config Deploy for a fabric.
    """
    # Prepopulate error message
    errmsg = f"Error triggering Config Deploy for fabric '{cfg.fabric_name}'. "
    try:
        instance = ConfigDeploy()
        instance.rest_send = rest_send
        instance.results = Results()
        instance.fabric_name = cfg.fabric_name

        print(f"Triggering Config Deploy for fabric '{cfg.fabric_name}'")
        instance.commit()
        print(instance.status)
    except (TypeError, ValueError) as error:
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)


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
        description="DESCRIPTION: Trigger Config Deploy on one or more fabrics.",
    )
    return parser.parse_args()


args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel(level=args.loglevel)

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
    validator = ConfigDeployConfigValidator(**user_config.contents)
except ValidationError as error:
    msg = f"{error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    ndfc_sender = NdfcPythonSender()
    ndfc_sender.args = args
    ndfc_sender.timeout = 300  # seconds
    ndfc_sender.commit()
except ValueError as error:
    msg = f"Exiting.  Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()
# Set the timeout higher to give Nexus Dashboard time to complete the request
rest_send.timeout = 300  # seconds

for item in validator.config:
    action(item)
