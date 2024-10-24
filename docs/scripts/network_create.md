# network_create.py

## Description

Creates a network.

## Usage

``` bash
./network_create.py --config config_network_create.yaml
```

## Example Config File

``` yaml title="config_network_create.yaml"
---
config:
  fabric_name: MyFabric
  network_name: MyNet
  enable_ir: True
  gateway_ip_address: 10.1.1.1/24
  network_id: 30005
  vlan_id: 3005
  vrf_name: MyVrf
```

## Example output

### Success

``` bash
(.venv) AROBEL-M-G793% ./network_create.py --config prod/config_network_create.yaml
Network MyNet created in fabric MyFabric
(.venv) AROBEL-M-G793%
```

### Failure

``` bash
(.venv) AROBEL-M-G793% ./network_create.py --config prod/config_network_create.yaml
Error creating network. Error detail: NetworkCreate.commit: networkId 30005 already exists in fabric MyFabric. Delete it before calling NetworkCreate.commit
(.venv) AROBEL-M-G793%
```
