#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric.py
Description: Create a fabric with AAA enabled
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_easy_fabric import NdfcEasyFabric

nc = NdfcCredentials()

logger = log("ndfc_easy_fabric_log", "INFO", "DEBUG")

ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

instance = NdfcEasyFabric()
instance.ndfc = ndfc
instance.logger = logger
instance.fabric_name = "AAA_Python"
instance.bgp_as = 1
instance.aaa_remote_ip_enabled = True
instance.bootstrap_enable = True
instance.enable_aaa = True
instance.aaa_server_conf = "aaa group server radius RADIUS"
"""
snmp-server aaa-user cache-timeout 3600
no snmp-server disable snmp-aaa sync
no snmp-server enable traps aaa server-state-change
aaa authentication login default local
aaa authorization ssh-publickey default local
aaa authorization ssh-certificate default local
aaa accounting default local
aaa user default-role
aaa authentication login default fallback error local
aaa authentication login console fallback error local
no aaa authentication login invalid-username-log
no aaa authentication login error-enable
no aaa authentication login mschap enable
no aaa authentication login mschapv2 enable
no aaa authentication login chap enable
no aaa authentication login ascii-authentication
"""
instance.create()
