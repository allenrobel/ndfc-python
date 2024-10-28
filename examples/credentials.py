#!/usr/bin/env python
"""
Name: credentials.py
Description:

Print Ansible Vault credentials.
"""
import argparse
import logging
import sys

from ndfc_python.ansible_vault_credentials import AnsibleVaultCredentials
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
    avc = AnsibleVaultCredentials()
    avc.ansible_vault = args.ansible_vault
    avc.commit()
except ValueError as error:
    msg = f"{error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

print(f"domain {avc.nd_domain}")
print(f"username {avc.username}")
print(f"password {avc.password}")
print(f"ndfc_ip {avc.ndfc_ip}")
