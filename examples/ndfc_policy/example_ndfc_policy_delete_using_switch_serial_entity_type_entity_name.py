#!/usr/bin/env python3
"""
Name: example_ndfc_policy_delete_using_switch_serial_entity_type_entity_name.py
Description: Delete policies matching switch serial number, entity type, entity name
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_policy import NdfcPolicy

nc = NdfcCredentials()
ndfc = NDFC(log("ndfc_policy_delete_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcPolicy(ndfc)
instance.serial_number = "FDO2443096H"
instance.entity_type = "INTERFACE"
instance.entity_name = "loopback1"
instance.delete()
