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

logger = log("ndfc_discover_log", "INFO", "DEBUG")
nc = NdfcCredentials()

ndfc = NDFC()
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

instance = NdfcDiscover()
instance.logger = logger
instance.ndfc = ndfc
instance.fabric_name = "easy"
instance.seed_ip = "10.1.1.1"
instance.discover_password = nc.discover_password
instance.discover_username = nc.discover_username
retries = 4
up = False
while up is False and retries > 0:
    try:
        up = instance.is_up()
    except ValueError as err:
        msg = f"exiting. {err}"
        logger.error(msg)
        sys.exit(1)
    retries -= 1
    if up is not True:
        sleep(10)
if up is not True:
    msg = f"switch {instance.seed_ip} is not up."
    instance.logger.info(msg)
    sys.exit(0)

fabric = NdfcFabric()
fabric.logger = logger
fabric.ndfc = ndfc
fabric.fabric_name = instance.fabric_name
fabric.config_save()
