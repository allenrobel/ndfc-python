# Classes

As we work to modify code in the `ansible-dcnm` repository to remove direct
dependencies on Ansible, we will leverage that code here.  `ndfc-python`
serves secondarily as a testing ground for new code that may eventually
find its way into `ansible-dcnm`.  The code behind the `dcnm_network`,
`dcnm_vrf`, and `dcnm_policy` Ansible modules is currently tied at the
hip to Ansible, so we are currently unable to leverage it.  We're using
the libraries below for now.

``*`` indicates that a class has not yet been updated to work with RestSend().

Library                   | Description
--------------------------| -----------
[CredentialsAnsibleVault] | Read an Ansible Vault and provide properties for credentials
[Log]                     | Create the base ndfc_python logging object
[NdfcDiscover]            | Discover device
[NdfcPolicy]              | ``*`` Create / delete policies
[NdfcPythonLogger]        | Configure logging for ``ndfc-python`` scripts
[NdfcPythonSender]        | Instantiate and configure the Sender() class
[NetworkCreate]           | Create networks
[NetworkDelete]           | Delete networks
[Reachability]            | Switch reachability information (from controller perspective).
[ReadConfig]              | Returns the contents of a YAML file as a dictionary, given a path to the file
[VrfCreate]               | Create VRFs
[Validations]             | Validation methods used by the other classes (deprecated)
[YamlReader]              | Read a YAML file and return its contents as a python dict

[CredentialsAnsibleVault]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/credentials/credentials_ansible_vault.py
[Log]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/log_v2.py
[NdfcDiscover]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_discover.py
[NdfcPolicy]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_policy.py
[NdfcPythonLogger]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_python_logger.py
[NdfcPythonSender]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_python_sender.py
[NetworkCreate]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/network_create.py
[NetworkDelete]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/network_delete.py
[Reachability]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/reachability.py
[ReadConfig]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/read_config.py
[VrfCreate]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/vrf_create.py
[Validations]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/validations.py
[YamlReader]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/yaml_reader.py
