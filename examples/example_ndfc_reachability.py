#!/usr/bin/env python3
"""
Description:

Test for switch reachability (from NDFC perspective)
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_reachability import NdfcReachability

nc = NdfcCredentials()
ndfc = NDFC(log("ndfc_reachability_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcReachability(ndfc)
instance.seed_ip = "10.1.1.1"
instance.fabric_name = "f1"
instance.max_hops = 1
instance.cdp_second_timeout = 5
# Note: NdfcReachability() populates username and password
# from the passed ndfc instance.  But, you can override these
# values with the following properties if need be.
# instance.username = nc.discover_username
# instance.password = nc.discover_password
instance.reachability()
print(f"status_code {instance.status_code}")
print(f"response {instance.response}")
print(f"sysName: {instance.response[0]['sysName']}")
print(f"serialNumber: {instance.response[0]['serialNumber']}")

print(f"Reachable: {instance.response[0]['reachable']}")
print(f"Known: {instance.response[0]['known']}")
print(f"Valid: {instance.response[0]['valid']}")
