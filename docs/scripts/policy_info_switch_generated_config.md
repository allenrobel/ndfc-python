# policy_info_switch_generated_config.py

## Description

Retrieve all policies for one or more switches and display their generated configs.

## Example configuration file

``` yaml title="config/policy_info_switch_generated_config.yaml"
---
config:
  - switch_name: LE1
    fabric_name: SITE1
  - switch_name: LE2
    fabric_name: SITE2
```

## Example Usage

The example below uses environment variables for credentials, so requires
only the `--config` argument.  See [Running the Example Scripts]
for details around specifying credentials from the command line, from
environment variables, from Ansible Vault, or a combination of these
credentials sources.

[Running the Example Scripts]: ../setup/running-the-example-scripts.md

``` bash
export ND_DOMAIN=local
export ND_IP4=192.168.7.7
export ND_PASSWORD=MySecretPassword
export ND_USERNAME=admin
./policy_info_switch_generated_config.py --config config/policy_info_switch_generated_config.yaml
# output not shown
```

## Example output

### Success

``` bash title="Policies retrieved successfully"
(ndfc-python) arobel@Allen-M4 examples % ./policy_info_switch_generated_config.py --config config/s12/policy_info_switch_generated_config.yaml
SITE1, LE1, policies:
power redundancy-mode ps-redundant
copp profile strict
feature dhcp
ipv6 switch-packets lla
feature ospf
feature pim
nv overlay evpn
feature interface-vlan
feature vn-segment-vlan-based
feature lldp
feature nv overlay
feature bgp
feature nxapi
cfs eth distribute
feature lacp
feature ngoam
username admin password 5 $5$BEJAMJ$ujNFizvgASVsw3a2RACVBgXpCOBVbmNE5Esh/vDc4ET role network-admin
service dhcp
ip dhcp relay
ip dhcp relay information option
ip dhcp relay information option vpn
ipv6 dhcp relay
system jumbomtu 9216
route-map FABRIC-RMAP-REDIST-SUBNET permit 10
  match tag 12345
router bgp 65001
  router-id 10.11.0.2
router ospf UNDERLAY
  router-id 10.11.0.2
ip pim ssm range 232.0.0.0/8
ip pim rp-address 10.13.254.1 group-list 239.1.1.0/25
nxapi https port 443
nxapi http port 80


snmp-server host 192.168.12.12 traps version 2c public udp-port 2162


hostname LE1
no password strength-check
evpn
fabric forwarding anycast-gateway-mac 2020.0000.00aa
vrf context management
  ip route 0.0.0.0/0 192.168.12.1
vrf context management
  ip route 0.0.0.0/0 192.168.12.1
vlan 1
line vty
etc...
```

### Failure - Fabric does not exist

``` bash title="Fabric does not exist"
(ndfc-python) arobel@Allen-M4 examples % ./policy_info_switch_generated_config.py --config config/s12/policy_info_switch_generated_config.yaml
Error retrieving fabric SITE8, switch LE1, policies. Error detail: PolicyInfoSwitch._final_verification: fabric_name SITE8 does not exist on the controller.
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure - Switch does not exist in fabric

``` bash title="Switch does not exist in fabric"
(ndfc-python) arobel@Allen-M4 examples % ./policy_info_switch_generated_config.py --config config/s12/policy_info_switch_generated_config.yaml
Error retrieving fabric SITE1, switch LE3, policies. Error detail: PolicyInfoSwitch._final_verification: switch_name LE3 not found in fabric SITE1.
(ndfc-python) arobel@Allen-M4 examples %
```
