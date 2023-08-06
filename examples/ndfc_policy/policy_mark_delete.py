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
logger = log("ndfc_policy_create_log", "INFO", "DEBUG")
ndfc = NDFC()
ndfc.logger = logger
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
    msg = f"error: {err}"
    ndfc.logger.error(msg)
    sys.exit(1)
ndfc.logger.info(ndfc.response.text)
