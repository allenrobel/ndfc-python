# Credentials

Credentials to access the Nexus Dashboard can be set in a few ways.

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

## Script command-line options

Script command line options, when available, override environment variables.

That is, if environment variables are set for ND_PASSWORD and ND_USERNAME,
you can override the password (while using the value of ND_USERNAME) with:

``` bash title="Override environment variable"
./script_name.py --nd_password MyNewPassword
```

### nd_domain

Nexus Dashboard login domain

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

## Ansible Vault

Lastly, for some example scripts, you can read the credentials from
an Ansible Vault.  See [Using Ansible Vault](using-ansible-vault.md)
