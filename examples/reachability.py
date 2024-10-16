#!/usr/bin/env python3
"""
Name: example_ndfc_reachability.py
Description:

Test for device reachability (from NDFC perspective)
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_reachability import NdfcReachability

logger = log("ndfc_reachability_log", "INFO", "DEBUG")
nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

instance = NdfcReachability()
instance.logger = logger
instance.ndfc = ndfc
instance.seed_ip = "10.1.1.2"
instance.fabric_name = "easy"

# For EasyFabric, if overlay_mode is "config-profile" (the default),
# it's recommended that preserve_config be set to False.  If it's
# desired to preserve the config, then set overlay_mode to "cli"
# and set preserve_config to True.
# instance.overlay_mode = "cli"
instance.preserve_config = False

instance.max_hops = 0
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
