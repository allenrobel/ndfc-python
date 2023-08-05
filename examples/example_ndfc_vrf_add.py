#!/usr/bin/env python3
"""
Name: example_ndfc_vrf_add.py
Description: Add a vrf to a fabric
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_vrf import NdfcVrf

logger = log("ndfc_vrf_add_log", "INFO", "DEBUG")
nc = NdfcCredentials()

ndfc = NDFC()
ndfc.logger = logger
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcVrf()
instance.logger = logger
instance.ndfc = ndfc
instance.display_name = "foo_vrf"
instance.fabric = "easy"
instance.vrf_id = 50055
instance.vrf_name = "foo_vrf"
instance.vrf_vlan_id = 2006
instance.post()
