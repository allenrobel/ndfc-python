# network_delete.py

## Description

Delete a network.

## Usage

``` bash
./network_delete.py --config config_network_delete.yaml
```

## Example Config File

``` yaml title="config_network_delete.yaml"
---
config:
  fabric_name: MyFabric
  network_name: MyNet
```

## Example output

### Success

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config prod/config_network_delete.yaml
Network MyNet deleted in fabric MyFabric
(.venv) AROBEL-M-G793%
```

### Failure - Network does not exist in fabric

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config prod/config_network_delete.yaml
Error deleting network. Error detail: NetworkDelete.commit: networkName MyNet does not exist in fabric MyFabric.
(.venv) AROBEL-M-G793%
```

### Failure - Fabric does not exist

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config config_network_delete.yaml
Error deleting network. Error detail: NetworkDelete.commit: fabric_name MyFabric does not exist on the controller.
(.venv) AROBEL-M-G793%
```
