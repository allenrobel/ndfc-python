# bootflash_files_info.py

## Description

List files from flash devices on one or more switches.

## Example configuration file

The configuration below lists all files with `.log` and `.yaml` extensions
from the bootflash device on the active supervisor of switches 10.1.1.2 and
10.1.1.3.

The configuration file structure is identical to [bootflash_files_delete](./bootflash_files_delete.md)

`filepath` can be any file glob.

Examples:

- `*:/*.txt` list all `.txt` files from all flash devices on the specified supervisor
-  `bootflash:/scanner-202411??.log` list all scanner log files whose name implies Nov 20224

``` yaml title="config/config_bootflash_files_info.yaml"
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
./bootflash_files_info.py --config config/config_bootflash_files_info.yaml
# output not shown
```

## Example output

### Files searched successfully

``` bash title="Successful search"
(.venv) arobel@AROBEL-M-G793 examples % ./bootflash_files_info.py --config prod/config_bootflash_files_info.yaml
{
    "changed": false,
    "diff": [
        {
            "10.1.1.2": [
                {
                    "date": "2024-03-01 01:04:02",
                    "device_name": "cvd-1312-leaf",
                    "filepath": "bootflash:/20240301_010220_poap_19786_init.log",
                    "ip_address": "10.1.1.2",
                    "serial_number": "FDO123456AB",
                    "size": "88497",
                    "supervisor": "active"
                },
                {
                    "date": "2024-06-18 22:52:55",
                    "device_name": "cvd-1312-leaf",
                    "filepath": "bootflash:/20240618_225115_poap_29865_init.log",
                    "ip_address": "10.1.1.2",
                    "serial_number": "FDO123456AB",
                    "size": "127820",
                    "supervisor": "active"
                },
                {
                    "date": "2024-06-18 22:52:23",
                    "device_name": "cvd-1312-leaf",
                    "filepath": "bootflash:/poap_retry_debugs.log",
                    "ip_address": "10.1.1.2",
                    "serial_number": "FDO123456AB",
                    "size": "188",
                    "supervisor": "active"
                },
                {
                    "date": "2024-09-27 18:56:09",
                    "device_name": "cvd-1312-leaf",
                    "filepath": "bootflash:/log_profile.yaml",
                    "ip_address": "10.1.1.2",
                    "serial_number": "FDO123456AB",
                    "size": "2566",
                    "supervisor": "active"
                }
            ],
            "10.1.1.3": [
                {
                    "date": "2024-09-27 18:56:03",
                    "device_name": "cvd-1313-leaf",
                    "filepath": "bootflash:/log_profile.yaml",
                    "ip_address": "10.1.1.3",
                    "serial_number": "FDO123456BC",
                    "size": "2566",
                    "supervisor": "active"
                }
            ],
            "sequence_number": 1
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "bootflash_info",
            "check_mode": false,
            "sequence_number": 1,
            "state": "query"
        }
    ],
    "response": [
        {
            "10.1.1.2": {
                "DATA": {
                    "bootFlashDataMap": {
                        "bootflash:": [
                            {
                                "bootflash_type": "active",
                                "date": "Jul 11 23:57:59 2024",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": ".rpmstore/",
                                "filePath": "bootflash:.rpmstore/",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "0"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Mar 01 01:04:02 2024",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": "20240301_010220_poap_19786_init.log",
                                "filePath": "bootflash:",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "88497"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Jun 18 22:52:55 2024",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": "20240618_225115_poap_29865_init.log",
                                "filePath": "bootflash:",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "127820"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Apr 11 17:09:22 2017",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": "home/",
                                "filePath": "bootflash:home/",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "0"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Sep 27 18:56:09 2024",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": "log_profile.yaml",
                                "filePath": "bootflash:",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "2566"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Jul 20 20:50:16 2024",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": "lost+found/",
                                "filePath": "bootflash:lost+found/",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "0"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Jun 18 22:52:23 2024",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": "poap_retry_debugs.log",
                                "filePath": "bootflash:",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "188"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Jul 11 23:59:10 2024",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": "scripts/",
                                "filePath": "bootflash:scripts/",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "0"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Dec 21 01:22:41 2022",
                                "deviceName": "cvd-1312-leaf",
                                "fileName": "nxos64-cs.10.3.2.F.bin",
                                "filePath": "bootflash:",
                                "ipAddr": " 10.1.1.2",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456AB",
                                "size": "2297351168"
                            }
                        ]
                    },
                    "bootFlashSpaceMap": {
                        "bootflash:": {
                            "bootflash_type": "active",
                            "deviceName": "cvd-1312-leaf",
                            "freeSpace": 46660952064,
                            "ipAddr": " 10.1.1.2",
                            "name": "bootflash:",
                            "serialNumber": "FDO123456AB",
                            "totalSpace": 53532012544,
                            "usedSpace": 6871060480
                        }
                    },
                    "partitions": [
                        "bootflash:"
                    ],
                    "requiredSpace": "NA"
                },
                "MESSAGE": "OK",
                "METHOD": "GET",
                "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/imagemgnt/bootFlash/bootflash-info?serialNumber=FDO123456AB",
                "RETURN_CODE": 200
            },
            "10.1.1.3": {
                "DATA": {
                    "bootFlashDataMap": {
                        "bootflash:": [
                            {
                                "bootflash_type": "active",
                                "date": "Jul 07 01:20:19 2024",
                                "deviceName": "cvd-1313-leaf",
                                "fileName": ".rpmstore/",
                                "filePath": "bootflash:.rpmstore/",
                                "ipAddr": " 10.1.1.3",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456BC",
                                "size": "0"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Apr 11 17:12:36 2017",
                                "deviceName": "cvd-1313-leaf",
                                "fileName": "home/",
                                "filePath": "bootflash:home/",
                                "ipAddr": " 10.1.1.3",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456BC",
                                "size": "0"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Sep 27 18:56:03 2024",
                                "deviceName": "cvd-1313-leaf",
                                "fileName": "log_profile.yaml",
                                "filePath": "bootflash:",
                                "ipAddr": " 10.1.1.3",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456BC",
                                "size": "2566"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Jul 20 20:50:16 2024",
                                "deviceName": "cvd-1313-leaf",
                                "fileName": "lost+found/",
                                "filePath": "bootflash:lost+found/",
                                "ipAddr": " 10.1.1.3",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456BC",
                                "size": "0"
                            },
                            {
                                "bootflash_type": "active",
                                "date": "Dec 21 02:23:18 2022",
                                "deviceName": "cvd-1313-leaf",
                                "fileName": "nxos64-cs.10.3.2.F.bin",
                                "filePath": "bootflash:",
                                "ipAddr": " 10.1.1.3",
                                "name": "bootflash:",
                                "serialNumber": "FDO123456BC",
                                "size": "2297351168"
                            }
                        ]
                    },
                    "bootFlashSpaceMap": {
                        "bootflash:": {
                            "bootflash_type": "active",
                            "deviceName": "cvd-1313-leaf",
                            "freeSpace": 46457872384,
                            "ipAddr": " 10.1.1.3",
                            "name": "bootflash:",
                            "serialNumber": "FDO123456BC",
                            "totalSpace": 53532012544,
                            "usedSpace": 7074140160
                        }
                    },
                    "partitions": [
                        "bootflash:"
                    ],
                    "requiredSpace": "NA"
                },
                "MESSAGE": "OK",
                "METHOD": "GET",
                "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/imagemgnt/bootFlash/bootflash-info?serialNumber=FDO123456BC",
                "RETURN_CODE": 200
            },
            "sequence_number": 1
        }
    ],
    "result": [
        {
            "10.1.1.2": {
                "found": true,
                "success": true
            },
            "10.1.1.3": {
                "found": true,
                "success": true
            },
            "sequence_number": 1
        }
    ]
}
(.venv) arobel@AROBEL-M-G793 examples %
```

