#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric.py
Description: Create a fabric using NdfcEasyFabric()
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_easy_fabric import NdfcEasyFabric

nc = NdfcCredentials()

ndfc = NDFC(log("ndfc_easy_fabric_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcEasyFabric(ndfc)
instance.fabric_name = "easy2"
instance.bgp_as = 65001
instance.mpls_handoff = True
instance.mpls_lb_id = 101
instance.mpls_loopback_ip_range = "10.100.1.0/25"
instance.subnet_range = "10.20.0.0/16"
instance.dci_subnet_range = "10.22.0.0/16"
instance.loopback0_ip_range = "10.23.0.0/16"
instance.loopback1_ip_range = "10.24.0.0/16"
instance.create()
