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
logger = log("ndfc_login_log", "INFO", "DEBUG")

ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

print(f"ndfc_token {ndfc.auth_token}")
