#!/usr/bin/env python3
"""
# Name

policy_create.py

# Description

Create a policy

#Usage

Edit ``examples/config/policy_create.yaml`` appropriately for your requirements.

```yaml
---
config:
  - switch_name: LE1
    fabric_name: SITE1 # fabric_name needed to retrieve switch information
    description: management vrf static route to syslog server
    entity_name: SWITCH
    entity_type: SWITCH
    priority: 200
    source: ""
    template_name: vrf_static_route
    nv_pairs:
      IP_PREFIX: 192.168.7.1/32
      NEXT_HOP_IP: 192.168.12.1
      VRF_NAME: management
```

If you've set the standard ndfc-python Nexus Dashboard credentials
environment variables (ND_DOMAIN, ND_IP4, ND_PASSWORD, ND_USERNAME)
then you're good to go.

```bash
./policy_create.py --config config/config_policy_create.yaml
```

If you haven't set the standard ndfc-python Nexus Dashboard credentials
environment variables, you can override them like so:

```bash
./policy_create.py --config config/config_policy_create.yaml --nd-username admin --nd-password MyPassword --nd-domain local --nd-ip4 10.1.1.2
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
from ndfc_python.policy_create import PolicyCreate
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.policy_create import PolicyCreateConfig, PolicyCreateConfigValidator
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def action(cfg: PolicyCreateConfig) -> None:
    """
    Given a policy configuration, create the policy.
    """
    try:
        instance = PolicyCreate()
        instance.rest_send = rest_send
        instance.results = Results()
        instance.description = cfg.description
        instance.fabric_name = cfg.fabric_name
        instance.entity_name = cfg.entityName
        instance.entity_type = cfg.entityType
        instance.nv_pairs = cfg.nvPairs
        instance.priority = cfg.priority
        instance.source = cfg.source
        instance.switch_name = cfg.switchName
        instance.template_name = cfg.templateName
        instance.template_content_type = cfg.templateContentType
        instance.commit()
    except (TypeError, ValueError) as error:
        errmsg = "Error creating "
        errmsg += f"fabric {cfg.fabric_name}, "
        errmsg += f"switch {cfg.switchName}, "
        errmsg += f"policy (template_name: {cfg.templateName}). "
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    result_msg = "Created "
    result_msg += f"fabric {instance.fabric_name}, "
    result_msg += f"switch {instance.switch_name}, "
    result_msg += f"policy_id {instance.rest_send.response_current.get('DATA', {}).get('policyId', 'N/A')}."
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
    validator = PolicyCreateConfigValidator(**ndfc_config.contents)
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
