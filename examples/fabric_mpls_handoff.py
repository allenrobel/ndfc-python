#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric_mpls_handoff.py
Description: Create a fabric configured with MPLS handoff
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_easy_fabric import NdfcEasyFabric

nc = NdfcCredentials()
logger = log("ndfc_easy_fabric_log", "INFO", "DEBUG")
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

instance = NdfcEasyFabric()
instance.logger = logger
instance.ndfc = ndfc
instance.fabric_name = "easy_mpls_handoff"
instance.bgp_as = 65001
instance.mpls_handoff = True
instance.mpls_lb_id = 101
instance.mpls_loopback_ip_range = "10.100.1.0/25"
instance.subnet_range = "10.20.0.0/16"
instance.dci_subnet_range = "10.22.0.0/16"
instance.loopback0_ip_range = "10.23.0.0/16"
instance.loopback1_ip_range = "10.24.0.0/16"
instance.create()
