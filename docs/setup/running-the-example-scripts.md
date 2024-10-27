# Running the example scripts

An example configuration file for each script is located in
`examples/config/config_<script_name>`,

Some example configuration files contain only a subset of available parameters.
See the documention for the class a script uses for a (more or less) complete
listing of parameters.

```bash
export PYTHONPATH=${PYTHONPATH}:/path/to/this/repo/ndfc-python/lib
# optional - for Ansible Vault
# export NDFC_PYTHON_CONFIG=/path/to/ndfc-python-settings.yaml
# optional - to enable logging
# export NDFC_LOGGING_CONFIG=/path/to/ndfc-python-logging-config.json

py311) ~ % cd $HOME/ndfc-python/examples
(py311) examples % ./device_info.py --config config/config_device_info.yaml
```
