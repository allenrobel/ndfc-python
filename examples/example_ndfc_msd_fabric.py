#!/usr/bin/env python3
"""
Name: example_ndfc_msd_fabric.py
Description: Create a multi-site domain (MSD) fabric
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_msd_fabric import NdfcMsdFabric

nc = NdfcCredentials()
logger = log("ndfc_msd_fabric_log", "INFO", "DEBUG")

ndfc = NDFC()
ndfc.logger = logger
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcMsdFabric()
instance.logger = logger
instance.ndfc = ndfc
instance.fabric_name = "msd_1"

# This defaults to 10.10.0.0/24.
# We change it to avoid overlap with an existing range
instance.loopback100_ip_range = "10.100.0.0/24"

# This defaults to "Manual"
# We change it since we want these auto-provisioned
# Valid values:
# "Manual"
# "Centralized_To_Route_Server"
# "Direct_To_BGWS"
instance.border_gwy_connections = "Centralized_To_Route_Server"

# Centralized_To_Route_Server requires two additional
# mandatory parameters
# - bgp_rp_asn
# - rp_server_ip
# Python list of route-server ASN numbers. List length must
# match bgp_rp_server_ip
instance.bgp_rp_asn = [65001, 65001]

# Python list of route-server IP addresses. List length must
# match bgp_rp_asn
instance.rp_server_ip = ["1.1.1.1", "1.1.1.2"]

# This defaults to 10.10.1.0/24.
# We change it to avoid overlap with an existing range
instance.dci_subnet_range = "10.101.1.0/24"
instance.create()
