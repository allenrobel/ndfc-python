# Credentials

Credentials to access the Nexus Dashboard can be set in a few ways.

## Script command-line options

Script command line options, take precedence over everything else (environment
variables and Ansible Vault).

That is, if environment variables are set for `ND_PASSWORD` and `ND_USERNAME`,
and your Ansible Vault contains `nd_domain`, you can override `ND_PASSWORD`
and `nd_domain` (while using the value of ND_USERNAME) with:

``` bash title="Override environment variable"
./script_name.py --nd_password MyNewPassword --nd-domain local --ansible-vault $HOME/.ansible/vault
```

### --nd-domain

Nexus Dashboard login domain.

Sets `args.nd_domain` within scripts.

### --nd-ip4

Nexus Dashboard IPv4 address

Sets `args.nd_ip4` within scripts.

### --nd-password

Nexus Dashboard password

Sets `args.nd_password` within scripts.

### --nd-username

Nexus Dashboard username

Sets `args.nd_username` within scripts.

### --nxos-password

Password for NX-OS switches.
Used for Nexus Dashboard Fabric Contoller switch discovery

Sets `args.nxos_password` within scripts.

### --nxos-username

Username for NX-OS switches.
Used for Nexus Dashboard Fabric Contoller switch discovery

Sets `args.nxos_username` within scripts.

## Environment variables

Credentials can be set using the following environment variables.

### ND_DOMAIN

Nexus Dashboard login domain

### ND_IP4

Nexus Dashboard IPv4 address

### ND_PASSWORD

Nexus Dashboard password

### ND_USERNAME

Nexus Dashboard username

### NXOS_PASSWORD

Password for NX-OS switches.
Used for Nexus Dashboard Fabric Contoller switch discovery

### NXOS_USERNAME

Username for NX-OS switches.
Used for Nexus Dashboard Fabric Contoller switch discovery

## Ansible Vault

Lastly, for most example scripts, you can read the credentials from
an Ansible Vault.  See [Using Ansible Vault](using-ansible-vault.md)
for details around encrypting key/values in a vault.

To indicate to the script that an Ansible Vault should be used
as credential source, use the following command line argument.
It should point to a valid Ansible Vault file.

### --ansible-vault $HOME/.ansible/vault

``` bash "Use Ansible Vault as a credential source"
./my_script.py --ansible-vault $HOME/.ansible/vault
```

The credential names within the vault file must be as follows.

### nd_domain

Nexus Dashboard login domain.

### nd_ip4

Nexus Dashboard IPv4 address

### nd_password

Nexus Dashboard password

### nd_username

Nexus Dashboard username

### nxos_password

Password for NX-OS switches.
Used for Nexus Dashboard Fabric Contoller switch discovery

### nxos_username

Username for NX-OS switches.
Used for Nexus Dashboard Fabric Contoller switch discovery
