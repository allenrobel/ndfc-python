# device_info.py

## Description

Returns switch information for one or more switches.

## Example configuration file

``` yaml title="config/device_info.yaml"
---
config:
  - switch_ip4: 10.1.1.2
  - switch_ip4: 10.1.1.3
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
./device_info.py --config config/device_info.yaml
ipv4_address 10.1.1.2
  serial_number: FDO123456AB
  fabric_name: f1
  status: ok
  model: N9K-C93180YC-EX
ipv4_address 10.1.1.3
  serial_number: FDO123456BC
  fabric_name: f1
  status: ok
  model: N9K-C93180YC-EX
(.venv) AROBEL-M-G793%
```

## Sample failure output

### Switch does not exist

``` bash title="switch does not exist"
(.venv) AROBEL-M-G793% ./device_info.py --config prod/device_info.yaml
Unable to get switch details. Error details: SwitchDetails._get: Switch with ip_address 10.1.1.2 does not exist on the controller.
(.venv) AROBEL-M-G793%
```

### Invalid ip address in config file

``` bash title="Invalid switch_ip4 value in --config"
(.venv) AROBEL-M-G793% ./device_info.py --config prod/device_info.yaml
1 validation error for DeviceInfoConfigValidator
config.0.switch_ip4
  Input is not a valid IPv4 address [type=ip_v4_address, input_value='foo', input_type=str]
(.venv) AROBEL-M-G793%
```
