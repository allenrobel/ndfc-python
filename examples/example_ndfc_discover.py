#!/usr/bin/env python3
"""
Description:

Discover switch
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_discover import NdfcDiscover
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

ndfc = NDFC(log("ndfc_discover_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

discover = NdfcDiscover(ndfc)
discover.fabric_name = "Easy_Fabric_1"
discover.cdpSecondTimeout = 5
discover.maxHops = 0
discover.username = nc.discover_username
discover.password = nc.discover_password
discover.preserveConfig = False
seedIps = ["10.1.1.1"]
for seedIp in seedIps:
    discover.seedIP = seedIp
    discover.discover()
    print(f"discover_status_code {discover.discover_status_code}")
    print(f"discover_response {discover.discover_response}")
