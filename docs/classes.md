# Classes

``*`` indicates that a class has not yet been updated to work with RestSend().

Library                 | Description
----------------------- | -----------
[Log]                   | Create the base ndfc_python logging object
[NdfcCredentials]       | Read the caller's Ansible Vault and provides the credentials therein to the other libraries
[NdfcDeviceInfo]        | Retrieve information about a switch
[NdfcDiscover]          | Discover device
[NdfcNetwork]           | ``*`` Create, delete networks
[NdfcPolicy]            | ``*`` Create / delete policies
[NdfcPythonConfig]      | Returns the contents of a YAML file as a dictionary, given a path to the file
[NdfcPythonLogger]      | Configure logging for ``ndfc-python`` scripts
[NdfcPythonSender]      | Instantiate and configure the Sender() class
[NdfcReachability]      | ``*`` Test switch reachability (from NDFC controller perspective).
[VrfCreate]             | Create VRFs
[Validations]           | Validation methods used by the other classes (deprecated)
[Validations]           | Read a YAML file and return its contents as a python dict

[Log]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/log_v2.py
[NdfcCredentials]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_credentials.py
[NdfcDeviceInfo]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_device_info.py
[NdfcDiscover]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_discover.py  
[NdfcNetwork]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_network.py
[NdfcPolicy]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_policy.py
[NdfcPythonConfig]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_python_config.py
[NdfcPythonLogger]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_python_logger.py
[NdfcPythonSender]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_python_sender.py
[NdfcReachability]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_reachability.py
[VrfCreate]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/vrf_create.py
[Validations]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/validations.py
[YamlReader]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/yaml_reader.py

