#!/usr/bin/env python3
"""
Name: device_info.py
Description:

Retrieve various information about devices, given their
fabric_name and ip_address.

Usage:

Edit the vars below to match your setup
    - fabric
    - devices
"""
import sys

from ndfc_python.log_v2 import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_device_info import NdfcDeviceInfo

try:
    log = Log()
    log.commit()
except ValueError as error:
    MSG = "Error while instantiating Log(). "
    MSG += f"Error detail: {error}"
    print(MSG)
    sys.exit(1)

FABRIC = "f1"
DEVICES = ["10.1.1.1", "10.1.1.2"]

nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

instance = NdfcDeviceInfo()
instance.ndfc = ndfc
instance.fabric_name = FABRIC
for ipv4 in DEVICES:
    instance.ip_address = ipv4
    instance.refresh()
    print(f"device: {instance.ip_address}")
    print(f"fabric: {instance.fabric_name}")
    print(f"   name: {instance.logical_name}")
    print(f"   role: {instance.switch_role}")
    print(f"   db_id: {instance.switch_db_id}")
    print(f"   serial_number: {instance.serial_number}")
    print(f"   model: {instance.model}")
    print(f"   release: {instance.release}")
    print(f"   status: {instance.status}")
    print(f"   oper_status: {instance.oper_status}")
