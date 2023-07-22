#!/usr/bin/env python3
"""
Name: example_ndfc_policy_mark_delete.py
Description: Mark switch policies for deletion matching SWITCH_SERIAL,
ENTITY_TYPE, and ENTITY_NAME
"""
import sys
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC, NdfcRequestError
from ndfc_python.ndfc_credentials import NdfcCredentials

SWITCH_SERIAL = "FDO2443096H"
ENTITY_TYPE = "INTERFACE"
ENTITY_NAME = "loopback1"

nc = NdfcCredentials()
ndfc = NDFC(log("ndfc_policy_mark_delete", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

url = f"{ndfc.url_control_policies_switches}"
url += f"/{SWITCH_SERIAL}/{ENTITY_TYPE}/{ENTITY_NAME}"

headers = {"Authorization": f"{ndfc.bearer_token}"}

try:
    ndfc.put(url, headers)
except NdfcRequestError as err:
    ndfc.log.error(f"error: {err}")
    sys.exit(1)
ndfc.log.info(ndfc.response.text)
