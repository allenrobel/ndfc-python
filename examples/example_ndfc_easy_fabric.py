#!/usr/bin/env python3
"""
Name: example_ndfc_fabric_site.py
Description: Create a site/child fabric using NdfcEasyFabric()
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_easy_fabric import NdfcEasyFabric
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

ndfc = NDFC(log("ndfc_easy_fabric_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcEasyFabric(ndfc)
instance.fabric_name = "foo"
instance.bgp_as = 65111
instance.replication_mode = "Ingress"
instance.subnet_range = "10.10.0.0/16"
instance.dci_subnet_range = "10.33.0.0/16"
instance.loopback0_ip_range = "10.11.0.0/16"
instance.loopback1_ip_range = "10.12.0.0/16"
instance.create()
