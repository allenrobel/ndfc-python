#!/usr/bin/env python3

from ndfc_lib.log import Log
from ndfc_lib.ndfc import NDFC
from ndfc_lib.ndfc_network import NdfcNetwork
from ndfc_lib.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log('vrf_log', 'INFO', 'DEBUG')
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip = nc.ndfc_ip
ndfc.login()

instance = NdfcNetwork(ndfc)
instance.fabric = 'foo'
instance.networkId = 30000
instance.vlanId = 3000
instance.vrf = 'foo_vrf'
instance.create()
