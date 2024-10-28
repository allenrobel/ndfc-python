# credentials.py

## Description

Read credentials specific to `ndfc-python` from an Ansible Vault file and print them.

## Expected keys

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
./credentials.py --ansible-vault $HOME/.ansible/vault
```

## Sample output

### Success

``` bash
(.venv) AROBEL-M-G793% ./credentials.py --ansible-vault $HOME/.ansible/vault
Vault password: user enters password
nd_domain local
nd_ip4 10.1.1.1
nd_password MySuperSecretNdPassword
nd_username admin
nxos_password MySuperSecretNxosPassword
nxos_username admin
(.venv) AROBEL-M-G793%```

### Failure - Ansible Vault missing expected content

``` bash
(.venv) AROBEL-M-G793% ./credentials.py --ansible-vault $HOME/.ansible/vault
Vault password:
AnsibleVaultCredentials.commit: Exiting. ansible_vault is missing key nd_password. vault file: /Users/arobel/.ansible/vault
(.venv) AROBEL-M-G793%
```

### Failure - Ansible Vault file is missing

``` bash
(.venv) AROBEL-M-G793% ./credentials.py --ansible-vault /tmp/not_an_ansible_vault
Vault password: user enters password
AnsibleVaultCredentials.commit: Exiting. Unable to load credentials in  /tmp/not_an_ansible_vault. Exception detail: Unable to retrieve file contents
Could not find or access '/tmp/not_an_ansible_vault' on the Ansible Controller.
If you are using a module and expect the file to exist on the remote, see the remote_src option
(.venv) AROBEL-M-G793%
```
