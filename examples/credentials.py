#!/usr/bin/env python
"""
Name: credentials.py
Description:

Print Ansible Vault credentials.
"""
# pylint: disable=duplicate-code
import argparse
import logging
import sys

from ndfc_python.credentials.credentials_ansible_vault import CredentialsAnsibleVault
from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_loglevel import parser_loglevel


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        parents=[parser_loglevel, parser_ansible_vault],
        description="DESCRIPTION: Display credentials from an Ansible Vault.",
    )
    return parser.parse_args()


args = setup_parser()

if args.ansible_vault is None:
    msg = "Usage: credentials.py --ansible-vault /path/to/ansible/vault"
    print(msg)
    sys.exit(1)

NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

try:
    cav = CredentialsAnsibleVault()
    cav.ansible_vault = args.ansible_vault
    cav.commit()
except ValueError as error:
    msg = "Perhaps an incorrect vault password was entered? "
    msg += f"Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

print(f"nd_domain {cav.nd_domain}")
print(f"nd_ip4 {cav.nd_ip4}")
print(f"nd_password {cav.nd_password}")
print(f"nd_username {cav.nd_username}")
print(f"nxos_password {cav.nxos_password}")
print(f"nxos_username {cav.nxos_username}")
