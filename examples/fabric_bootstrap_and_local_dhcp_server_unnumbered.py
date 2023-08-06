#!/usr/bin/env python3
"""
Name: example_ndfc_easy_fabric_bootstrap_and_local_dhcp_server_unnumbered.py

Description:
Create a fabric with unnumbered fabric interfaces, configured with
inband management, local (NDFC) DHCP server, and bootstrap enabled

NOTES:

1. If you encounter the following error in the fabric's Event Analytics:

"Inband Management is supported with 'LAN Device Management Connectivity'
Server Setting set to 'Data' only. Please update the setting and retry
the management mode change."

1a. Ensure that at least 2 "External Services IPs" are configured here:

Nexus Dashboard (Admin Console) -> Infrastructure -> Cluster Configuration
  -> General -> External Service Pools -> Data Service IPs -> Add IP Address

1b. Ensure you have configured a Data Network Route here:

Nexus Dashboard (Admin Console) -> Infrastructure -> Cluster Configuration
  -> General -> Routes -> Data Network Routes -> Add Data Network Routes

1c. Change the following setting from "Management" to "Data":

Fabric Controller -> Settings -> Server Settings ->
   Admin -> LAN Device Management Connectivity

IMPORTANT! The below addressing within the range 10.1.0.0/16
assumes that the Nexus Dashboard External Data Network has
been configured to 10.1.0.0/16.  Change these script
addresses to align with your Nexus Dashboard configuration.
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_easy_fabric import NdfcEasyFabric

nc = NdfcCredentials()

logger = log("ndfc_easy_fabric_log", "INFO", "DEBUG")
ndfc = NDFC()
ndfc.logger = logger
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcEasyFabric()
instance.ndfc = ndfc
instance.logger = logger
instance.fabric_name = "unnumbered_fabric"
instance.bgp_as = 65001
instance.fabric_interface_type = "unnumbered"
instance.bootstrap_enable = True
instance.dhcp_enable = True
# dhcp_ipv6_enable pertains to both IPv4 and IPv6
# Unlike all other *_enable properties, this is
# not a boolean.
instance.dhcp_ipv6_enable = "DHCPv4"
instance.mgmt_gw = "10.1.1.1"
instance.mgmt_prefix = 24

# dhcp_end and dhcp_start must be within loopback0_ip_range below
instance.dhcp_end = "10.1.1.200"
instance.dhcp_start = "10.1.1.10"
instance.inband_mgmt = True
instance.seed_switch_core_interfaces = "Eth1/1-10"
instance.spine_switch_core_interfaces = "Eth1/1-10"

instance.unnum_bootstrap_lb_id = 1000
# unnum_dhcp_end - unnum_dhcp_start must be a subset
# of dhcp_end - dhcp_start
instance.unnum_dhcp_end = "10.1.1.50"
instance.unnum_dhcp_start = "10.1.1.10"

instance.subnet_range = "10.20.0.0/16"
instance.dci_subnet_range = "10.22.0.0/16"
instance.loopback0_ip_range = "10.1.0.0/16"
instance.loopback1_ip_range = "10.24.0.0/16"
instance.create()
