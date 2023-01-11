#!/usr/bin/env python
"""
Name: example_ndfc_load_config.py
Description:

Load the configuration file pointed to in lib/ndfc_python/ndfc_config.py
and print the parameters and values contained therein.

Usage:

Edit the config_file variable at the top of ndfc-python/lib/ndfc_python/ndfc_config.py
to point to your Ansible vault file
"""

from ndfc_python.ndfc_config import NdfcLoadConfig

c = NdfcLoadConfig()
print(f"c.ansible_vault {c.config['ansible_vault']}")
