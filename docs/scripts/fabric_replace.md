# fabric_replace.py

## Description

Replace the configuration for one or more fabrics.

## Example configuration file

Note, for a description of all configuration parameters for all fabric types
see [dcnm_fabric](https://allenrobel.github.io/dcnm-docpoc/modules/dcnm_fabric/).

``` yaml title="config/config_fabric_replace.yaml"
---
config:
  - FABRIC_NAME: MyFabric
    FABRIC_TYPE: VXLAN_EVPN
    BGP_AS: 65002
    REPLICATION_MODE: Ingress
  - FABRIC_NAME: YourFabric
    FABRIC_TYPE: LAN_Classic
    IS_READ_ONLY: False
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
./fabric_replace.py --config config/config_fabric_replace.yaml
# output not shown
```

## Example output

### Fabric configurations replaced successfully

``` yaml title="config/config_fabric_replace.yaml"
---
config:
  - FABRIC_NAME: MyFabric
    FABRIC_TYPE: VXLAN_EVPN
    BGP_AS: 65002
    REPLICATION_MODE: Multicast
  - FABRIC_NAME: YourFabric
    FABRIC_TYPE: LAN_Classic
    IS_READ_ONLY: False
```

``` bash title="Fabric configuration replace success"
(.venv) AROBEL-M-G793% ./fabric_replace.py --ansible-vault $HOME/.ansible/vault --config prod/config_fabric_create.yaml
Vault password:
{
    "changed": true,
    "diff": [
        {
            "FABRIC_NAME": "MyFabric",
            "REPLICATION_MODE": "Multicast",
            "sequence_number": 1
        },
        {
            "FABRIC_NAME": "YourFabric",
            "IS_READ_ONLY": "false",
            "sequence_number": 2
        },
        {
            "sequence_number": 3
        },
        {
            "sequence_number": 4
        },
        {
            "sequence_number": 5
        },
        {
            "sequence_number": 6
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "fabric_replace",
            "check_mode": false,
            "sequence_number": 1,
            "state": "replaced"
        },
        {
            "action": "fabric_replace",
            "check_mode": false,
            "sequence_number": 2,
            "state": "replaced"
        },
        {
            "action": "config_save",
            "check_mode": false,
            "sequence_number": 3,
            "state": "replaced"
        },
        {
            "action": "config_save",
            "check_mode": false,
            "sequence_number": 4,
            "state": "replaced"
        },
        {
            "action": "config_deploy",
            "check_mode": false,
            "sequence_number": 5,
            "state": "replaced"
        },
        {
            "action": "config_deploy",
            "check_mode": false,
            "sequence_number": 6,
            "state": "replaced"
        }
    ],
    "response": [
        {
            "DATA": {
                "removed": "for brevity"
            },
            "MESSAGE": "OK",
            "METHOD": "PUT",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/MyFabric/Easy_Fabric",
            "RETURN_CODE": 200,
            "sequence_number": 1
        },
        {
            "DATA": {
                "removed": "for brevity"
            },
            "MESSAGE": "OK",
            "METHOD": "PUT",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/YourFabric/LAN_Classic",
            "RETURN_CODE": 200,
            "sequence_number": 2
        },
        {
            "MESSAGE": "Fabric MyFabric DEPLOY is False or None. Skipping config-save.",
            "RETURN_CODE": 200,
            "sequence_number": 3
        },
        {
            "MESSAGE": "Fabric YourFabric DEPLOY is False or None. Skipping config-save.",
            "RETURN_CODE": 200,
            "sequence_number": 4
        },
        {
            "MESSAGE": "FabricConfigDeploy._can_fabric_be_deployed: Fabric MyFabric DEPLOY is False or None. Skipping config-deploy.",
            "RETURN_CODE": 200,
            "sequence_number": 5
        },
        {
            "MESSAGE": "FabricConfigDeploy._can_fabric_be_deployed: Fabric YourFabric DEPLOY is False or None. Skipping config-deploy.",
            "RETURN_CODE": 200,
            "sequence_number": 6
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
        },
        {
            "changed": true,
            "sequence_number": 4,
            "success": true
        },
        {
            "changed": true,
            "sequence_number": 5,
            "success": true
        },
        {
            "changed": true,
            "sequence_number": 6,
            "success": true
        }
    ]
}
```

### No changes are required

``` bash title="Fabrics do not require changes"
(.venv) AROBEL-M-G793% ./fabric_replace.py --ansible-vault $HOME/.ansible/vault --config prod/config_fabric_replace.yaml
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
            "action": "fabric_replace",
            "check_mode": false,
            "sequence_number": 1,
            "state": "replaced"
        }
    ],
    "response": [
        {
            "MESSAGE": "No fabrics to update for replaced state.",
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

### Fabric requires changes to align with user's config

Below, we have changed ``REPLICATION_MODE`` for `MyFabric` and
`IS_READ_ONLY` for `YourFabric`

``` yaml title="config/config_fabric_replace.yaml"
---
config:
  - FABRIC_NAME: MyFabric
    REPLICATION_MODE: Multicast
    FABRIC_TYPE: VXLAN_EVPN
    BGP_AS: 65002
    DEPLOY: False
  - FABRIC_NAME: YourFabric
    FABRIC_TYPE: LAN_CLASSIC
    IS_READ_ONLY: True
    DEPLOY: False
```

``` bash title="User config changed some MyFabric parameters"
{
    "changed": true,
    "diff": [
        {
            "FABRIC_NAME": "MyFabric",
            "REPLICATION_MODE": "Multicast",
            "sequence_number": 1
        },
        {
            "FABRIC_NAME": "YourFabric",
            "IS_READ_ONLY": "true",
            "sequence_number": 2
        },
        {
            "sequence_number": 3
        },
        {
            "sequence_number": 4
        },
        {
            "sequence_number": 5
        },
        {
            "sequence_number": 6
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "fabric_replace",
            "check_mode": false,
            "sequence_number": 1,
            "state": "replaced"
        },
        {
            "action": "fabric_replace",
            "check_mode": false,
            "sequence_number": 2,
            "state": "replaced"
        },
        {
            "action": "config_save",
            "check_mode": false,
            "sequence_number": 3,
            "state": "replaced"
        },
        {
            "action": "config_save",
            "check_mode": false,
            "sequence_number": 4,
            "state": "replaced"
        },
        {
            "action": "config_deploy",
            "check_mode": false,
            "sequence_number": 5,
            "state": "replaced"
        },
        {
            "action": "config_deploy",
            "check_mode": false,
            "sequence_number": 6,
            "state": "replaced"
        }
    ],
    "response": [
        {
            "DATA": {
                "removed": "for brevity"
            },
            "MESSAGE": "OK",
            "METHOD": "PUT",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/MyFabric/Easy_Fabric",
            "RETURN_CODE": 200,
            "sequence_number": 1
        },
        {
            "DATA": {
                "removed": "for brevity"
            },
            "MESSAGE": "OK",
            "METHOD": "PUT",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/YourFabric/LAN_Classic",
            "RETURN_CODE": 200,
            "sequence_number": 2
        },
        {
            "MESSAGE": "Fabric MyFabric DEPLOY is False or None. Skipping config-save.",
            "RETURN_CODE": 200,
            "sequence_number": 3
        },
        {
            "MESSAGE": "Fabric YourFabric DEPLOY is False or None. Skipping config-save.",
            "RETURN_CODE": 200,
            "sequence_number": 4
        },
        {
            "MESSAGE": "FabricConfigDeploy._can_fabric_be_deployed: Fabric MyFabric DEPLOY is False or None. Skipping config-deploy.",
            "RETURN_CODE": 200,
            "sequence_number": 5
        },
        {
            "MESSAGE": "FabricConfigDeploy._can_fabric_be_deployed: Fabric YourFabric DEPLOY is False or None. Skipping config-deploy.",
            "RETURN_CODE": 200,
            "sequence_number": 6
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
        },
        {
            "changed": true,
            "sequence_number": 4,
            "success": true
        },
        {
            "changed": true,
            "sequence_number": 5,
            "success": true
        },
        {
            "changed": true,
            "sequence_number": 6,
            "success": true
        }
    ]
}
(.venv) AROBEL-M-G793%
```
