# Classes

Classes marked with ``*`` are not yet updated to use RestSend.

Library                 | Description
----------------------- | -----------
[log_v2]                | Create the base ndfc_python logging object.
[ndfc_config]           | Load YAML file pointed to by --config command-line option
[ndfc_credentials]      | Read the caller's Ansible Vault and provides the credentials therein to the other libraries
[ndfc_device_info]      | Retrieve device information
[ndfc_discover]         | Discover device
[ndfc_network]          | Create, delete networks ``*``
[ndfc_policy]           | Create / delete policies ``*``
[ndfc_reachability]     | Test for device reachability (from NDFC perspective)
[vrf_create]            | Create VRFs
[validations]           | Validation methods used by the other classes

[log_v2]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/log_v2.py
[ndfc_config]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_config.py
[ndfc_credentials]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_credentials.py
[ndfc_device_info]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_device_info.py
[ndfc_discover]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_discover.py
[ndfc_network]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_network.py
[ndfc_policy]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_policy.py
[ndfc_reachability]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/ndfc_reachability.py
[vrf_create]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/vrf_create.py
[validations]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/validations.py
