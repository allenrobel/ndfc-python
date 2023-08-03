#!/usr/bin/env python3
"""
Description:

Check if switch is up and manageable.  If so, call config_save on the fabric.
"""
import sys
from time import sleep

from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_discover import NdfcDiscover
from ndfc_python.ndfc_fabric import NdfcFabric

nc = NdfcCredentials()

ndfc = NDFC(log("ndfc_discover_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcDiscover(ndfc)
instance.fabric_name = "ext1"
instance.seed_ip = "10.1.1.1"
instance.discover_password = nc.discover_password
instance.discover_username = nc.discover_username
retries = 4
up = False
while up is False and retries > 0:
    try:
        up = instance.is_up()
    except ValueError as err:
        ndfc.log.error(f"exiting. {err}")
        sys.exit(1)
    retries -= 1
    if up is not True:
        sleep(10)
if up is not True:
    ndfc.log.info(f"switch {instance.seed_ip} is not up.")
    sys.exit(0)

fabric = NdfcFabric(ndfc)
fabric.fabric_name = instance.fabric_name
fabric.config_save()