### Switch does not exist on the controller

``` bash title="Switch does not exist on the controller"
(.venv) arobel@AROBEL-M-G793 examples % ./bootflash_files_info.py --config config/config_bootflash_files_info.yaml
Exiting.  Error detail: BootflashInfo.refresh_bootflash_info: serial_number not found for switch 10.1.1.2. Error detail SwitchDetails._get: Switch with ip_address 10.1.1.2 does not exist on the controller.
(.venv) arobel@AROBEL-M-G793 examples %
```

### Files not found

``` bash title="Files not found"
(.venv) arobel@AROBEL-M-G793 examples % ./bootflash_files_info.py --config prod/config_bootflash_files_info.yaml
{
    "changed": false,
    "diff": [
        {
            "10.1.1.2": [],
            "10.1.1.3": [],
            "sequence_number": 1
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "bootflash_info",
            "check_mode": false,
            "sequence_number": 1,
            "state": "query"
        }
    ],
    "response": [
        {
            "10.1.1.2": {
                "DATA": {
                    "bootFlashDataMap": {
                        "bootflash:": ["OUTPUT REMOVED FOR BREVITY"]
                    },
                    "bootFlashSpaceMap": {
                        "bootflash:": {
                            "bootflash_type": "active",
                            "deviceName": "cvd-1312-leaf",
                            "freeSpace": 46660952064,
                            "ipAddr": " 10.1.1.2",
                            "name": "bootflash:",
                            "serialNumber": "FDO123456AB",
                            "totalSpace": 53532012544,
                            "usedSpace": 6871060480
                        }
                    },
                    "partitions": [
                        "bootflash:"
                    ],
                    "requiredSpace": "NA"
                },
                "MESSAGE": "OK",
                "METHOD": "GET",
                "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/imagemgnt/bootFlash/bootflash-info?serialNumber=FDO123456AB",
                "RETURN_CODE": 200
            },
            "10.1.1.3": {
                "DATA": {
                    "bootFlashDataMap": {
                        "bootflash:": ["OUTPUT REMOVED FOR BREVITY"]
                    },
                    "bootFlashSpaceMap": {
                        "bootflash:": {
                            "bootflash_type": "active",
                            "deviceName": "cvd-1313-leaf",
                            "freeSpace": 46457872384,
                            "ipAddr": " 10.1.1.3",
                            "name": "bootflash:",
                            "serialNumber": "FDO123456BC",
                            "totalSpace": 53532012544,
                            "usedSpace": 7074140160
                        }
                    },
                    "partitions": [
                        "bootflash:"
                    ],
                    "requiredSpace": "NA"
                },
                "MESSAGE": "OK",
                "METHOD": "GET",
                "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/imagemgnt/bootFlash/bootflash-info?serialNumber=FDO123456BC",
                "RETURN_CODE": 200
            },
            "sequence_number": 1
        }
    ],
    "result": [
        {
            "10.1.1.2": {
                "found": true,
                "success": true
            },
            "10.1.1.3": {
                "found": true,
                "success": true
            },
            "sequence_number": 1
        }
    ]
}
(.venv) arobel@AROBEL-M-G793 examples %
```
