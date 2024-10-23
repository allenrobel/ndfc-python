# Running the example scripts

```bash
export PYTHONPATH=${PYTHONPATH}:/path/to/this/repo/ndfc-python/lib
# optional - for Ansible Vault
# export NDFC_PYTHON_CONFIG=/path/to/ndfc-python-settings.yaml
# optional - to enable logging
# export NDFC_LOGGING_CONFIG=/path/to/ndfc-python-logging-config.json

py311) ~ % cd $HOME/ndfc-python/examples
(py311) examples % ./device_info.py --config config_device_info.yaml
```
