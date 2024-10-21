# Classes

Library                 | Description
----------------------- | -----------
[ndfc]                  | Methods to login to an NDFC controller and perform get, post, delete operations
[ndfc_config]           | Loads the config file which all libraries reference
[ndfc_credentials]      | Read the caller's Ansible Vault and provides the credentials therein to the other libraries
[ndfc_device_info]      | Retrieve device information
[ndfc_discover]         | Discover device
[ndfc_network]          | Create, delete networks
[ndfc_policy]           | Create / delete policies
[ndfc_reachability]     | Test for device reachability (from NDFC perspective)
[vrf_create]            | Create VRFs
[validations]           | Validation methods used by the other classes

[ndfc]: blob/main/lib/ndfc_python/ndfc.py
[ndfc_config]: blob/main/lib/ndfc_python/ndfc_config.py
[ndfc_credentials]: blob/main/lib/ndfc_python/ndfc_credentials.py
[ndfc_device_info]: blob/main/lib/ndfc_python/ndfc_device_info.py
[ndfc_discover]: blob/main/lib/ndfc_python/ndfc_discover.py
[ndfc_network]: blob/main/lib/ndfc_python/ndfc_network.py
[ndfc_policy]: main/lib/ndfc_python/ndfc_policy.py
[ndfc_reachability]: blob/main/lib/ndfc_python/ndfc_reachability.py
[vrf_create]: blob/main/lib/ndfc_python/vrf_create.py
[validations]: blob/main/lib/ndfc_python/validations.py
