#!/usr/bin/env python
"""
Name: example_ndfc_credentials.py
Description:

Print the user's credentials after asking for their ansible vault password
"""
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

print("username {nc.username}")
print("password {nc.password}")
print("ndfc_ip {nc.ndfc_ip}")
