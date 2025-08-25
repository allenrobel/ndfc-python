# rm_switch_resource_usage.py

## Description

Display switch resource usage (from controller perspective) for one or more devices.

## Example configuration file

```yaml title="Example configuration file"
---
config:
  - serial_number: 9OW9132EH2M
    pool_name: ALL
  - serial_number: 9OW9132EH2M
    pool_name: TOP_DOWN_VRF_VLAN
```

## Example Usage

The example below uses environment variables for credentials, so requires only the `--config` argument. See [Running the Example Scripts] for details around specifying credentials from the command line, from environment variables, from Ansible Vault, or a combination of these credentials sources.

[Running the Example Scripts]: ../setup/running-the-example-scripts.md

```bash title="Example usage"
export ND_DOMAIN=local
export ND_IP4=10.1.1.1
export ND_PASSWORD=MyNdPassword
export ND_USERNAME=admin
export NXOS_PASSWORD=MyNxosPassword
export NXOS_USERNAME=admin
cd $HOME/repos/ndfc-python/examples
./rm_switch_resource_usage.py --config config/rm_switch_resource_usage.yaml
# output not shown
```

## Sample output

### Success

```bash title="Success"
(ndfc-python) arobel@Allen-M4 examples % ./rm_switch_resource_usage.py --config config/rm_switch_resource_usage.yaml
Switch 9OW9132EH2M resource usage. Filter: ALL.[
    {
        "id": 96,
        "resourcePool": {
            "id": 0,
            "poolName": "TOP_DOWN_NETWORK_VLAN",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "v0n0",
        "allocatedIp": "2301",
        "allocatedOn": 1755817858702,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 97,
        "resourcePool": {
            "id": 0,
            "poolName": "TOP_DOWN_VRF_VLAN",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "v0",
        "allocatedIp": "2000",
        "allocatedOn": 1755378426526,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 197,
        "resourcePool": {
            "id": 0,
            "poolName": "TOP_DOWN_VRF_VLAN",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "ndfc-python-vrf1",
        "allocatedIp": "2001",
        "allocatedOn": 1755832323207,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 27,
        "resourcePool": {
            "id": 0,
            "poolName": "LOOPBACK_ID",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "loopback0",
        "allocatedIp": "0",
        "allocatedOn": 1755324490087,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 40,
        "resourcePool": {
            "id": 0,
            "poolName": "LOOPBACK_ID",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "loopback1",
        "allocatedIp": "1",
        "allocatedOn": 1755324503672,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 98,
        "resourcePool": {
            "id": 0,
            "poolName": "LOOPBACK_ID",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "v0~loopback2",
        "allocatedIp": "2",
        "allocatedOn": 1755378426533,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 200,
        "resourcePool": {
            "id": 0,
            "poolName": "LOOPBACK_ID",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "ndfc-python-vrf1~loopback131",
        "allocatedIp": "131",
        "allocatedOn": 1755838635461,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 26,
        "resourcePool": {
            "id": 0,
            "poolName": "LOOPBACK0_IP_POOL",
            "fabricName": null,
            "vrfName": "default",
            "poolType": "IP_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "DeviceInterface",
        "entityName": "9OW9132EH2M~loopback0",
        "allocatedIp": "10.22.0.1",
        "allocatedOn": 1755324489993,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 38,
        "resourcePool": {
            "id": 0,
            "poolName": "10.25.0.4/30",
            "fabricName": null,
            "vrfName": "default",
            "poolType": "IP_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "DeviceInterface",
        "entityName": "9OW9132EH2M~Ethernet1/1",
        "allocatedIp": "10.25.0.6",
        "allocatedOn": 1755324494566,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 39,
        "resourcePool": {
            "id": 0,
            "poolName": "LOOPBACK1_IP_POOL",
            "fabricName": null,
            "vrfName": "default",
            "poolType": "IP_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "DeviceInterface",
        "entityName": "9OW9132EH2M~loopback1",
        "allocatedIp": "10.23.0.1",
        "allocatedOn": 1755324503584,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 99,
        "resourcePool": {
            "id": 0,
            "poolName": "v0_LOOPBACK_IPV4",
            "fabricName": null,
            "vrfName": "v0",
            "poolType": "IP_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "DeviceInterface",
        "entityName": "9OW9132EH2M~loopback2",
        "allocatedIp": "10.29.0.1",
        "allocatedOn": 1755378426535,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 201,
        "resourcePool": {
            "id": 0,
            "poolName": "ndfc-python-vrf1_LOOPBACK_IPV4",
            "fabricName": null,
            "vrfName": "ndfc-python-vrf1",
            "poolType": "IP_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "DeviceInterface",
        "entityName": "9OW9132EH2M~loopback131",
        "allocatedIp": "10.19.0.131",
        "allocatedOn": 1755838635463,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    }
]
Switch 9OW9132EH2M resource usage. Filter: TOP_DOWN_VRF_VLAN.[
    {
        "id": 97,
        "resourcePool": {
            "id": 0,
            "poolName": "TOP_DOWN_VRF_VLAN",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "v0",
        "allocatedIp": "2000",
        "allocatedOn": 1755378426526,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    },
    {
        "id": 197,
        "resourcePool": {
            "id": 0,
            "poolName": "TOP_DOWN_VRF_VLAN",
            "fabricName": null,
            "vrfName": null,
            "poolType": "ID_POOL",
            "dynamicSubnetRange": null,
            "targetSubnet": 0,
            "overlapAllowed": false,
            "hierarchicalKey": null
        },
        "entityType": "Device",
        "entityName": "ndfc-python-vrf1",
        "allocatedIp": "2001",
        "allocatedOn": 1755832323207,
        "allocatedFlag": true,
        "allocatedScopeValue": "9OW9132EH2M",
        "ipAddress": "192.168.12.152",
        "switchName": "LE2",
        "hierarchicalKey": "0"
    }
]
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure - Invalid configuration

```bash
(ndfc-python) arobel@Allen-M4 examples % ./rm_switch_resource_usage.py --config config/rm_switch_resource_usage.yaml
1 validation error for RmSwitchResourceUsageConfigValidator
config
  Input should be a valid list [type=list_type, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.11/v/list_type
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure - Configuration is missing mandatory serial_number

```bash
(ndfc-python) arobel@Allen-M4 examples % ./rm_switch_resource_usage.py --config config/rm_switch_resource_usage.yaml
1 validation error for RmSwitchResourceUsageConfigValidator
config.0.serial_number
  Field required [type=missing, input_value={'pool_name': 'ALL'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure - serial_number does not exist on the controller

TODO: Complete this section.

```bash
# output not shown
```
