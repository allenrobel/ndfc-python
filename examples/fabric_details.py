#!/usr/bin/env python
"""
Name: example_ndfc_login.py
Description:

Return fabric information for FABRIC_NAME.

Usage:

1. Set the following environment variables appropriately for your setup:

    export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
    # The following contains the path to your Ansible Vault.  Not needed if you
    # are not using Ansible Vault.
    export NDFC_PYTHON_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/config/config.yml
    export NDFC_USERNAME=admin
    export NDFC_PASSWORD=MyPassword
    export NDFC_DOMAIN=local
    export NDFC_IP4=10.1.1.1

1a. Alternately, you can override NDFC_USERNAME, NDFC_PASSWORD,
    NDFC_DOMAIN, and NDFC_IP4 within the script.  Examples:

    Explicitly setting these:

    sender = Sender()
    sender.username = "admin"
    sender.password = "MyPassword"
    sender.domain = "local"
    sender.ip4 = "10.1.1.1"
    sender.login()

2a. If you'd rather use Ansible Vault, modify the script to include:

    nc = NdfcCredentials()
    sender = Sender()
    sender.username = nc.username
    sender.password = nc.password
    sender.domain = nc.nd_domain
    sender.ip4 = nc.ndfc_ip
    sender.login()


2b.  If using Ansible vault, edit the YAML file pointed to by environment
     variable NDFC_PYTHON_CONFIG to contain at least the following.
     NdfcCredentials() reads this variable to locate the configuration file
     that contains a path to your vault.

    ---
    ansible_vault: "/path/to/your/ansible/vault"

3. Set the FABRIC_NAME variable in the script below.

"""
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

# We are using our local copy of log_v2.py which is modified to
# console logging.  The copy in the DCNM Ansible Collection specifically
# disallows console logging.
from ndfc_python.read_config import ReadConfig
# fmt: off
from plugins.module_utils.common.api.v1.lan_fabric.rest.control.fabrics.fabrics import EpFabricDetails
# fmt: on
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend


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
        description="DESCRIPTION: Print the reachability status of a switch.",
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

ep_fabric_details = EpFabricDetails()
ep_fabric_details.fabric_name = config.get("fabric_name")

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()
rest_send.path = ep_fabric_details.path
rest_send.verb = ep_fabric_details.verb
try:
    rest_send.commit()
except ValueError as error:
    msg = "Problem querying the controller. "
    msg += f"Error detail: {error}"
    log.error(msg)
    sys.exit(1)

if rest_send.response_current["MESSAGE"] == "Not Found":
    msg = f"Fabric {ep_fabric_details.fabric_name} does not exist on the controller"
    log.error(msg)
    sys.exit(1)

msg = f"{json.dumps(rest_send.response_current['DATA'], indent=4, sort_keys=True)}"
print(msg)
