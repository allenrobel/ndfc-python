#!/usr/bin/env python3
'''
Description:

Create a site/child fabric using NdfcFabricSite()
'''
from ndfc_lib.log import Log
from ndfc_lib.ndfc import NDFC
from ndfc_lib.ndfc_fabric_site import NdfcFabricSite
from ndfc_lib.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log('vrf_log', 'INFO', 'DEBUG')
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip = nc.ndfc_ip
ndfc.login()

instance = NdfcFabricSite(ndfc)
instance.fabric = 'f2'
instance.BGP_AS = 65002
instance.REPLICATION_MODE = 'Ingress'
instance.create()
