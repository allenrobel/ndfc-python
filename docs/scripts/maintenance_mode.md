# maintenance_mode.py

## Description

Enable or disable maintenance mode on one or more switches.

## Example configuration file

``` yaml title="config/config_maintenance_mode.yaml"
---
config:
    - ip_address: 10.1.1.2
      deploy: true
      wait_for_mode_change: true
      mode: maintenance
    - ip_address: 10.1.1.3
      deploy: true
      wait_for_mode_change: true
      mode: normal
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
./maintenance_mode.py --config config/config_maintenance_mode.yaml
# output not shown
```

## Example output

### Success

``` bash title="Successful mode change for two switches"
(.venv) AROBEL-M-G793% ./maintenance_mode.py --config prod/config_maintenance_mode.yaml
Maintenance mode change can take up to 5 minutes. Patience is a virtue.
{
    "changed": true,
    "diff": [
        {
            "fabric_name": "f1",
            "ip_address": "10.1.1.2",
            "maintenance_mode": "maintenance",
            "sequence_number": 1,
            "serial_number": "FOX1234ABCD"
        },
        {
            "fabric_name": "f1",
            "ip_address": "10.1.1.3",
            "maintenance_mode": "normal",
            "sequence_number": 2,
            "serial_number": "FOX5678EFGH"
        },
        {
            "10.1.1.2": "10.1.1.2",
            "deploy_maintenance_mode": true,
            "sequence_number": 3
        },
        {
            "10.1.1.3": "10.1.1.3",
            "deploy_maintenance_mode": true,
            "sequence_number": 4
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "change_sytem_mode",
            "check_mode": false,
            "sequence_number": 1,
            "state": "merged"
        },
        {
            "action": "change_sytem_mode",
            "check_mode": false,
            "sequence_number": 2,
            "state": "merged"
        },
        {
            "action": "deploy_maintenance_mode",
            "check_mode": false,
            "sequence_number": 3,
            "state": "merged"
        },
        {
            "action": "deploy_maintenance_mode",
            "check_mode": false,
            "sequence_number": 4,
            "state": "merged"
        }
    ],
    "response": [
        {
            "DATA": {
                "status": "Success"
            },
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/switches/FOX1234ABCD/maintenance-mode",
            "RETURN_CODE": 200,
            "sequence_number": 1
        },
        {
            "DATA": {
                "status": "Success"
            },
            "MESSAGE": "OK",
            "METHOD": "DELETE",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/switches/FOX5678EFGH/maintenance-mode",
            "RETURN_CODE": 200,
            "sequence_number": 2
        },
        {
            "DATA": {
                "status": "Success"
            },
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/switches/FOX1234ABCD/deploy-maintenance-mode?waitForModeChange=true",
            "RETURN_CODE": 200,
            "sequence_number": 3
        },
        {
            "DATA": {
                "status": "Success"
            },
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/switches/FOX5678EFGH/deploy-maintenance-mode?waitForModeChange=true",
            "RETURN_CODE": 200,
            "sequence_number": 4
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
        }
    ]
}
(.venv) AROBEL-M-G793%
```

### Script is run when no changes are needed

``` bash title="Controller state already matches configuration file."
(.venv) AROBEL-M-G793% ./maintenance_mode.py --config prod/config_maintenance_mode.yaml
{
    "changed": false,
    "diff": [],
    "failed": false,
    "metadata": [],
    "response": [],
    "result": []
}
(.venv) AROBEL-M-G793%
```

### Switch does not exist on the controller

``` bash title="Switch does not exist"
(.venv) AROBEL-M-G793% ./maintenance_mode.py --config prod/config_maintenance_mode.yaml
Exiting.  Error detail: Merged.get_have: Error while retrieving switch info. Error detail: SwitchDetails._get: Switch with ip_address 10.1.1.8 does not exist on the controller.
(.venv) AROBEL-M-G793%
```
