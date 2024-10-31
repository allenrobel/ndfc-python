# [credentials.py]

[credentials.py]: https://github.com/allenrobel/ndfc-python/blob/main/examples/credentials.py

## Description

Print the credentials that would be used from the hierarchy of credential
sources that `ndfc-python` scripts traverse.

## Credentials hierarchy and precedence

For details around `ndfc-python`'s credentials hierarchy and precedence, and
the credential names used, see [Credentials](../setup/set-credentials.md).

## Example Usage

### Mix of credential sources

Below, the `NXOS_USERNAME` environment variable is set, so its value
is used unless overridden by the command line.  In this case, we can
omit `--nxos-username` from the command line.

``` bash title="Mix of command line args and enviroment variables"
(.venv) AROBEL-M-G793% export NXOS_USERNAME=admin
(.venv) AROBEL-M-G793% ./credentials.py \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password foo \
    --nd-username admin \
    --nxos-password bar
The following credentials would be used:
  nd_domain local
  nd_ip4 10.1.1.1
  nd_password foo
  nd_username admin
  nxos_password bar
  nxos_username admin
```

### Overriding a lower precedence credential

Below, we override the `NXOS_USERNAME` environment variable with its
corresponding (higher precedence) command line argument:

``` bash title="Override environment variable"
(.venv) AROBEL-M-G793% export NXOS_USERNAME=admin
(.venv) AROBEL-M-G793% ./credentials.py \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password foo \
    --nd-username admin \
    --nxos-password bar \
    --nxos-username beeblebrox
The following credentials would be used:
  nd_domain local
  nd_ip4 10.1.1.1
  nd_password foo
  nd_username admin
  nxos_password bar
  nxos_username beeblebrox
```

Below, we unset `NXOS_USERNAME` and point to an Ansible Vault file
which contains all of the credentials that `ndfc-python` knows about.
The Ansible vault file is the lowest precedence source of credentials
but, since we haven't specified any command-line credentials, and no
environment variables are set, the Ansible Vault file is used.

Notice that the script asks for the Ansible Vault password to that
it can read the vault.

```bash
(.venv) AROBEL-M-G793% unset NXOS_USERNAME
(.venv) AROBEL-M-G793% ./credentials.py --ansible-vault $HOME/.ansible/vault
Vault password:
The following credentials would be used:
  nd_domain local
  nd_ip4 10.2.1.1
  nd_password FooPassword
  nd_username admin
  nxos_password BarPassword
  nxos_username admin
(.venv) AROBEL-M-G793%
```

### Failure - Ansible Vault missing expected content

Below, we are pointing `--ansible-vault` at a file that does not contain the expected
credential names.

``` bash
(.venv) AROBEL-M-G793% ./credentials.py --ansible-vault $HOME/.ansible/vault
Vault password:
CredentialsAnsibleVault.commit: Exiting. ansible_vault is missing key nd_password. vault file: /Users/arobel/.ansible/vault
(.venv) AROBEL-M-G793%
```

### Failure - Ansible Vault file is missing

Below, we are pointing `--ansible-vault` at a file that does not exist.

``` bash
(.venv) AROBEL-M-G793% ./credentials.py --ansible-vault /tmp/no_files_here
Vault password:
CredentialsAnsibleVault.commit: Exiting. Unable to load credentials in  /tmp/no_files_here. Exception detail: Unable to retrieve file contents
Could not find or access '/tmp/no_files_here' on the Ansible Controller.
If you are using a module and expect the file to exist on the remote, see the remote_src option
(.venv) AROBEL-M-G793%
```
