# network_attach.py

## Description

Attach one or more networks.

## Example configuration file

``` yaml title="config/network_attach.yaml"
---
config:
  - deployment: true
    detach_switch_ports: []
    dot1q_vlan: ""
    extension_values: ""
    fabric_name: SITE1
    freeform_config: []
    instance_values: ""
    mso_created: false
    mso_set_vlan: false
    network_name: ndfc-python-net1
    serial_number: 96KWEIQE2HC
    switch_ports:
      - Ethernet1/2
    untagged: true
    tor_ports: []
    vlan: 2301
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
export ND_IP4=10.1.1.1
export ND_PASSWORD=MySecret
export ND_USERNAME=admin
./network_attach.py --config config/network_attach.yaml
# output not shown
```

## Example output

### Success

``` bash
(ndfc-python) arobel@Allen-M4 examples % ./network_attach.py --config config/network_attach.yaml
Network ndfc-python-net1 attached to fabric SITE1, serial number 96KWEIQE2HC.
Network ndfc-python-net1 attached to fabric SITE2, serial number 9OW9132EH2M.
(ndfc-python) arobel@Allen-M4 examples %
```

### Example Failure Messages

#### Network does not exist

``` bash
(ndfc-python) arobel@Allen-M4 examples % ./network_attach.py --config test_network_attach.yaml
Error attaching network. Error detail: NetworkAttach._final_verification: networkName foo does not exist in fabric SITE1. Create it first before calling NetworkAttach.commit
(ndfc-python) arobel@Allen-M4 examples %
```

#### Switch serial_number is invalid

``` bash
(ndfc-python) arobel@Allen-M4 examples % ./network_attach.py --config test_network_attach.yaml
Invalid Switch Serial Number :96KWEIQE2H
(ndfc-python) arobel@Allen-M4 examples %
```

#### Invalid interface

``` bash
(ndfc-python) arobel@Allen-M4 examples % ./network_attach.py --config test_network_attach.yaml
Error attaching network. Controller response: {'RETURN_CODE': 200, 'DATA': {'ndfc-python-net1-[96KWEIQE2HC/LE1]': 'Invalid Interfaces in LE1. Invalid interfaces are Po2.'}, 'MESSAGE': 'OK', 'METHOD': 'POST', 'REQUEST_PATH': 'https://192.168.7.7/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/SITE1/networks/attachments'}
(ndfc-python) arobel@Allen-M4 examples %
```

#### Invalid value for `untagged`

```bash
(ndfc-python) arobel@Allen-M4 examples % ./network_attach.py --config test_network_attach.yaml
1 validation error for NetworkAttachConfigValidator
config.0.untagged
  Input should be a valid boolean [type=bool_type, input_value='foo', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/bool_type
(ndfc-python) arobel@Allen-M4 examples %
```
