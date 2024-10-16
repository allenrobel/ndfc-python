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

logger = log("netbox_ndfc_network_create_log", "INFO", "DEBUG")
nc = NdfcCredentials()

ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

netbox_obj = netbox()
netbox_vlans = netbox_obj.ipam.vlans.all()

for vlan in netbox_vlans:
    instance = NdfcNetwork()
    instance.logger = logger
    instance.ndfc = ndfc
    instance.fabric = "easy"
    instance.network_id = vlan.vid + 10000
    instance.vlan_id = vlan.vid
    instance.vrf = "MyVrf"
    if instance.network_id_exists_in_fabric() is True:
        msg = f"Skipping. network_id {instance.network_id} already exists"
        msg += f" in fabric {instance.fabric}"
        instance.logger.info(msg)
        continue
    msg = f"Creating network {instance.vlan_id} ID "
    msg += f"{instance.network_id} in vrf {instance.vrf},"
    msg += f"fabric {instance.fabric}"
    instance.logger.info(msg)
    instance.create()
