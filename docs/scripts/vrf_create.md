# vrf_create.py

## Description

Create one or more VRFs (virtual routing and forwarding instances).

## Example configuration file

``` yaml title="config/config_vrf_create.yaml"
---
config:
  - fabric_name: MyFabric1
    vrf_display_name: MyVrf1
    vrf_id: 50005
    vrf_name: MyVrf1
    vrf_vlan_id: 3005
  - fabric_name: MyFabric1
    vrf_display_name: MyVrf2
    vrf_id: 50006
    vrf_name: MyVrf2
    vrf_vlan_id: 3006
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
./vrf_create.py --config config/config_vrf_create.yaml
# output not shown
```

## Example output

### Success

``` bash title="VRFs created successfully"
(.venv) AROBEL-M-G793% ./vrf_create.py --config prod/config_vrf_create.yaml
Created vrf MyVrf1 in fabric f1
Created vrf MyVrf2 in fabric f1
(.venv) AROBEL-M-G793%
```

### Failure - VRFs already exist in fabric MyFabric1

``` bash title="VRFs exist in the target fabric"
(.venv) AROBEL-M-G793% ./vrf_create.py --config prod/config_vrf_create.yaml
Error creating vrf MyVrf1. Error detail: VrfCreate._final_verification: VRF MyVrf1 already exists in fabric MyFabric1
Error creating vrf MyVrf2. Error detail: VrfCreate._final_verification: VRF MyVrf2 already exists in fabric MyFabric1
(.venv) AROBEL-M-G793%
```
