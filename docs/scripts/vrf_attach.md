# vrf_attach.py

## Description

Attach one or more VRFs.

## Example configuration file

``` yaml title="config/vrf_attach.yaml"
---
config:
  # Topology
  # LE1--SP1--BG1---BG2--SP2--LE2

  # SITE1

  # BG1 - Border Gateway
  - deployment: true
    extension_values:
      - auto_vrf_lite_flag: true
        dot1q_id: "3"
        if_name: Ethernet1/1
        ip_mask: "10.33.0.1/30"
        ipv6_mask: "2010::10:33:0:1/64"
        neighbor_asn: "65002"
        neighbor_ip: 10.33.0.2
        ipv6_neighbor: "2010::10:33:0:2"
        peer_vrf_name: ndfc-python-vrf1
    fabric_name: SITE1
    freeform_config: []
    instance_values:
      loopback_id: 111
      loopback_ip_address: 10.19.0.141
      loopback_ip_v6_address: ""
      switch_route_target_import_evpn: ""
      switch_route_target_export_evpn: ""
    serial_number: 9IMIT2HLNO2
    vlan: 2001
    vrf_name: ndfc-python-vrf1

  # LE1 - Leaf
  - deployment: true
    extension_values:
      - {}
    fabric_name: SITE1
    freeform_config: []
    instance_values:
      loopback_id: 111
      loopback_ip_address: 10.19.0.131
      loopback_ip_v6_address: ""
      switch_route_target_import_evpn: ""
      switch_route_target_export_evpn: ""
    serial_number: 96KWEIQE2HC
    vlan: 2001
    vrf_name: ndfc-python-vrf1

  # SITE2

  # BG2 - Border Gateway
  - deployment: true
    extension_values:
      - auto_vrf_lite_flag: true
        dot1q_id: "3"
        if_name: Ethernet1/1
        ip_mask: "10.33.0.2/30"
        ipv6_mask: "2010::10:33:0:2/64"
        neighbor_asn: "65001"
        neighbor_ip: 10.33.0.1
        ipv6_neighbor: "2010::10:33:0:1"
        peer_vrf_name: ndfc-python-vrf1
    fabric_name: SITE2
    freeform_config: []
    instance_values:
      loopback_id: 111
      loopback_ip_address: 10.19.0.142
      loopback_ip_v6_address: ""
      switch_route_target_import_evpn: ""
      switch_route_target_export_evpn: ""
    serial_number: 9Q3FOROSWIP
    vlan: 2001
    vrf_name: ndfc-python-vrf1

  # LE2 - Leaf
  - deployment: true
    extension_values:
      - {}
    fabric_name: SITE2
    freeform_config: []
    instance_values:
      loopback_id: 111
      loopback_ip_address: 10.19.0.132
      loopback_ip_v6_address: ""
      switch_route_target_import_evpn: ""
      switch_route_target_export_evpn: ""
    serial_number: 9OW9132EH2M
    vlan: 2001
    vrf_name: ndfc-python-vrf1

```

### Configuration Notes

#### instance_values

- If the fabric is configured with `Per VRF Per VTEP Loopback IPv4 Auto-Provision`
  - instance_values.loopback_id must be set
  - instance_values.loopback_ip_address must be set to a value within the range configured in `Per VRF Per Loopback IPv4 Pool for Loopbacks`
  - You'll find the `Per VRF Per Loopback` parameters under `Fabric Settings` -> `Resources`
  - The same applies for `Per VRF Per VTEP Loopback IPv6 Auto-Provision`

## Example Usage

The example below uses environment variables for credentials, so requires
only the `--config` argument.  See [Running the Example Scripts]
for details around specifying credentials from the command line, from
environment variables, from Ansible Vault, or a combination of these
credentials sources.

[Running the Example Scripts]: ../setup/running-the-example-scripts.md

``` bash
export ND_DOMAIN=local
export ND_IP4=10.1.1.1
export ND_PASSWORD=MySecret
export ND_USERNAME=admin
./vrf_attach.py --config config/vrf_attach.yaml
# output not shown
```

## Example output

### Success

``` bash
(ndfc-python) arobel@Allen-M4 examples % ./vrf_attach.py --config config/vrf_attach.yaml
VRF ndfc-python-vrf1 attached to fabric SITE1, serial number 96KWEIQE2HC.
VRF ndfc-python-vrf1 attached to fabric SITE2, serial number 9OW9132EH2M.
(ndfc-python) arobel@Allen-M4 examples %
```

### Example Failure Messages

#### VRF does not exist

``` bash
(ndfc-python) arobel@Allen-M4 examples % ./vrf_attach.py --config test_vrf_attach.yaml
Error attaching vrf. Error detail: VrfAttach._final_verification: vrfName foo does not exist in fabric SITE1. Create it first before calling VrfAttach.commit
(ndfc-python) arobel@Allen-M4 examples %
```

#### Switch serial_number is invalid

``` bash
(ndfc-python) arobel@Allen-M4 examples % ./vrf_attach.py --config test_vrf_attach.yaml
Invalid Switch Serial Number :96KWEIQE2H
(ndfc-python) arobel@Allen-M4 examples %
```

#### Per-VRF loopback is enabled within the fabric, and loopback_id is set to ""

``` bash
(ndfc-python) arobel@Allen-M4 examples % ./vrf_attach.py --config config/vrf_attach.yaml
per vrf level loopback is enabled and hence not allowed to clear the loopback ID  or IP
per vrf level loopback is enabled and hence not allowed to clear the loopback ID  or IP
(ndfc-python) arobel@Allen-M4 examples %
```

#### Invalid value for `mso_created`

```bash
(ndfc-python) arobel@Allen-M4 examples % ./vrf_attach.py --config config/vrf_attach.yaml
1 validation error for VrfAttachConfigValidator
config.1.mso_created
  Input should be a valid boolean [type=bool_type, input_value='foo', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/bool_type
(ndfc-python) arobel@Allen-M4 examples %
```
