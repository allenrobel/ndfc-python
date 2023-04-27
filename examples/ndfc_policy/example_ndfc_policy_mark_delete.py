#!/usr/bin/env python3
"""
Name: example_ndfc_policy_mark_delete.py
Description: Mark switch policies for deletion matching switch serial, entity_type, entity_name
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials

switch_serial = "FDO2443096H"
entity_type = "INTERFACE"
entity_name = "loopback1"

nc = NdfcCredentials()
ndfc = NDFC(log("example_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()


url = (
    f"{ndfc.url_control_policies_switches}/{switch_serial}/{entity_type}/{entity_name}"
)
headers = {"Authorization": f"{ndfc.bearer_token}"}
payload = {}

response = ndfc.put(url, headers, payload)

ndfc.log.info(ndfc.response.text)
