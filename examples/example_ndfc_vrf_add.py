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

vrf = NdfcVrf(ndfc)
vrf.displayName = 'foo_vrf'
vrf.fabric = 'foo'
vrf.vrfId = 50055
vrf.vrfName = 'foo_vrf'
vrf.vrfVlanId = 2000
vrf.post()
