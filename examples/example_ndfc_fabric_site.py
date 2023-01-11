#!/usr/bin/env python3
"""
Name: example_ndfc_fabric_site.py
Description: Create a site/child fabric using NdfcFabricSite()
"""
from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_fabric_site import NdfcFabricSite
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log("vrf_log", "INFO", "DEBUG")
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcFabricSite(ndfc)
instance.fabric = "foo"
instance.bgp_as = 65003
instance.replication_mode = "Ingress"
instance.subnet_range = "10.10.0.0/16"
instance.dci_subnet_range = "10.33.0.0/16"
instance.loopback0_ip_range = "10.11.0.0/16"
instance.loopback1_ip_range = "10.12.0.0/16"
instance.create()
