# interface_access_create.py

## Description

Create one or more access-mode interfaces.

## Example configuration file

``` yaml title="config/interface_access_create.yaml"
---
config:
  - access_vlan: 10
    admin_state: True
    bpduguard_enabled: True
    desc: "Eth1/2: Connected to HO1"
    enable_netflow: False
    freeform_config: ""
    interface_name: Ethernet1/2
    mtu: jumbo
    netflow_monitor: ""
    porttype_fast_enabled: True
    ptp: False
    serial_number: 96KWEIQE2HC
    speed: Auto
```

### Configuration Paramter Notes

- access_vlan - This can take a value of an empty string if you want the interface to assume a vlan value from a network attach request.
- admin_state - If True, the interface will be enabled (no shutdown).  If False, the interface will be disabled (shutdown).
- freeform_config - This one needs work.  It should really be a list.  However, you can use statements like "beacon on; 

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
./interface_access_create.py --config config/interface_access_create.yaml
# output not shown
```

## Example output

### Success

``` bash title="Interface created successfully"
arobel@glide:~/repos/ndfc-python/examples$ source $HOME/repos/ndfc-python/.venv/bin/activate
(ndfc-python) arobel@glide:~/repos/ndfc-python/examples$ source $HOME/repos/ndfc-python/env/env
(ndfc-python) arobel@glide:~/repos/ndfc-python/examples$ ./interface_access_create.py --config config/interface_access_create.yaml
Interface Ethernet1/2 created on switch 96KWEIQE2HC
(ndfc-python) arobel@glide:~/repos/ndfc-python/examples$
```

### Failure - serial_number does not exist

``` bash title="serial_number does not exist"
(ndfc-python) arobel@Allen-M4 examples % ./interface_access_create.py --config config/interface_access_create.yaml
Controller response (403 and MESSAGE 'Forbidden') implies that serial_number 6KWEIQE2HC does not exist.
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure - Bad interface name

``` bash title="Bad interface name"
(ndfc-python) arobel@Allen-M4 examples % ./interface_access_create.py --config config/interface_access_create.yaml
Error creating interface thernet1/2 on switch 96KWEIQE2HC. Controller response: {'RETURN_CODE': 500, 'DATA': [{'reportItemType': 'ERROR', 'message': 'Interface Type and Interface name does not match', 'entity': '96KWEIQE2HC~thernet1/2', 'line': 0, 'column': 0, 'trigger': None, 'impact': None, 'recommendation': None}], 'MESSAGE': 'Internal Server Error', 'METHOD': 'POST', 'REQUEST_PATH': 'https://192.168.7.7/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/interface'}
(ndfc-python) arobel@Allen-M4 examples % vi config/interface_access_create.yaml
```

### Failure - Bad configuration value for porttype_fast_enabled

``` bash title="Bad porttype_fast_enabled value"
(ndfc-python) arobel@Allen-M4 examples % ./interface_access_create.py --config config/interface_access_create.yaml
1 validation error for InterfaceAccessCreateConfigValidator
config.0.porttype_fast_enabled
  Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value='foo', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/bool_parsing
(ndfc-python) arobel@Allen-M4 examples %
```
