# device_info.py

## Description

Returns switch information for one or more switches.

## Usage

``` bash
./device_info.py --config config/config_device_info.yaml
```

## Example Config File

``` yaml title="config/config_device_info.yaml"
---
config:
  - switch_ip4: 10.1.1.1
  - switch_ip4: 10.1.1.2
```

## Sample output

### Success

``` bash title="Success"
(.venv) AROBEL-M-G793% ./device_info.py --config prod/config_device_info.yaml
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

### Failure - switch does not exist

``` bash title="switch does not exist"
(.venv) AROBEL-M-G793% ./device_info.py --config prod/config_device_info.yaml
Unable to get switch details. Error details: SwitchDetails._get: Switch with ip_address 10.1.1.4 does not exist on the controller.
(.venv) AROBEL-M-G793%
```
