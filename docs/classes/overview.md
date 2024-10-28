# Classes

``*`` indicates that a class has not yet been updated to work with RestSend().

Library                   | Description
--------------------------| -----------
[Log]                     | Create the base ndfc_python logging object
[AnsibleVaultCredentials] | Read an Ansible Vault and provide properties for credentials
[NdfcDiscover]            | Discover device
[NdfcPolicy]              | ``*`` Create / delete policies
[NdfcPythonLogger]        | Configure logging for ``ndfc-python`` scripts
[NdfcPythonSender]        | Instantiate and configure the Sender() class
[NdfcReachability]        | ``*`` Test switch reachability (from NDFC controller perspective).
[NetworkCreate]           | Create networks
[NetworkDelete]           | Delete networks
[ReadConfig]              | Returns the contents of a YAML file as a dictionary, given a path to the file
[VrfCreate]               | Create VRFs
[Validations]             | Validation methods used by the other classes (deprecated)
[YamlReader]              | Read a YAML file and return its contents as a python dict

[Log]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/log_v2.py
[AnsibleVaultCredentials]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ansible_vault_credentials.py
[NdfcDiscover]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_discover.py
[NdfcPolicy]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_policy.py
[NdfcPythonLogger]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_python_logger.py
[NdfcPythonSender]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_python_sender.py
[NdfcReachability]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_reachability.py
[NetworkCreate]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/network_create.py
[NetworkDelete]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/network_delete.py
[ReadConfig]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/read_config.py
[VrfCreate]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/vrf_create.py
[Validations]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/validations.py
[YamlReader]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/yaml_reader.py
