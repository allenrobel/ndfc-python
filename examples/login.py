#!/usr/bin/env python
"""
Name: login.py
Summary: Basic NDFC login.
Description:

Login to an NDFC controller and print the returned auth token.

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

"""
# pylint: disable=duplicate-code
import argparse
import logging
import sys

# We are using our local copy of log_v2.py which is modified to
# console logging.  The copy in the DCNM Ansible Collection specifically
# disallows console logging.
from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username


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
            parser_loglevel,
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
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

msg = f"Sender().token: {ndfc_sender.sender.token}"
log.info(msg)
