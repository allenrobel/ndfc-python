# ndfc-python

This repository contains Python classes and example scripts for interacting with Cisco's Nexus Dashboard Fabric Controller (NDFC) via its REST API.


## Libraries

Library               | Description
--------------------- | -----------
ndfc                  | Methods to login to an NDFC controller and perform get, post, delete operations
ndfc_config           | Loads the config file which all libraries reference
ndfc_credentials      | Read the caller's Ansible Vault and provides the credentials therein to the other libraries
ndfc_device_info      | Retrieve device information
ndfc_discover         | Discover device
ndfc_easy_fabric_ebgp | Create a fabric using Easy_Fabric_eBGP template
ndfc_easy_fabric      | Create a fabric using Easy_Fabric template
ndfc_network          | Create, delete networks
ndfc_msd_fabric       | Create a multisite domain fabric
ndfc_policy           | Create / delete policies
ndfc_reachability     | Test for device reachability (from NDFC perspective)
ndfc_vrf              | Create VRFs
validations           | Validation methods used by the other classes

## Example scripts

Script                           | Description
-------------------------------- | -----------
example_ndfc_credentials.py      | Print the user's credentials after asking for their ansible vault password
example_ndfc_device_info.py      | Retrieve various information about a device, given its fabric_name and ip_address
example_ndfc_discover_is_ip.py   | Check if device is up and manageable.  If so, call config_save on the fabric.
example_ndfc_discover.py         | Discover device
example_ndfc_easy_fabric_bootstrap_and_local_dhcp_server_unnumbered.py | Create a fabric with unnumbered fabric interfaces, configured with inband management, local (NDFC) DHCP server, and bootstrap enabled
example_ndfc_easy_fabric_bootstrap_and_local_dhcp_server.py | Create a fabric configured with DHCP server and with bootstrap enabled
example_ndfc_easy_fabric_ebgp.py | Create an eBGP-based fabric
example_ndfc_easy_fabric_ipv6_underlay.py | Create a fabric configured with an IPv6 underlay
example_ndfc_easy_fabric_mpls_handoff.py | Create a fabric configured with MPLS handoff
example_ndfc_easy_fabric_mst.py  | Create a fabric configured with multi-instance spanning tree
example_ndfc_easy_fabric_multicast_bidir.py | Create a fabric using multicast replication and configured with four multicast bidir rendevous points
example_ndfc_easy_fabric_rpvst_plus.py | Create a fabric with rpvst+ spanning-tree root option
example_ndfc_easy_fabric_with_syslog.py | Create a fabric with syslog configured
example_ndfc_easy_fabric.py      | Create a fabric with ipv4 underlay
example_ndfc_load_config.py      | Load the configuration file pointed to in lib/ndfc_python/ndfc_config.py and print the parameters and values contained therein
example_ndfc_login.py            | Login to an NDFC controller and print the returned auth token
example_ndfc_msd_fabric.py       | Create a multi-site domain (MSD) fabric
example_ndfc_network_create.py   | Create an NDFC network
example_ndfc_network_delete.py   | Delete an NDFC network
example_ndfc_reachability.py     | Test for device reachability (from NDFC perspective)
example_ndfc_vrf_add.py          | Add a vrf to a fabric
example_netbox_ndfc_network_create.py | Read networks from a Netbox instance, and create these in NDFC.  This is a proof-of-concept for one way to integrate NDFC and Netbox.

## To clone this repository

```bash
git clone https://github.com/allenrobel/ndfc-python.git
```

## Dependencies

### Ansible Python Libraries

The libraries and scripts in this repository require that the Ansible libraries be installed.  

#### Example

```bash
pip install ansible
```

## Fabric Characteristics

The characteristics of the child/site fabrics are as follows (see also the included PDF for a topology).

1. 2 Spine acting as Route Reflectors for all Leaf and Border Gateway
2. 4 Leaf / VTEP (2 VPC pairs using fabric-peering for their virtual peer-link)
3. 2 Border Gateway / VTEP
4. 2 VRF: v1 and v2
5. L3 (ipv4 / ipv6) connectivity between VRF v1 and v2 (import/export of route-targets)
6. L2 connectivity within each VRF
7. OSPF underlay
8. VXLAN/EVPN Replication Mode: Ingress

