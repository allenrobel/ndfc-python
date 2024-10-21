#!/usr/bin/env python
"""
Name: load_config.py
Description:

Load the configuration file pointed to by the environment variable NDFC_CONFIG_FILE,
and print the parameters and values contained therein.
"""

from ndfc_python.ndfc_config import NdfcLoadConfig

c = NdfcLoadConfig()
print(f"c.ansible_vault {c.config['ansible_vault']}")
