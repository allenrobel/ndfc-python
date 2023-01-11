#!/usr/bin/env python3
"""
Description:

Discover switch
"""
from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_discover import NdfcDiscover
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log("vrf_log", "INFO", "DEBUG")
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcDiscover(ndfc)
instance.fabric = "f1"
instance.cdpSecondTimeout = 5
instance.username = nc.discover_username
instance.password = nc.discover_password
instance.preserveConfig = False
seedIps = ["172.22.150.110", "172.22.150.111"]
for seedIp in seedIps:
    instance.seedIP = seedIp
    instance.discover()
    print(f"discover_status_code {instance.discover_status_code}")
    print(f"discover_response {instance.discover_response}")