Spines and Leafs can be added/removed by updating the Common Role Variables described below.

## Config File

To use these scripts and libraries, you'll need to update a common settings file located in ``./ndfc-python/lib/ndfc_python/config.yml``.  This points to the locaton of your Ansible Vault file (see below for how Ansible Vault is used).

There is one setting in this file (currently):

```yaml
---
ansible_vault: '/path/to/your/ansible/vault/file'
```

## Ansible Vault

Next, you'll need to edit your Ansible Vault file to add your NDFC username and password and the ip address of your ndfc controller.  We may also require the username and password for your switches in the future, so you might want to add this as well.

```bash
/path/to/your/ansible/vault/file 
```

It is recommended (but not mandatory) that you encrypt these passwords.  Below is one way to do this.

### Modify /path/to/your/ansible/vault/file

#### Edit ``ansible_password`` (password for NDFC controller) and ``device_password`` (password for NX-OS switches)

Add ``ansible_password`` and ``device_password`` in encrypted format (or non-encrypted, if you don't care about security).  These are the passwords you use to login to your DCNM/NDFC Controller, and NX-OS switches, respectively.

To add encrypted passwords for the NDFC controller and NX-OS devices, issue the following from this repository's top-level directory.

```bash
ansible-vault encrypt_string 'mySuperSecretNdfcPassword' --name 'ansible_password' >> /path/to/your/ansible/vault/file
echo "\n" >> /path/to/your/ansible/vault/file
ansible-vault encrypt_string 'mySuperSecretNxosPassword' --name 'device_password' >> /path/to/your/ansible/vault/file
echo "\n" >> /path/to/your/ansible/vault/file
```

ansible-vault will prompt you for a vault password, which you'll use to decrypt these passwords when running the example scripts.

Example:

```bash
% ansible-vault encrypt_string 'mySuperSecretNdfcPassword' --name 'ansible_password' >> /path/to/your/ansible/vault/file
New Vault password: 
Confirm New Vault password: 
%
% echo "\n" >> /path/to/your/ansible/vault/file
% cat /path/to/your/ansible/vault/file
ansible_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          35313565343034623966323832303764633165386439663133323832383336366362663431366565
          6238373030393562363831616266336464353963393566300a316564663135323263653165393330
          33353935396462663531323437336366653937326234313866623535313431366534363938633834
          6563336634653963320a376364323430316134623430636265383561663631343763646465626365
          36666366333438373537343033393939653830663061623362613439376161626439
% 
```

If you don't care about security, you can add a non-encrypted password by editing the file directly.
The following are example unencrypted passwords for the NDFC controller and NX-OS devices added to this file:

```yaml
ansible_password: mySuperSecretNdfcPassword
device_password: mySuperSecretNxosPassword
```

#### Add usernames for NDFC Controller and switches

Change ``ansible_user`` in the same file to the username associated with the above password that you're using on DCNM/NDFC.
Change ``device_username`` in the same file to the username used to login to your NX-OS switches.

Example:

```yaml
ansible_user: voldomort
device_username: admin
```

#### Add the ip address of your DCNM/NDFC Controller

```yaml
ndfc_ip: 192.168.1.1
```

## Python Path

Add this repository's library to your python path.  For example, in .bash_profile or .zprofile

```bash
PYTHONPATH=${PYTHONPATH}:${HOME}/repos/ndfc-python/lib
export PYTHONPATH
```

## To run the example scripts

```bash
cd (py311) ~ % cd /top/level/directory/for/this/repo/examples
(py311) examples % ./example_ndfc_credentials.py 
Vault password: 
username admin
password FeFiFoFum
ndfc_ip 192.168.1.2
(py311) examples % 
```

When prompted, enter the password you used in response to the ansible-vault command in step 1 above.

## Code of Conduct

This repository follows the Contributor Covenant [Code of Conduct](https://github.com/allenrobel/ndfc-roles/blob/master/CODE_OF_CONDUCT.md). Please read and familiarize yourself with this document.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) for full text.
