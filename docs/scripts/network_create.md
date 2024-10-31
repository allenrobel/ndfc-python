# network_create.py

## Description

Create one or more networks.

## Example configuration file

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
./network_create.py --config config/config_network_create.yaml
# output not shown
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
