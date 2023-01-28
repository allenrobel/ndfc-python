#!/usr/bin/env python3
"""
Name: example_ndfc_network_create.py
Description: Create an NDFC network
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_network import NdfcNetwork
from ndfc_python.ndfc_credentials import NdfcCredentials
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
        print(f"Skipping. network_id {ndfc_network.network_id} already exists.")
        continue
    ndfc_network.create()
