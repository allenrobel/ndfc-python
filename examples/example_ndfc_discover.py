#!/usr/bin/env python3
'''
Description:

Discover switch
'''
from ndfc_lib.log import Log
from ndfc_lib.ndfc import NDFC
from ndfc_lib.ndfc_discover import NdfcDiscover
from ndfc_lib.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log('vrf_log', 'INFO', 'DEBUG')
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip = nc.ndfc_ip
ndfc.login()

instance = NdfcDiscover(ndfc)
instance.seedIP = '172.22.150.115'
instance.fabric = 'f2'
instance.cdpSecondTimeout = 5
instance.username = nc.discover_username
instance.password = nc.discover_password
instance.preserveConfig = False
instance.discover()
print('discover_status_code {}'.format(instance.discover_status_code))
print('discover_response {}'.format(instance.discover_response))
