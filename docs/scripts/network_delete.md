# network_delete.py

## Description

Delete one or more networks.

## Usage

``` bash
./network_delete.py --config config/config_network_delete.yaml
```

## Example Config File

``` yaml title="config/config_network_delete.yaml"
---
config:
  - fabric_name: MyFabric1
    network_name: MyNet1
  - fabric_name: MyFabric1
    network_name: MyNet2
```

## Example output

### Success

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config prod/config_network_delete.yaml
Network MyNet1 deleted from fabric MyFabric1
Network MyNet2 deleted from fabric MyFabric1
(.venv) AROBEL-M-G793%
```

### Failure - Network does not exist in fabric

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config prod/config_network_delete.yaml
Error deleting network. Error detail: NetworkDelete.commit: networkName MyNet1 does not exist in fabric MyFabric1.
Error deleting network. Error detail: NetworkDelete.commit: networkName MyNet2 does not exist in fabric MyFabric1.
(.venv) AROBEL-M-G793%
```

### Failure - Fabric does not exist

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config prod/config_network_delete.yaml
Error deleting network. Error detail: NetworkDelete.commit: fabric_name MyFabric1 does not exist on the controller.
(.venv) AROBEL-M-G793%
```
