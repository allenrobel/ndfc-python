#!/usr/bin/env python

from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials

log = Log('ndfc_log', 'INFO', 'DEBUG')

nc = NdfcCredentials()

ndfc = NDFC(log)
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip = nc.ndfc_ip
ndfc.login()

print('ndfc_token {}'.format(ndfc.auth_token))
