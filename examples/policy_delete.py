#!/usr/bin/env python3
"""
# Name

policy_delete.py

## Description

Delete a policy

## NOTES

1. The policy scripts in this repository use the policy description as a unique identifier for a policy.
This was a design decision made to improve user-friendliness of the scripts.  Nexus Dashboard uses
a unique policy ID (e.g. POLICY-12810) to identify policies.  We felt that using the policy ID would
be less user-friendly as users would have to look up the policy ID before they could use the scripts.

The implication of this design is that deleting a policy will be rejected if the controller
returns multiple policies with the same description for a given switch.

## Usage

Edit ``examples/config/policy_delete.yaml`` appropriately for your requirements.

```yaml
---
config:
  - switch_name: LE1
    fabric_name: SITE1
    description: management vrf static route to syslog server
```

If you've set the standard ndfc-python Nexus Dashboard credentials environment variables (ND_DOMAIN, ND_IP4, ND_PASSWORD, ND_USERNAME) then you're good to go.

```bash
./policy_delete.py --config config/policy_delete.yaml
```

If you haven't set the standard ndfc-python Nexus Dashboard credentials environment variables, you can override them like so:

```bash
./policy_delete.py --config config/policy_delete.yaml --nd-username admin --nd-password MyPassword --nd-domain local --nd-ip4 10.1.1.2
```
"""
# pylint: disable=duplicate-code
import argparse
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
from ndfc_python.policy_delete import PolicyDelete
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.policy_delete import PolicyDeleteConfig, PolicyDeleteConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def action(cfg: PolicyDeleteConfig) -> None:
    """
    Given a policy configuration, delete the policy.
    """
    try:
        instance = PolicyDelete()
        instance.rest_send = rest_send
        instance.results = Results()
        instance.description = cfg.description
        instance.fabric_name = cfg.fabric_name
        instance.switch_name = cfg.switch_name
        instance.commit()
    except (TypeError, ValueError) as error:
        errmsg = "Error deleting policy for "
        errmsg += f"fabric {cfg.fabric_name}, "
        errmsg += f"switch {cfg.switch_name}, "
        errmsg += f"policy description '{cfg.description}'. "
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    result_msg = "Deleted "
    result_msg += f"fabric {instance.fabric_name}, "
    result_msg += f"switch {instance.switch_name}, "
    # If the request was successful, there will be exactly one policy_id in instance.policy_ids
    result_msg += f"policy_id {instance.policy_ids[0]}"
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
        description="DESCRIPTION: Delete policy from one or more switches.",
    )
    return parser.parse_args()


args = setup_parser()


NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

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
    validator = PolicyDeleteConfigValidator(**ndfc_config.contents)
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
