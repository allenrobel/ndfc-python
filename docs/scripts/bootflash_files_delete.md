# bootflash_files_delete.py

## Description

Delete files from flash devices on one or more switches.

## Configuration parameters

### targets

A list of dictionaries containing the keys `filepath` and `supervisor`

#### filepath

Can be any file glob (obviously, some are dangerous!).

##### filepath examples

- `*:/*.txt` delete all `.txt` files from all flash devices on the specified supervisor
-  `bootflash:/scanner-202411??.log` delete all scanner log files whose name implies Nov 20224

#### supervisor

The supervisor containing the filepath.  Can be one of `active` or `standby`.

### switches

A list of switch ipv4 addresses.

## Example configuration file

The configuration below deletes all files with `.log` and `.yaml` extensions
from the bootflash device on the active supervisor of switches 10.1.1.2 and
10.1.1.3.

The configuration file structure is identical to [bootflash_files_info](./bootflash_files_info.md)

``` yaml title="config/config_bootflash_files_delete.yaml"
---
config:
  targets:
    - filepath: bootflash:/*.log
      supervisor: active
    - filepath: bootflash:/*.yaml
      supervisor: active
  switches:
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
./bootflash_files_delete.py --config config/config_bootflash_files_delete.yaml
# output not shown
```

## Example output

### Files deleted successfully

``` bash title="Successful deletion"
(.venv) arobel@AROBEL-M-G793 examples % ./bootflash_files_delete.py --config prod/config_bootflash_files_delete.yaml
{
    "changed": true,
    "diff": [
        {
            "10.1.1.2": [
                {
                    "date": "2024-09-27 18:56:03",
                    "device_name": "cvd-1313-leaf",
                    "filepath": "bootflash:/log_profile.yaml",
                    "ip_address": "10.1.1.2",
                    "serial_number": "FDO123456AB",
                    "size": "2566",
                    "supervisor": "active"
                }
            ],
            "10.1.1.3": [
                {
                    "date": "2024-09-27 18:56:14",
                    "device_name": "cvd-1314-leaf",
                    "filepath": "bootflash:/log_profile.yaml",
                    "ip_address": "10.1.1.3",
                    "serial_number": "FDO123456BC",
                    "size": "2468",
                    "supervisor": "active"
                }
            ],
            "sequence_number": 1
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "bootflash_delete",
            "check_mode": false,
            "sequence_number": 1,
            "state": "deleted"
        }
    ],
    "response": [
        {
            "DATA": "File(s) Deleted Successfully. \nDeleted files: [log_profile.yaml][log_profile.yaml]",
            "MESSAGE": "OK",
            "METHOD": "DELETE",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/imagemgnt/bootFlash/bootflash-files",
            "RETURN_CODE": 200,
            "sequence_number": 1
        }
    ],
    "result": [
        {
            "changed": true,
            "sequence_number": 1,
            "success": true
        }
    ]
}
```

### Switch does not exist on the controller

``` bash title="Switch does not exist on the controller"
(.venv) arobel@AROBEL-M-G793 examples % ./bootflash_files_delete.py --config config/config_bootflash_files_delete.yaml
Exiting.  Error detail: BootflashInfo.refresh_bootflash_info: serial_number not found for switch 10.1.1.2. Error detail SwitchDetails._get: Switch with ip_address 10.1.1.2 does not exist on the controller.
(.venv) arobel@AROBEL-M-G793 examples %
```

### Files not found

``` bash title="Files not found"
(.venv) arobel@AROBEL-M-G793 examples % ./bootflash_files_delete.py --config prod/config_bootflash_files_delete.yaml
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
            "action": "bootflash_delete",
            "check_mode": false,
            "sequence_number": 1,
            "state": "deleted"
        }
    ],
    "response": [
        {
            "MESSAGE": "No files to delete.",
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
```
