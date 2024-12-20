# fabric_create.py

## Description

Create or update one or more fabrics.

## Example configuration file

Note, for a description of all configuration parameters for all fabric types
see [dcnm_fabric](https://allenrobel.github.io/dcnm-docpoc/modules/dcnm_fabric/).

``` yaml title="config/config_fabric_create.yaml"
---
config:
  - FABRIC_NAME: MyFabric
    FABRIC_TYPE: VXLAN_EVPN
    BGP_AS: 65002
    REPLICATION_MODE: Ingress
    VRF_VLAN_RANGE: 2000-2299
  - FABRIC_NAME: YourFabric
    FABRIC_TYPE: LAN_CLASSIC
```

## Example Usage

The example below uses environment variables for credentials, so requires
only the `--config` argument.  See [Running the Example Scripts]
for details around specifying credentials from the command line, from
environment variables, from Ansible Vault, or a combination of these
credentials sources.

[Running the Example Scripts]: ../setup/running-the-example-scripts.md

``` bash
export ND_DOMAIN=local
export ND_IP4=10.1.1.1
export ND_PASSWORD=MySecret
export ND_USERNAME=admin
./fabric_create.py --config config/config_fabric_create.yaml
# output not shown
```

## Example output

### Fabrics created successfully

``` bash title="Fabrics create success"
(.venv) AROBEL-M-G793% ./fabric_create.py --config prod/config_fabric_create.yaml
{
    "changed": true,
    "diff": [
        {
            "BGP_AS": 65002,
            "FABRIC_NAME": "MyFabric",
            "REPLICATION_MODE": "Ingress",
            "VRF_VLAN_RANGE": "2000-2299",
            "sequence_number": 1
        },
        {
            "FABRIC_NAME": "YourFabric",
            "sequence_number": 2
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "fabric_create",
            "check_mode": false,
            "sequence_number": 1,
            "state": "merged"
        },
        {
            "action": "fabric_create",
            "check_mode": false,
            "sequence_number": 2,
            "state": "merged"
        }
    ],
    "response": [
        {
            "DATA": {
                "removed": "for brevity"
            },
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/MyFabric/Easy_Fabric",
            "RETURN_CODE": 200,
            "sequence_number": 1
        },
        {
            "DATA": {
                "removed": "for brevity"
            },
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/YourFabric/LAN_Classic",
            "RETURN_CODE": 200,
            "sequence_number": 2
        }
    ],
    "result": [
        {
            "changed": true,
            "sequence_number": 1,
            "success": true
        },
        {
            "changed": true,
            "sequence_number": 2,
            "success": true
        }
    ]
}
(.venv) AROBEL-M-G793%
```

### Fabrics already exist, and no changes are required

``` bash title="Fabrics do not require changes"
(.venv) AROBEL-M-G793% ./fabric_create.py --ansible-vault $HOME/.ansible/vault --config prod/config_fabric_create.yaml
Vault password:
{
    "changed": false,
    "diff": [
        {
            "sequence_number": 1
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "fabric_update",
            "check_mode": false,
            "sequence_number": 1,
            "state": "merged"
        }
    ],
    "response": [
        {
            "MESSAGE": "No fabrics to update for merged state.",
            "RETURN_CODE": 200,
            "sequence_number": 1
        }
    ],
    "result": [
        {
            "changed": false,
            "sequence_number": 1,
            "success": true
        }
    ]
}
(.venv) AROBEL-M-G793%
```

### Fabric already exists, but requires changes to align with user's config

Below, we have changed ``REPLICATION_MODE`` and `BGP_AS` for fabric `MyFabric`
Since `SITE_ID`, by default, is assigned the value of `BGP_AS`, we need to change
it as well if we want it to be in sync with `BGP_AS`

``` yaml title="config/config_fabric_create.yaml"
---
config:
  - FABRIC_NAME: MyFabric
    FABRIC_TYPE: VXLAN_EVPN
    BGP_AS: 65004
    SITE_ID: 65004
    REPLICATION_MODE: Multicast
    VRF_VLAN_RANGE: 2000-2299
  - FABRIC_NAME: YourFabric
    FABRIC_TYPE: LAN_CLASSIC
```

``` bash title="User config changed some MyFabric parameters"
{
    "changed": true,
    "diff": [
        {
            "BGP_AS": "65004",
            "FABRIC_NAME": "MyFabric",
            "REPLICATION_MODE": "Multicast",
            "SITE_ID": "65004",
            "sequence_number": 1
        },
        {
            "sequence_number": 2
        },
        {
            "sequence_number": 3
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "fabric_update",
            "check_mode": false,
            "sequence_number": 1,
            "state": "merged"
        },
        {
            "action": "config_save",
            "check_mode": false,
            "sequence_number": 2,
            "state": "merged"
        },
        {
            "action": "config_deploy",
            "check_mode": false,
            "sequence_number": 3,
            "state": "merged"
        }
    ],
    "response": [
        {
            "DATA": {
                "removed": "for_brevity"
            },
            "MESSAGE": "OK",
            "METHOD": "PUT",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/MyFabric/Easy_Fabric",
            "RETURN_CODE": 200,
            "sequence_number": 1
        },
        {
            "MESSAGE": "Fabric MyFabric DEPLOY is False or None. Skipping config-save.",
            "RETURN_CODE": 200,
            "sequence_number": 2
        },
        {
            "MESSAGE": "FabricConfigDeploy._can_fabric_be_deployed: Fabric MyFabric DEPLOY is False or None. Skipping config-deploy.",
            "RETURN_CODE": 200,
            "sequence_number": 3
        }
    ],
    "result": [
        {
            "changed": true,
            "sequence_number": 1,
            "success": true
        },
        {
            "changed": true,
            "sequence_number": 2,
            "success": true
        },
        {
            "changed": true,
            "sequence_number": 3,
            "success": true
        }
    ]
}
```
