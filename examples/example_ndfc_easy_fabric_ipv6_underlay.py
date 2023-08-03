#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric_ipv6_underlay.py
Description: Create a fabric configured with an IPv6 underlay
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
instance.fabric_name = "IPv6_EasyFabric"
instance.bgp_as = 65001
instance.underlay_is_v6 = True
instance.use_link_local = False
# all of the following are mandatory when underlay_is_v6 is set to True
instance.anycast_lb_id = 123
instance.router_id_range = "10.1.1.0/24"
instance.loopback0_ipv6_range = "fd00::a02:0/119"
instance.loopback1_ipv6_range = "fd00::a03:0/118"
instance.v6_subnet_range = "fd00::a04:0/112"
instance.v6_subnet_target_mask = 126
instance.create()
