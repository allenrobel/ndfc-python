#!/usr/bin/env python3
"""
Name: example_ndfc_network_delete.py
Description: Delete an NDFC network
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_network import NdfcNetwork

logger = log("ndfc_network_delete_log", "INFO", "DEBUG")
nc = NdfcCredentials()

ndfc = NDFC()
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

instance = NdfcNetwork()
instance.logger = logger
instance.ndfc = ndfc
instance.fabric = "easy"
instance.network_name = "MyNet"
instance.delete()
