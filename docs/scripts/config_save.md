# config_save.py

## Description

Save pending configurations for one or more fabrics.

## Example configuration file

Note, if you are running this script in a multi-site environment,
always list the child fabrics first, followed by the parent fabric.

The example below shows this scenario.

``` yaml title="config/config_config_save.yaml"
---
config:
  - fabric_name: ChildFabric1
  - fabric_name: ChildFabric2
  - fabric_name: MSDFabric
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
./config_save.py --config config/config_config_save.yaml
# output not shown
```

## Example output

### Success

``` bash title="Configurations saved successfully"
(ndfc-python) arobel@Allen-M4 examples % ./config_save.py --config test_config_save.yaml --loglevel DEBUG
Triggered Config Save for fabric 'SITE2':
{
    "RETURN_CODE": 200,
    "DATA": {
        "status": "Config save is completed"
    },
    "MESSAGE": "OK",
    "METHOD": "POST",
    "REQUEST_PATH": "https://192.168.7.7/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/SITE2/config-save"
}
Triggered Config Save for fabric 'MSD':
{
    "RETURN_CODE": 200,
    "DATA": {
        "status": "Config save is completed"
    },
    "MESSAGE": "OK",
    "METHOD": "POST",
    "REQUEST_PATH": "https://192.168.7.7/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/MSD/config-save"
}
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure

TODO: Add failer case
