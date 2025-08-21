# maintenance_mode_info.py

## Description

Enable or disable maintenance mode on one or more switches.

## Example configuration file

``` yaml title="config/maintenance_mode_info.yaml"
---
config:
    - ip_address: 10.1.1.2
    - ip_address: 10.1.1.3
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
./maintenance_mode_info.py --config config/maintenance_mode_info.yaml
# output not shown
```

## Example output

### Success

``` bash title="Successful query for two switches"
(.venv) AROBEL-M-G793% ./maintenance_mode_info.py --config prod/maintenance_mode_info.yaml
{
    "changed": false,
    "diff": [
        {
            "10.1.1.2": {
                "fabric_deployment_disabled": false,
                "fabric_freeze_mode": false,
                "fabric_name": "f1",
                "fabric_read_only": false,
                "ip_address": "10.1.1.2",
                "mode": "normal",
                "role": "spine",
                "serial_number": "FOX5678EFGH"
            },
            "10.1.1.3": {
                "fabric_deployment_disabled": false,
                "fabric_freeze_mode": false,
                "fabric_name": "f1",
                "fabric_read_only": false,
                "ip_address": "10.1.1.3",
                "mode": "maintenance",
                "role": "spine",
                "serial_number": "FOX5678EFGH"
            },
            "sequence_number": 1
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "maintenance_mode_info",
            "check_mode": false,
            "sequence_number": 1,
            "state": null
        }
    ],
    "response": [
        {
            "MESSAGE": "MaintenanceModeInfo OK.",
            "METHOD": "NA",
            "REQUEST_PATH": "NA",
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

### Switch does not exist on the controller

``` bash title="Switch does not exist"
(.venv) AROBEL-M-G793% ./maintenance_mode_info.py --config prod/maintenance_mode_info.yaml
Exiting.  Error detail: Query.commit: Error while retrieving switch information from the controller. Error detail: Query.get_have: Error while retrieving switch info. Error detail: SwitchDetails._get: Switch with ip_address 10.1.1.8 does not exist on the controller.
(.venv) AROBEL-M-G793%
```

### Invalid config file

``` bash title="config file contains incorrect value for ip_address"
(.venv) AROBEL-M-G793% ./maintenance_mode_info.py --config prod/maintenance_mode_info.yaml
1 validation error for MaintenanceModeInfoConfigValidator
config.0.ip_address
  Input is not a valid IPv4 address [type=ip_v4_address, input_value='foo', input_type=str]
(.venv) AROBEL-M-G793%
```
