#!/usr/bin/env python
"""
Name: example_ndfc_login.py
Description:

Login to an NDFC controller and print the returned auth token.

Usage:

1. Set the following environment variables appropriately for your setup:

export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
export NDFC_PYTHON_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/config/config.yml

2. Edit the YAML file pointed to by NDFC_PYTHON_CONFIG to contain at least:

---
ansible_vault: "/path/to/your/ansible/vault"

"""
from ndfc_python.log_v2 import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials

try:
    log = Log()
    log.commit()
except ValueError as error:
    MSG = "Error while instantiating Log(). "
    MSG += f"Error detail: {error}"
    print(MSG)

nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

print(f"ndfc_token {ndfc.auth_token}")
