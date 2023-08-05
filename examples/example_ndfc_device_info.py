#!/usr/bin/env python3
"""
Name: example_ndfc_device_info.py
Description:

Retrieve various information about a device, given its
fabric_name and ip_address
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_device_info import NdfcDeviceInfo

nc = NdfcCredentials()

logger = log("ndfc_device_info", "INFO", "DEBUG")
ndfc = NDFC()
ndfc.logger = logger
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcDeviceInfo()
instance.ndfc = ndfc
instance.logger = logger
instance.fabric_name = "easy"
for ipv4 in ["172.22.150.102", "172.22.150.103"]:
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
