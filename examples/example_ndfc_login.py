#!/usr/bin/env python
"""
Name: example_ndfc_login.py
Description:

Login to an NDFC controller and print the returned auth token.
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()
ndfc = NDFC(log("ndfc_login_log", "INFO", "DEBUG"))
ndfc.ip4 = nc.ndfc_ip
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.login()

print(f"ndfc_token {ndfc.auth_token}")
