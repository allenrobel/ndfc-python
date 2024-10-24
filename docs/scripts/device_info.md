# device_info.py

## Description

Returns switch information.

## Usage

``` bash
./device_info.py --config config_device_info.yaml
```

## Example Config File

``` yaml
---
config:
  switch_ip4: 10.1.1.1
```

## Sample output

### Success

``` bash
(.venv) AROBEL-M-G793% ./device_info.py --config prod/config_device_info.yaml
fabric_name: f1
serial_number: FDO211229AH
status: ok
model: N9K-C93180YC-EX
(.venv) AROBEL-M-G793%
```

### Failure

``` bash
(.venv) AROBEL-M-G793% ./device_info.py --config prod/config_device_info.yaml
Unable to get switch details. Error details: SwitchDetails._get: Switch with ip_address 172.22.150.10 does not exist on the controller.
(.venv) AROBEL-M-G793%
```
