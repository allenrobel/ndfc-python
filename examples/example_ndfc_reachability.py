#!/usr/bin/env python3
"""
Description:

Test for switch reachability (from NDFC perspective)
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_reachability import NdfcReachability

logger = log("ndfc_reachability_log", "INFO", "DEBUG")
nc = NdfcCredentials()
ndfc = NDFC()
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

instance = NdfcReachability()
instance.logger = logger
instance.ndfc = ndfc
instance.seed_ip = "172.22.150.113"
instance.fabric_name = "easy"
# for EasyFabric, if overlay_mode is "config-profile"
# it's recommended that preserve_config is set to False
instance.preserve_config = False
instance.max_hops = 0
#instance.cdp_second_timeout = 5
instance.username = nc.discover_username
instance.password = nc.discover_password
instance.reachability()
print(f"status_code {instance.status_code}")
print(f"response {instance.response}")
print(f"sysName: {instance.response[0]['sysName']}")
print(f"serialNumber: {instance.response[0]['serialNumber']}")

print(f"Reachable: {instance.response[0]['reachable']}")
print(f"Known: {instance.response[0]['known']}")
print(f"Valid: {instance.response[0]['valid']}")
