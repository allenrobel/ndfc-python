#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric_bootstrap_and_local_dhcp_server.py
Description:
Create a fabric configured with DHCP server and with bootstrap enabled
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
instance.ndfc = ndfc
instance.logger = logger
instance.fabric_name = "easy_bootstrap"
instance.bgp_as = 65001
instance.bootstrap_enable = True
instance.dhcp_enable = True
# dhcp_ipv6_enable pertains to both IPv4 and IPv6
# Unlike all other *_enable properties, this is
# not a boolean.
instance.dhcp_ipv6_enable = "DHCPv4"
instance.mgmt_gw = "10.1.1.1"
instance.dhcp_start = "10.1.1.2"
instance.dhcp_end = "10.1.1.5"
instance.mgmt_gw = "10.1.1.1"
instance.mgmt_prefix = 24
instance.subnet_range = "10.20.0.0/16"
instance.dci_subnet_range = "10.22.0.0/16"
instance.loopback0_ip_range = "10.23.0.0/16"
instance.loopback1_ip_range = "10.24.0.0/16"
instance.create()
