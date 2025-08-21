# network_delete.py

## Description

Delete one or more networks.

## Example configuration file

``` yaml title="config/network_delete.yaml"
---
config:
  - fabric_name: MyFabric1
    network_name: MyNet1
  - fabric_name: MyFabric1
    network_name: MyNet2
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
./network_delete.py --config config/network_delete.yaml
# output not shown
```

## Example output

### Success

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config prod/network_delete.yaml
Network MyNet1 deleted from fabric MyFabric1
Network MyNet2 deleted from fabric MyFabric1
(.venv) AROBEL-M-G793%
```

### Failure - Network does not exist in fabric

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config prod/network_delete.yaml
Error deleting network. Error detail: NetworkDelete.commit: networkName MyNet1 does not exist in fabric MyFabric1.
Error deleting network. Error detail: NetworkDelete.commit: networkName MyNet2 does not exist in fabric MyFabric1.
(.venv) AROBEL-M-G793%
```

### Failure - Fabric does not exist

``` bash
(.venv) AROBEL-M-G793% ./network_delete.py --config prod/network_delete.yaml
Error deleting network. Error detail: NetworkDelete.commit: fabric_name MyFabric1 does not exist on the controller.
(.venv) AROBEL-M-G793%
```
