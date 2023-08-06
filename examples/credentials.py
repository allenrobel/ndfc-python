#!/usr/bin/env python
"""
Name: example_ndfc_credentials.py
Description:

Print the user's credentials after asking for their ansible vault password
"""
from ndfc_python.ndfc_credentials import NdfcCredentials

nc = NdfcCredentials()

print(f"username {nc.username}")
print(f"password {nc.password}")
print(f"ndfc_ip {nc.ndfc_ip}")
