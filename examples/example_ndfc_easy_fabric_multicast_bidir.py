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
instance.fabric_name = "bidir"
instance.bgp_as = 65001
instance.replication_mode = "Multicast"
# rp_mode: "asm" or "bidir"
# If rp_mode is "bidir", phantom_rp_lb_id must be set (see below)
instance.rp_mode = "bidir"
# rp_count can be either 2 or 4
instance.rp_count = 4
# if rp_count == 2 phantom_rp_lb_id[1-2] must be set
instance.phantom_rp_lb_id1 = 101
instance.phantom_rp_lb_id2 = 102
# if rp_count == 4, phantom_rp_lb_id[1-4] must be set
instance.phantom_rp_lb_id3 = 103
instance.phantom_rp_lb_id4 = 104
instance.subnet_range = "10.20.0.0/16"
instance.dci_subnet_range = "10.22.0.0/16"
instance.loopback0_ip_range = "10.23.0.0/16"
instance.loopback1_ip_range = "10.24.0.0/16"
instance.create()
