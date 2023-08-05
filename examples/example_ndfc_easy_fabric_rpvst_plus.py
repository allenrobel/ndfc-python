#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric_rpvst_plus.py
Description: Create a fabric with rpvst+ spanning-tree root option
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_easy_fabric import NdfcEasyFabric

nc = NdfcCredentials()
logger = log("ndfc_easy_fabric_log", "INFO", "DEBUG")
ndfc = NDFC()
ndfc.logger = logger
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcEasyFabric()
instance.logger = logger
instance.ndfc = ndfc
instance.fabric_name = "easy_rpvst_plus"
instance.bgp_as = 65001
instance.stp_root_option = "rpvst+"
instance.stp_vlan_range = ["1-3967"]
instance.subnet_range = "10.20.0.0/16"
instance.dci_subnet_range = "10.22.0.0/16"
instance.loopback0_ip_range = "10.23.0.0/16"
instance.loopback1_ip_range = "10.24.0.0/16"
instance.create()
