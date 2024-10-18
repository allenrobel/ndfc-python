# ndfc-python

This repository contains Python classes and example scripts for interacting
with Cisco's Nexus Dashboard Fabric Controller (NDFC) via its REST API.

NOTES:
1. We have removed the example scripts and libraries for fabrics for now.
   These will be replaced with code from the DCNM Ansible Collection which
   we are modifying to work without Ansible.

## Libraries

Library                 | Description
----------------------- | -----------
[ndfc]                  | Methods to login to an NDFC controller and perform get, post, delete operations
[ndfc_config]           | Loads the config file which all libraries reference
[ndfc_credentials]      | Read the caller's Ansible Vault and provides the credentials therein to the other libraries
[ndfc_device_info]      | Retrieve device information
[ndfc_discover]         | Discover device
[ndfc_network]          | Create, delete networks
[ndfc_policy]           | Create / delete policies
[ndfc_reachability]     | Test for device reachability (from NDFC perspective)
[ndfc_vrf]              | Create VRFs
[validations]           | Validation methods used by the other classes

[ndfc]: /lib/ndfc_python/ndfc.py
[ndfc_config]: /lib/ndfc_python/ndfc_config.py
[ndfc_credentials]: /lib/ndfc_python/ndfc_credentials.py
[ndfc_device_info]: /lib/ndfc_python/ndfc_device_info.py
[ndfc_discover]: /lib/ndfc_python/ndfc_discover.py
[ndfc_network]: /lib/ndfc_python/ndfc_network.py
[ndfc_policy]: /lib/ndfc_python/ndfc_policy.py
[ndfc_reachability]: /lib/ndfc_python/ndfc_reachability.py
[ndfc_vrf]: /lib/ndfc_python/ndfc_vrf.py
[validations]: /lib/ndfc_python/validations.py

## The following libraries have been removed, see note 1 above

Library                 | Description
----------------------- | -----------
ndfc_easy_fabric_ebgp   | Create a fabric using Easy_Fabric_eBGP template.
ndfc_easy_fabric        | Create a fabric using Easy_Fabric template.
ndfc_msd_fabric         | Create a multisite domain fabric.

## Example scripts

Script                  | Description
----------------------- | -----------
[credentials.py]        | Print the user's credentials after asking for their ansible vault password
[device_info.py]          | Retrieve various information about a device, given its fabric_name and ip_address
[discover_is_up.py]       | Check if device is up and manageable.  If so, call config_save on the fabric.
[discover.py]             | Discover device
[load_config.py]          | Load the configuration file pointed to in lib/ndfc_python/ndfc_config.py and print the parameters and values contained therein
[login.py]                | Login to an NDFC controller and print the returned auth token
[network_create.py]       | Create an NDFC network
[network_delete.py]       | Delete an NDFC network
[reachability.py]         | Test for device reachability (from NDFC perspective)
[vrf_add.py]              | Add a vrf to a fabric
[netbox_ndfc_network_create.py] | Read networks from a Netbox instance, and create these in NDFC.  This is a proof-of-concept for one way to integrate NDFC and Netbox.

## The following example scripts have been removed, see note 1 above

Script                  | Description
----------------------- | -----------
fabric_bootstrap_and_local_dhcp_server_unnumbered.py | Create a fabric with unnumbered fabric interfaces, configured with inband management, local (NDFC) DHCP server, and bootstrap enabled
fabric_bootstrap_and_local_dhcp_server.py | Create a fabric configured with DHCP server and with bootstrap enabled
fabric_ebgp.py          | Create an eBGP-based fabric
fabric_ipv4_underlay.py | Create a fabric with ipv4 underlay
fabric_ipv6_underlay.py | Create a fabric configured with an IPv6 underlay
fabric_mpls_handoff.py  | Create a fabric configured with MPLS handoff
fabric_mst.py           | Create a fabric configured with multi-instance spanning tree
fabric_multicast_bidir.py | Create a fabric using multicast replication and configured with four multicast bidir rendevous points
fabric_netflow.py       | Create a fabric with netflow configuration options
fabric_rpvst_plus.py    | Create a fabric with rpvst+ spanning-tree root option
fabric_with_syslog.py   | Create a fabric with syslog configured
fabric_msd.py           | Create a multi-site domain (MSD) fabric

[credentials.py]: /examples/credentials.py
[device_info.py]: /examples/device_info.py
[discover_is_up.py]: /examples/discover_is_up.py
[discover.py]: /examples/discover.py
[load_config.py]: /examples/load_config.py
[login.py]: /examples/login.py
[netbox_ndfc_network_create.py]: /examples/netbox_ndfc_network_create.py
[network_create.py]: /examples/network_create.py
[network_delete.py]: /examples/network_delete.py
[reachability.py]: /examples/reachability.py
[vrf_add.py]: /examples/vrf_add.py

## To clone this repository

