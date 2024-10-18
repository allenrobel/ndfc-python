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

1.  Set the following environment variables before running this script
    (edit appropriately for your setup)

export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/netbox-tools/lib
export NDFC_PYTHON_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/config/config.yml

Optional, to enable logging:
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json

2. This example depends on the netbox-tools library which can be found here:

https://github.com/allenrobel/netbox-tools

3.  The netbox-tools library depends on pynetbox being installed.

source /path/to/your/venv/bin/active
pip install pynetbox

4.  You'll be asked for the Ansible Vault password twice.  Once for access
    to the NDFC controller and once for access to your Netbox instance.

"""
import logging
import sys

unable_to_import = []
try:
    import requests
except ImportError as error:
    unable_to_import.append("requests")
try:
    from ndfc_python.log_v2 import Log
    from ndfc_python.ndfc import NDFC, NdfcRequestError
    from ndfc_python.ndfc_credentials import NdfcCredentials
    from ndfc_python.ndfc_network import NdfcNetwork
except ImportError as error:
    unable_to_import.append("ndfc-python")
try:
    from netbox_tools.common import netbox
except ImportError as error:
    unable_to_import.append("netbox-tools")

if len(unable_to_import) != 0:
    msg = "Unable to import the following libraries: "
    msg += f"{','.join(unable_to_import)}. "
    msg += "Check PYTHONPATH and/or install as needed."
    print(msg)
    sys.exit(1)

try:
    log = Log()
    log.commit()
except ValueError as error:
    msg = "Error while instantiating Log(). "
    msg += f"Error detail: {error}"
    print(msg)
    sys.exit(1)

log = logging.getLogger("ndfc_python.main")

nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()

try:
    netbox_obj = netbox()
    netbox_vlans = netbox_obj.ipam.vlans.all()
except ConnectionRefusedError as error:
    msg = "Unable to connect to netbox. "
    msg += f"Error detail: {error}"
    log.error(msg)
    sys.exit(1)

try:
    for vlan in netbox_vlans:
        instance = NdfcNetwork()
        instance.ndfc = ndfc
        instance.fabric = "f1"
        instance.network_id = vlan.vid + 10000
        instance.vlan_id = vlan.vid
        instance.vrf = "MyVrf"
        if instance.network_id_exists_in_fabric() is True:
            msg = f"Skipping. network_id {instance.network_id} already exists"
            msg += f" in fabric {instance.fabric}"
            log.info(msg)
            continue
        msg = f"Creating network {instance.vlan_id} ID "
        msg += f"{instance.network_id} in vrf {instance.vrf},"
        msg += f"fabric {instance.fabric}"
        log.info(msg)
        instance.create()
except (
    requests.exceptions.ConnectionError,
    ConnectionRefusedError,
    NdfcRequestError,
    ValueError,
) as error:
    msg = "Error creating network. "
    msg += f"Error detail: {error}"
    log.error(msg)
    sys.exit(1)
