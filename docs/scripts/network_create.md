# network_create.py

## Description

Create one or more networks.

## Usage

``` bash
./network_create.py --config config/config_network_create.yaml
```

## Example Config File

``` yaml title="config/config_network_create.yaml"
---
config:
  - fabric_name: MyFabric1
    network_name: MyNet1
    enable_ir: True
    gateway_ip_address: 10.5.1.1/24
    network_id: 30005
    vlan_id: 3005
    vrf_name: MyVrf1
  - fabric_name: MyFabric1
    network_name: MyNet2
    enable_ir: True
    gateway_ip_address: 10.6.1.1/24
    network_id: 30006
    vlan_id: 3006
    vrf_name: MyVrf1
```

## Example output

### Success

``` bash
(.venv) AROBEL-M-G793% ./network_create.py --config prod/config_network_create.yaml
Network MyNet1 with id 30005 created in fabric MyFabric1
Network MyNet2 with id 30006 created in fabric MyFabric1
(.venv) AROBEL-M-G793%
```

### Failure

``` bash
(.venv) AROBEL-M-G793% ./network_create.py --config prod/config_network_create.yaml
Error creating network. Error detail: NetworkCreate.commit: networkId 30005 already exists in fabric MyFabric1. Delete it before calling NetworkCreate.commit
(.venv) AROBEL-M-G793%
```
