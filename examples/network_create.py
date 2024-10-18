#!/usr/bin/env python3
"""
Name: example_ndfc_network_create.py
Description: Create an NDFC network

NOTES:

1.  Set the following environment variables before running this script
    (edit appropriately for your setup)

export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/netbox-tools/lib
export NDFC_PYTHON_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/config/config.yml

Optional, to enable logging:
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json

2. Edit the network values in the script below.
"""
import logging
import sys

from ndfc_python.log_v2 import Log
from ndfc_python.ndfc import NDFC, NdfcRequestError
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_network import NdfcNetwork

try:
    log = Log()
    log.commit()
except ValueError as error:
    MSG = "Error while instantiating Log(). "
    MSG += f"Error detail: {error}"
    print(MSG)
    sys.exit(1)

log = logging.getLogger("ndfc_python.main")

nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

try:
    instance = NdfcNetwork()
    instance.ndfc = ndfc
    instance.fabric = "f1"
    instance.network_name = "MyNet"
    instance.enable_ir = True
    instance.gateway_ip_address = "10.1.1.1/24"
    instance.network_id = 30005
    instance.vlan_id = 3005
    instance.vrf = "MyVrf"
    instance.create()
except (NdfcRequestError, ValueError) as error:
    msg = "Error creating network. "
    msg += f"Error detail: {error}"
    log.error(msg)
