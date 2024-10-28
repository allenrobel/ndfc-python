# reachability.py

## Description

Test for device reachability (from controller perspective).

For now, this script requires Ansible to be installed since it uses Ansible
Vault for credentials.

`pip install ansible`

We plan to rework this to support other credential sources soon, including
environment variables and command line options.

## Expected Ansible Vault keys

The following keys are expected to be present in the Ansible Vault.
An error will result if these are not present.

### nd_domain

Nexus Dashboard login domain

### nd_ip4

Nexus Dashboard IPv4 address
### nd_password

Nexus Dashboard password

### nd_username

Nexus Dashboard username

### nxos_password

NX-OS switches password.
Used for Nexus Dashboard Fabric Contoller switch discovery

### nxos_username

NX-OS switches username.
Used for Nexus Dashboard Fabric Contoller switch discovery

## Example Usage

``` bash
./reachability.py --config/config_reachability.yaml --ansible-vault $HOME/.ansible/vault
```

## Sample output

### Success

``` bash
(.venv) AROBEL-M-G793% ./reachability.py --config prod/config_reachability.yaml --ansible-vault $HOME/.ansible/vault
Vault password:
auth: True
device_index: cvd-1314-leaf(FDO211218FV)
hop_count: 0
ip_addr: 172.22.150.105
known: True
last_change: None
platform: N9K-C93180YC-EX
reachable: True
selectable: False
serial_number: FDO211218FV
status_reason: already managed in f1
switch_role: None
sys_name: cvd-1314-leaf
valid: True
vdc_id: 0
vdc_mac: None
vendor: Cisco
version: 10.2(5)
(.venv) AROBEL-M-G793%
```

### Failure - Ansible Vault missing expected content

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
Exiting. Error detail: Reachability.commit: fabric_name MyFabric does not exist on the controller.
(.venv) AROBEL-M-G793%
```