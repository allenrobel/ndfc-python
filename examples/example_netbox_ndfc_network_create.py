#!/usr/bin/env python3
"""
Name: example_netbox_ndfc_network_create.py
Description:

Read networks from a Netbox instance, and create these in NDFC.  This is a
proof-of-concept for one way to integrate NDFC and Netbox.

Netbox info:

https://docs.netbox.dev
https://github.com/netbox-community/netbox

NOTES: 

1. This example depends on the netbox-tools library which can be found here:

https://github.com/allenrobel/netbox-tools

2. You'll be asked for the Ansible Vault password twice.  Once for access
to the NDFC controller and once for access to your Netbox instance.
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_network import NdfcNetwork
from netbox_tools.common import netbox

nc = NdfcCredentials()
ndfc = NDFC(log("ndfc_network_create_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

netbox_obj = netbox()
netbox_vlans = netbox_obj.ipam.vlans.all()

for vlan in netbox_vlans:
    ndfc_network = NdfcNetwork(ndfc)
    ndfc_network.fabric = "MSD"
    ndfc_network.network_id = vlan.vid + 10000
    ndfc_network.vlan_id = vlan.vid
    ndfc_network.vrf = "foo_vrf"
    if ndfc_network.network_id_exists_in_fabric() is True:
        message = (
            f"Skipping. network_id {ndfc_network.network_id} already exists"
            f" in fabric {ndfc_network.fabric}"
        )
        ndfc.log.info(message)
        continue
    message = (
        f"Creating network {ndfc_network.vlan_id} ID {ndfc_network.network_id}"
        f" in vrf {ndfc_network.vrf}, fabric {ndfc_network.fabric}"
    )
    ndfc.log.info(message)
    ndfc_network.create()
