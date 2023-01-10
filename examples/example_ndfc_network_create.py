#!/usr/bin/env python3
"""
Name: example_ndfc_network_create.py
Description: Create an NDFC network
"""
from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_network import NdfcNetwork
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log("ndfc_network_create_log", "INFO", "DEBUG")
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip = nc.ndfc_ip
ndfc.login()

instance = NdfcNetwork(ndfc)
instance.fabric = "MSD"
instance.network_id = 30005
instance.vlan_id = 3005
instance.vrf = "foo_vrf"
instance.create()
