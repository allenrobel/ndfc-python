#!/usr/bin/env python3
"""
# Name

policy_info_switch_generated_config.py

## Description

Display the generated config for policies on one or more switches

## Usage

Edit ``examples/config/policy_info_switch_generated_config.yaml`` appropriately for your requirements.

```yaml
---
config:
  - switch_name: LE1
    fabric_name: SITE1
```

If you've set the standard ndfc-python Nexus Dashboard credentials
environment variables (ND_DOMAIN, ND_IP4, ND_PASSWORD, ND_USERNAME)
then you're good to go.

```bash
./policy_info_switch_generated_config.py --config config/policy_info_switch_generated_config.yaml
```

If you haven't set the standard ndfc-python Nexus Dashboard credentials
environment variables, you can override them like so:

```bash
./policy_info_switch_generated_config.py --config config/policy_info_switch_generated_config.yaml --nd-username admin --nd-password MyPassword --nd-domain local --nd-ip4 10.1.1.2
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
from ndfc_python.policy_info_switch import PolicyInfoSwitch
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.policy_info_switch import PolicyInfoSwitchConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def strip_extra_returns(text: str) -> str:
    """
    Strip extra returns from a string

    Args:
        text (str): Text to strip
    """
    return text.replace("\n\n\n", "\n")


def action(cfg: PolicyInfoSwitch) -> None:
    """
    Given a PolicyInfoSwitch configuration, retrieve and display the switch policies.
    """
    try:
        instance = PolicyInfoSwitch()
        instance.rest_send = rest_send
        instance.results = Results()
        instance.fabric_name = cfg.fabric_name
        instance.switch_name = cfg.switch_name
        instance.commit()
    except (TypeError, ValueError) as error:
        errmsg = "Error retrieving "
        errmsg += f"fabric {cfg.fabric_name}, "
        errmsg += f"switch {cfg.switch_name}, "
        errmsg += "policies. "
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    result_msg = f"{cfg.fabric_name}, {cfg.switch_name}, policies:\n"
    for policy in instance.policies:
        generated_config = policy.get("generatedConfig")
        if generated_config:
            result_msg += strip_extra_returns(generated_config)
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
    ndfc_config = ReadConfig()
    ndfc_config.filename = args.config
    ndfc_config.commit()
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit()

try:
    validator = PolicyInfoSwitchConfigValidator(**ndfc_config.contents)
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
