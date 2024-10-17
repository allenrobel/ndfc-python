#!/usr/bin/env python3
"""
Name: example_ndfc_discover.py
Description: Discover device
"""
import sys

from ndfc_python.log_v2 import Log
from ndfc_python.ndfc import NDFC, NdfcRequestError
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_discover import NdfcDiscover

fabric_name = "MyFabric"
seed_ips = ["10.1.1.1"]

try:
    log = Log()
    log.commit()
except ValueError as error:
    MSG = "Error while instantiating Log(). "
    MSG += f"Error detail: {error}"
    print(MSG)
    sys.exit(1)

nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

instance = NdfcDiscover()
instance.ndfc = ndfc
instance.fabric_name = fabric_name
instance.cdp_second_timeout = 5
instance.max_hops = 0
instance.discover_username = nc.discover_username
instance.discover_password = nc.discover_password
instance.preserve_config = True
for seed_ip in seed_ips:
    instance.seed_ip = seed_ip
    try:
        instance.discover()
    except (NdfcRequestError, ValueError) as error:
        msg = f"exiting. {error}"
        raise ValueError(msg) from error
    print(f"discover_status_code {instance.discover_status_code}")
    print(f"discover_response {instance.discover_response}")
