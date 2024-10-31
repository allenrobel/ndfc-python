# reachability.py

## Description

Display reachability (from controller perspective) information for one or more
devices.

## Example configuration file

``` yaml title="Example configuraion file"
---
config:
  - fabric_name: MyFabric1
    seed_ip: 10.1.1.2
  - fabric_name: MyFabric1
    seed_ip: 10.1.1.3
```

## Example Usage

The example below uses environment variables for credentials, so requires
only the `--config` argument.  See [Running the Example Scripts]
for details around specifying credentials from the command line, from
environment variables, from Ansible Vault, or a combination of these
credentials sources.

[Running the Example Scripts]: ../setup/running-the-example-scripts.md

``` bash title="Example usage"
export ND_DOMAIN=local
export ND_IP4=10.1.1.1
export ND_PASSWORD=MyNdPassword
export ND_USERNAME=admin
export NXOS_PASSWORD=MyNxosPassword
export NXOS_USERNAME=admin
cd $HOME/repos/ndfc-python/examples
./reachability.py --config/config_reachability.yaml
# output not shown
sys_name: cvd-1313-leaf
  auth: True
  device_index: cvd-1313-leaf(FDO211218HH)
  hop_count: 0
  ip_addr: 10.1.1.2
  known: True
  last_change: None
  platform: N9K-C93180YC-EX
  reachable: True
  selectable: False
  serial_number: FDO123456AB
  status_reason: already managed in MyFabric1
  switch_role: None
  valid: True
  vdc_id: 0
  vdc_mac: None
  vendor: Cisco
  version: 10.3(1)
```

## Sample output

### Success

``` bash title="Success"
export ND_DOMAIN=local
export ND_IP4=10.1.1.1
export ND_PASSWORD=MyNdPassword
export ND_USERNAME=admin
export NXOS_PASSWORD=MyNxosPassword
export NXOS_USERNAME=admin
cd $HOME/repos/ndfc-python/examples
./reachability.py --config/config_reachability.yaml
# output not shown
sys_name: cvd-1313-leaf
  auth: True
  device_index: cvd-1313-leaf(FDO211218HH)
  hop_count: 0
  ip_addr: 10.1.1.2
  known: True
  last_change: None
  platform: N9K-C93180YC-EX
  reachable: True
  selectable: False
  serial_number: FDO123456AB
  status_reason: already managed in MyFabric1
  switch_role: None
  valid: True
  vdc_id: 0
  vdc_mac: None
  vendor: Cisco
  version: 10.3(1)
```

### Failure - Missing credential

``` bash
(.venv) AROBEL-M-G793% ./reachability.py --config prod/config_reachability.yaml --ansible-vault $HOME/.ansible/vault
Vault password:
CredentialsAnsibleVault.commit: Exiting. ansible_vault is missing key nd_password. vault file: /Users/arobel/.ansible/vault
(.venv) AROBEL-M-G793%
```

### Failure - Ansible Vault file is missing

``` bash
(.venv) AROBEL-M-G793% ./reachability.py --config prod/config_reachability.yaml --ansible-vault $HOME/does_not_exist
Vault password:
Exiting. Error detail: CredentialsAnsibleVault.commit: Unable to load credentials in  /Users/arobel/does_not_exist. Exception detail: AnsibleFileNotFound: Unable to retrieve file contents
Could not find or access '/Users/arobel/does_not_exist' on the Ansible Controller.
If you are using a module and expect the file to exist on the remote, see the remote_src option
(.venv) AROBEL-M-G793%
```

### Failure - fabric_name does not exist on the controller

```bash
(.venv) AROBEL-M-G793% ./reachability.py --config prod/config_reachability.yaml --ansible-vault $HOME/.ansible/vault
Vault password:
Exiting. Error detail: Reachability.commit: fabric_name MyFabric1 does not exist on the controller.
(.venv) AROBEL-M-G793%
```
