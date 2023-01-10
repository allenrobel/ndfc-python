#!/usr/bin/env python3

from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_network import NdfcNetwork
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log('vrf_log', 'INFO', 'DEBUG')
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip = nc.ndfc_ip
ndfc.login()

instance = NdfcNetwork(ndfc)
instance.fabric = 'MSD'
instance.networkName = 'MyNetwork_30005'
instance.delete()
