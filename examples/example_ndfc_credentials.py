#!/usr/bin/env python

from ndfc_lib.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

print('username {}'.format(nc.username))
print('password {}'.format(nc.password))
print('ndfc_ip {}'.format(nc.ndfc_ip))
