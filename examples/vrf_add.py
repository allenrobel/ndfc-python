#!/usr/bin/env python3
"""
Name: example_ndfc_vrf_add.py
Description: Add a vrf to a fabric
"""
import logging
import sys

from ndfc_python.log_v2 import Log
from ndfc_python.ndfc import NDFC, NdfcRequestError
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_vrf import NdfcVrf

try:
    log = Log()
    log.commit()
except ValueError as error:
    msg = "Error while instantiating Log(). "
    msg += f"Error detail: {error}"
    print(msg)
    sys.exit(1)

log = logging.getLogger("ndfc_python.main")

nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

try:
    instance = NdfcVrf()
    instance.ndfc = ndfc
    instance.display_name = "MyVrf"
    instance.fabric = "f1"
    instance.vrf_id = 50055
    instance.vrf_name = "MyVrf"
    instance.vrf_vlan_id = 2006
    instance.post()
except (NdfcRequestError, ValueError) as error:
    msg = "Error creating vrf. "
    msg += f"Error detail: {error}"
    log.error(msg)
