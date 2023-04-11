#!/usr/bin/env python3
"""
Description:

Check if switch is up and manageable
"""
from time import sleep
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_discover import NdfcDiscover
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_fabric import NdfcFabric

nc = NdfcCredentials()

ndfc = NDFC(log("ndfc_discover_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

discover = NdfcDiscover(ndfc)
discover.fabric_name = "Easy_Fabric_1"
discover.seedIP = "10.1.1.1"
retries = 4
up = False
while up == False and retries > 0:
    up = discover.is_up()
    retries -= 1
    if up is not True:
        sleep(10)
fabric = NdfcFabric(ndfc)
fabric.fabric_name = discover.fabric_name
fabric.config_save()
