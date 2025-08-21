# vrf_delete.py

## Description

Delete one or more VRFs (virtual routing and forwarding instances).

## Example configuration file

``` yaml title="config/config_vrf_create.yaml"
---
config:
  - fabric_name: MyFabric1
    vrf_names:
    - MyVrf1
    - MyVrf2
  - fabric_name: MyFabric2
    vrf_names:
    - MyVrf3
    - MyVrf4
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
./vrf_delete.py --config config/vrf_delete.yaml
# output not shown
```

## Example output

### Success

``` bash title="VRFs deleted successfully"
(.venv) AROBEL-M-G793% ./vrf_delete.py --config prod/vrf_delete.yaml
Deleted vrfs MyVrf1,MyVrf2 from fabric f1
(.venv) AROBEL-M-G793%(.venv) AROBEL-M-G793%
```

### Failure - VRFs do not exist in fabric f1

``` bash title="VRFs do not exist in the target fabric"
(.venv) AROBEL-M-G793% ./vrf_delete.py --config prod/config_vrf_create.yaml
Error deleting vrfs ['MyVrf1', 'MyVrf2'] from fabric f1. Error detail: VrfDelete._final_verification: VRF MyVrf1 does not exist in fabric f1
(.venv) AROBEL-M-G793%
```

### Failure - Fabric f2 does not exist

``` bash title="Fabric does not exist"
(.venv) AROBEL-M-G793% ./vrf_delete.py --config prod/config_vrf_create.yaml
Error deleting vrfs ['MyVrf1', 'MyVrf2'] from fabric f2. Error detail: VrfDelete.get_vrfs: Fabric f2 does not exist on the controller.
(.venv) AROBEL-M-G793%
```
