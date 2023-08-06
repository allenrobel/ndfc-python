#!/usr/bin/env python3
"""
Name: example_ndfc_network_create.py
Description: Create an NDFC network
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC, NdfcRequestError
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_network import NdfcNetwork

logger = log("ndfc_network_create_log", "INFO", "DEBUG")
nc = NdfcCredentials()

ndfc = NDFC()
ndfc.logger = logger
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcNetwork()
instance.logger = logger
instance.ndfc = ndfc
instance.fabric = "easy"
instance.network_name = "MyNet"
instance.enable_ir = True
instance.gateway_ip_address = "10.1.1.1/24"
instance.network_id = 30005
instance.vlan_id = 3005
instance.vrf = "MyVrf"
try:
    instance.create()
except NdfcRequestError as err:
    msg = f"exiting {err}"
    instance.logger.error(msg)
