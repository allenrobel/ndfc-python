#!/usr/bin/env python3
'''
Description:

Test for switch reachability (from NDFC perspective)
'''
from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_reachability import NdfcReachability
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log('ndfc_reachability', 'INFO', 'DEBUG')
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcReachability(ndfc)
instance.seedIP = '192.168.1.110'
instance.fabric = 'f1'
instance.cdpSecondTimeout = 5
instance.username = nc.discover_username
instance.password = nc.discover_password
instance.reachability()
print('status_code {}'.format(instance.status_code))
print('response {}'.format(instance.response))
