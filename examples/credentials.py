#!/usr/bin/env python
"""
# Name

credentials.py

## Description

Print the credentials that would be used from the hierarchy of credential
sources that ndfc-python traverses.

For details about ndfc-python's credentials hierarchy and precedence, see:

https://allenrobel.github.io/ndfc-python/setup/set-credentials/

## Usage

Below, the NXOS_USERNAME environment variable is set, so its value
is used unless overridden by the command line.

```bash
(.venv) AROBEL-M-G793% export NXOS_USERNAME=admin
(.venv) AROBEL-M-G793% ./credentials.py \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password foo \
    --nd-username admin \
    --nxos-password bar
The following credentials would be used:
  nd_domain local
  nd_ip4 10.1.1.1
  nd_password foo
  nd_username admin
  nxos_password bar
  nxos_username admin
```

Below, we override the NXOS_USERNAME environment variable with its
corresponding command line argument:

```bash
(.venv) AROBEL-M-G793% export NXOS_USERNAME=admin
(.venv) AROBEL-M-G793% ./credentials.py \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password foo \
    --nd-username admin \
    --nxos-password bar \
    --nxos-username beeblebrox
The following credentials would be used:
  nd_domain local
  nd_ip4 10.1.1.1
  nd_password foo
  nd_username admin
  nxos_password bar
  nxos_username beeblebrox
```

Below, we unset NXOS_USERNAME and point to an Ansible vault file
which contains all the credentials.  The Ansible vault file is
the lowest precedence source of credentials but, since we haven't
specified any command-line credentials, and no environment variables
are set, the Ansible vault file is used.

```bash
(.venv) AROBEL-M-G793% unset NXOS_USERNAME
(.venv) AROBEL-M-G793% ./credentials.py --ansible-vault $HOME/.ansible/vault
Vault password:
The following credentials would be used:
  nd_domain local
  nd_ip4 172.22.150.244
  nd_password FooPassword
  nd_username admin
  nxos_password BarPassword
  nxos_username admin
(.venv) AROBEL-M-G793%```

"""
# pylint: disable=duplicate-code
import argparse
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.parsers.parser_nxos_password import parser_nxos_password
from ndfc_python.parsers.parser_nxos_username import parser_nxos_username


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
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
            parser_nxos_password,
            parser_nxos_username,
            parser_loglevel,
        ],
        description="DESCRIPTION: Print information about one or more switches.",
    )
    return parser.parse_args()


args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

try:
    ndfc_sender = NdfcPythonSender()
    ndfc_sender.args = args
    # Do not login, we're just printing credentials
    ndfc_sender.login = False
    ndfc_sender.commit()
except ValueError as error:
    msg = f"Exiting.  Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

print("The following credentials would be used:")
print(f"  nd_domain {ndfc_sender.nd_domain}")
print(f"  nd_ip4 {ndfc_sender.nd_ip4}")
print(f"  nd_password {ndfc_sender.nd_password}")
print(f"  nd_username {ndfc_sender.nd_username}")
print(f"  nxos_password {ndfc_sender.nxos_password}")
print(f"  nxos_username {ndfc_sender.nxos_username}")
