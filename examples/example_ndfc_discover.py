#!/usr/bin/env python3
"""
Description:

Discover switch
"""
import sys

from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_discover import NdfcDiscover

nc = NdfcCredentials()

ndfc = NDFC(log("ndfc_discover_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcDiscover(ndfc)
instance.fabric_name = "ext1"
instance.cdp_second_timeout = 5
instance.max_hops = 0
instance.discover_username = nc.discover_username
instance.discover_password = nc.discover_password
instance.preserve_config = True
seedIps = ["172.22.150.102"]
for seedIp in seedIps:
    instance.seed_ip = seedIp
    try:
        instance.discover()
    except ValueError as err:
        ndfc.log.error(f"exiting. {err}")
        sys.exit(1)
    print(f"discover_status_code {instance.discover_status_code}")
    print(f"discover_response {instance.discover_response}")
