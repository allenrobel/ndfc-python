# network_create.py

## Description

Creates a network.

## Usage

``` bash
./device_info.py --config config_device_info.yaml
```

## Example Config File

``` yaml
---
config:
  fabric_name: f1
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
Network MyNet created in fabric f1
(.venv) AROBEL-M-G793%
```

### Failure

``` bash
(.venv) AROBEL-M-G793% ./network_create.py --config prod/config_network_create.yaml
Error creating network. Error detail: NetworkCreate.commit: networkId 30005 already exists in fabric f1. Delete it before calling NetworkCreate.commit
(.venv) AROBEL-M-G793%
```
