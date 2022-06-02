#!/usr/bin/env python
# Edit the config_file variable at the top of ndfc-python/ndfc_lib/ndfc_config.py 
# to point to your Ansible vault file

from ndfc_lib.ndfc_config import NdfcLoadConfig

c = NdfcLoadConfig()
print('c.ansible_vault {}'.format(c.config['ansible_vault']))
