# [controller_info.py]

[controller_info.py]: https://github.com/allenrobel/ndfc-python/blob/main/examples/controller_info.py

## Description

Return controller information (version, etc).

## Usage

1. See credentials.py for various options to set credentials.
2. Run the script (we're using command-line for credentials below).

``` bash
./controller_info.py --nd_username admin --nd_password MyPassword --nd_domain local --nd_ip4 10.1.1.1
```

## Output

``` bash

arobel@AROBEL-M-G793 examples % ./controller_version.py --nd-domain local --nd-ip4 10.1.1.1 --nd-password MyPassword --nd-username admin
Controller information:
12.2.2.238      Full version
12              Major version
2               Minor version
2               Patch version
False           Development version
LAN             Mode
False           Upgrade in progress
False           Media Controller
False           High Availability enabled
EASYFABRIC      Install
Raw response:
{
    "dev": false,
    "install": "EASYFABRIC",
    "isHaEnabled": false,
    "isMediaController": false,
    "is_upgrade_inprogress": false,
    "mode": "LAN",
    "uuid": "",
    "version": "12.2.2.238"
}
```
