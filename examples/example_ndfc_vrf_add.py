#!/usr/bin/env python3
"""
Name: example_ndfc_vrf_add.py
Description: Add a vrf to a fabric
"""
from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_vrf import NdfcVrf
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()
ndfc = NDFC(log("ndfc_vrf_add_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcVrf(ndfc)
instance.display_name = "foo_vrf"
instance.fabric = "MSD"
instance.vrf_id = 50055
instance.vrf_name = "foo_vrf"
instance.vrf_vlan_id = 2000
instance.post()