```bash
git clone https://github.com/allenrobel/ndfc-python.git
```

## Dependencies

### Ansible Python Libraries

The libraries and scripts in this repository require that the Ansible libraries be installed.
These are needed for Ansible vault.

#### Example

```bash
pip install ansible
```

<!---
Commenting this section out until we have replaced the fabric scripts and libraries...

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

-->

## Config File

To use these scripts and libraries, you'll need to update a common settings file and set the
environment variable ``NDFC_PYTHON_CONFIG`` to point to it.  For example, if you want your
settings to be located in $HOME/ndfc-python-settings.yaml, then set:

```bash
export NDFC_PYTHON_CONFIG=$HOME/ndfc-python-settings.yaml
```

And edit this file to contain:

```yaml
---
ansible_vault: '/path/to/your/ansible/vault/file'
```

## Ansible Vault

Next, you'll need to edit your Ansible Vault file to add your Nexus Dashboard Controller
credentials (username, password, and login domain) and ip address.

We may also require the username and password for your switches in the future,
so you might want to add this as well.

```bash
/path/to/your/ansible/vault/file 
```

It is recommended (but not mandatory) that you encrypt all passwords.  Below is one way to do this.

### Modify /path/to/your/ansible/vault/file

#### Edit ``ansible_password`` (password for NDFC controller) and ``device_password`` (password for NX-OS switches)

Add ``ansible_password`` and ``device_password`` in encrypted format (or non-encrypted,
if you don't care about security).  These are the passwords you use to login to your
ND/NDFC Controller, and NX-OS switches, respectively.

To add encrypted passwords for the ND/NDFC controller and NX-OS devices,
issue the following from this repository's top-level directory.

```bash
ansible-vault encrypt_string 'mySuperSecretNdfcPassword' --name 'ansible_password' >> /path/to/your/ansible/vault/file
echo "" >> /path/to/your/ansible/vault/file
ansible-vault encrypt_string 'mySuperSecretNxosPassword' --name 'device_password' >> /path/to/your/ansible/vault/file
echo "" >> /path/to/your/ansible/vault/file
```

ansible-vault will prompt you for a vault password, which you'll use to decrypt
these passwords when running the example scripts.

Example:

```bash
% ansible-vault encrypt_string 'mySuperSecretNdfcPassword' --name 'ansible_password' >> /path/to/your/ansible/vault/file
New Vault password: 
Confirm New Vault password: 
%
% echo "" >> /path/to/your/ansible/vault/file
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

If you don't care about security, you can add a non-encrypted password by editing the
file directly. The following are example unencrypted passwords for the ND/NDFC controller
and NX-OS devices added to this file:

```yaml
ansible_password: mySuperSecretNdfcPassword
device_password: mySuperSecretNxosPassword
```

#### Add the domain for Nexus Dashboard Controller login

Change ``nd_domain`` in the same file to the domain associated with the above password
that you're using on ND/NDFC.  If the "domain" field is not displayed when you login to
the GUI, then use local, as shown below.

```yaml
nd_domain: local
```

#### Add usernames for Nexus Dashboard Controller and switches

Change ``ansible_user`` in the same file to the username associated with the above
password that you're using on ND/NDFC.

Change ``device_username`` in the same file to the username used to login to your
NX-OS switches.

Example:

```yaml
ansible_user: voldomort
device_username: admin
```

#### Add the ip address of your Nexus Dashboard Controller

```yaml
ndfc_ip: 192.168.1.1
```

## Python Path

Add this repository's library to your python path.  For example, in .bash_profile or .zprofile

```bash
export PYTHONPATH=${PYTHONPATH}:${HOME}/repos/ndfc-python/lib
```

## Logging configuration

To enable logging, set the following environment variable.

```bash
export NDFC_LOGGING_CONFIG=/path/to/logging_config.json
```

This is a standard Pyton logging configuration file.  There is an example
file in this repository at ``lib/ndfc_python/logging_config.json``

## To run the example scripts

```bash
export PYTHONPATH=${PYTHONPATH}:/path/to/this/repo/ndfc-python/lib
export NDFC_PYTHON_CONFIG=/path/to/ndfc-python-settings.yaml
export NDFC_LOGGING_CONFIG=/path/to/ndfc-python-logging-config.json #optional

cd (py311) ~ % cd /top/level/directory/of/this/repo/examples
(py311) examples % ./example_ndfc_credentials.py 
Vault password: 
username admin
password FeFiFoFum
ndfc_ip 192.168.1.2
nd_domain local
(py311) examples % 
```

When prompted, enter the password you used in response to the ansible-vault command in step 1 above.

## Code of Conduct

This repository follows the Contributor Covenant [Code of Conduct](https://github.com/allenrobel/ndfc-roles/blob/master/CODE_OF_CONDUCT.md). Please read and familiarize yourself with this document.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) for full text.
