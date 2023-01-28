#!/usr/bin/env python3
"""
Name: example_ndfc_policy_delete_using_policy_ids.py
Description: Delete policies matching policy IDs
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
instance.policy_ids = ["POLICY-1178200"]
instance.delete()
