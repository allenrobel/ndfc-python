#!/usr/bin/env python
"""
Name: fabric_info.py
Description:

Return fabric information for FABRIC_NAME.

Usage:

1. Set the following environment variables appropriately for your setup:

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible/collections/ansible_collections/cisco/dcnm
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
# The following contains the path to your Ansible Vault.  Not needed if you
# are not using Ansible Vault.
export NDFC_PYTHON_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/config/config.yml
export ND_USERNAME=admin
export ND_PASSWORD=MyPassword
export ND_DOMAIN=local
export ND_IP4=10.1.1.1
```

1a. Alternately, you can override ND_USERNAME, ND_PASSWORD,
    ND_DOMAIN, and ND_IP4 within the script.  Examples:

    Explicitly setting these:

    sender = Sender()
    sender.username = "admin"
    sender.password = "MyPassword"
    sender.domain = "local"
    sender.ip4 = "10.1.1.1"
    sender.login()

2a. If you'd rather use Ansible Vault, modify the script to include:

    cav = CredentialsAnsibleVault()
    sender = Sender()
    sender.username = cav.nd_username
    sender.password = cav.nd_password
    sender.domain = cav.nd_domain
    sender.ip4 = cav.nd_ip4
    sender.login()


2b.  If using Ansible vault, edit the YAML file pointed to by environment
     variable NDFC_PYTHON_CONFIG to contain at least the following.
     NdfcCredentials() reads this variable to locate the configuration file
     that contains a path to your vault.

    ---
    ansible_vault: "/path/to/your/ansible/vault"

3. Set the FABRIC_NAME variable in the script below.

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

# We are using our local copy of log_v2.py which is modified to
# console logging.  The copy in the DCNM Ansible Collection specifically
# disallows console logging.
from ndfc_python.read_config import ReadConfig
from ndfc_python.validators.fabric_info import FabricInfoConfigValidator

# fmt: off
from plugins.module_utils.common.api.v1.lan_fabric.rest.control.fabrics.fabrics import EpFabricDetails

# fmt: on
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


def fabric_info(config):
    """
    Given a fabric configuration, print information about the fabric.
    """
    ep_fabric_details.fabric_name = config.get("fabric_name")

    rest_send.path = ep_fabric_details.path
    rest_send.verb = ep_fabric_details.verb
    try:
        rest_send.commit()
    except ValueError as error:
        errmsg = "Problem querying the controller. "
        errmsg += f"Error detail: {error}"
        print(errmsg)
        log.error(errmsg)
        return

    if rest_send.response_current["MESSAGE"] == "Not Found":
        result_msg = f"Fabric {ep_fabric_details.fabric_name} does not exist on the controller"
        print(result_msg)
        log.info(result_msg)
        return

    result_msg = f"{json.dumps(rest_send.response_current['DATA'], indent=4, sort_keys=True)}"
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
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
            parser_loglevel,
        ],
        description="DESCRIPTION: Print information about one or more fabrics.",
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
    print(msg)
    log.error(msg)
    sys.exit()

try:
    validator = FabricInfoConfigValidator(**ndfc_config.contents)
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
    print(msg)
    log.error(msg)
    sys.exit(1)

ep_fabric_details = EpFabricDetails()
rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()
rest_send.results = Results()

params_list = json.loads(validator.model_dump_json()).get("config", {})

for params in params_list:
    fabric_info(params)
