#!/usr/bin/env python3
"""
Name: example_ndfc_network_delete.py
Description: Delete an NDFC network
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_network import NdfcNetwork
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

ndfc = NDFC(log("ndfc_network_delete_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcNetwork(ndfc)
instance.fabric = "MSD"
instance.network_name = "MyNetwork_30005"
instance.delete()
