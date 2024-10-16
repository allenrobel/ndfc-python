#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric_with_syslog.py
Description: Create a fabric with syslog configured
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
instance.fabric_name = "easy_syslog"
instance.bgp_as = 65001
# configure one v4 and one v6 syslog server
instance.syslog_server_ip_list = ["10.1.1.1", "2001::1"]
# syslog_server_vrf
# Below we imply that each server in syslog_server_ip_list
# lives in a separate VRF (10.1.1.1 lives in VRF management,
# and 2001::1 lives in VRF MyVrf).  If, instead, both servers
# live in the same VRF, you can include a single item in
# syslog_server_vrf, which would be associated with all syslog
# servers defined in syslog_server_ip_list.
instance.syslog_server_vrf = ["management", "myVrf"]
# Per-server syslog severity level.  This list must contain the same
# number of elements as syslog_server_ip_list. Severity levels range
# from 0 to 7.  Below, we assign severity level 7 to server 10.1.1.1,
# and severity level 0 to 2001::1
instance.syslog_sev = [7, 0]
instance.dci_subnet_range = "10.22.0.0/16"
instance.loopback0_ip_range = "10.23.0.0/16"
instance.loopback1_ip_range = "10.24.0.0/16"
instance.create()
