#!/usr/bin/env python3

from ndfc_lib.log import Log
from ndfc_lib.ndfc import NDFC
from ndfc_lib.ndfc_vrf import NdfcVrf
from ndfc_lib.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

log = Log('vrf_log', 'INFO', 'DEBUG')
ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip = nc.ndfc_ip
ndfc.login()

instance = NdfcVrf(ndfc)
instance.displayName = 'foo_vrf'
instance.fabric = 'foo'
instance.vrfId = 50055
instance.vrfName = 'foo_vrf'
instance.vrfVlanId = 2000
instance.post()
