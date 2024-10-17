#!/usr/bin/env python3
"""
Name: example_ndfc_network_create.py
Description: Create an NDFC network
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
