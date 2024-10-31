# Running the example scripts

An example configuration file for each script is located in
`examples/config/config_<script_name>`,

Some example configuration files contain only a subset of available parameters.
See the documention for the class a script uses for a (more or less) complete
listing of parameters.

## Example script invocation

### Using the command line for all credentials

``` bash title="Using command line arguments"
export PYTHONPATH=${PYTHONPATH}:/path/to/this/repo/ndfc-python/lib
# optional - to enable logging
# export NDFC_LOGGING_CONFIG=/path/to/ndfc-python-logging-config.json

py311) ~ % cd $HOME/ndfc-python/examples
(py311) examples % ./device_info.py --config config/config_device_info.yaml --nd-password MyNdPassword --nd-username admin --nd-domain local --nd-ip4 10.1.1.1
```

### Using a combination of command line and environment variables for credentials

``` bash title="Using command line and environment"
export PYTHONPATH=${PYTHONPATH}:/path/to/this/repo/ndfc-python/lib
export ND_PASSWORD=MyNdPassword
export ND_DOMAIN=local

py311) ~ % cd $HOME/ndfc-python/examples
(py311) examples % ./device_info.py --config config/config_device_info.yaml --nd-username admin --nd-ip4 10.1.1.1
```

### Using a combination of command line, environment variables, and Ansible Vault for credentials

Below, we assume that `$HOME/.ansible/vault` contains `nd_password` and `nd_domain`.

``` bash title="Using command line and environment"
export PYTHONPATH=${PYTHONPATH}:/path/to/this/repo/ndfc-python/lib
export ND_IP4=10.1.1.1

py311) ~ % cd $HOME/ndfc-python/examples
(py311) examples % ./device_info.py --config config/config_device_info.yaml --nd-username admin --ansible-vault $HOME/.ansible/vault
```

## See also

[List of ndfc-python credentials](./set-credentials.md)
[Using Ansible Vault](./using-ansible-vault.md)
