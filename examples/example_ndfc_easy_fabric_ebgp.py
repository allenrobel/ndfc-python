#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric_ebgp.py
Description: Create an eBGP-based fabric
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_easy_fabric_ebgp import NdfcEasyFabricEbgp

nc = NdfcCredentials()
logger = log("ndfc_easy_fabric_ebgp_log", "INFO", "DEBUG")
ndfc = NDFC()
ndfc.logger = logger
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcEasyFabricEbgp()
instance.logger = logger
instance.ndfc = ndfc
instance.fabric_name = "Easy_Fabric_EBGP_1"
instance.bgp_as = 65222
# instance.subnet_range = "10.10.0.0/16"
# instance.dci_subnet_range = "10.33.0.0/16"
# instance.loopback0_ip_range = "10.11.0.0/16"
# instance.loopback1_ip_range = "10.12.0.0/16"
instance.create()
