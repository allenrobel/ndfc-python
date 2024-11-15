# image_policy_info_all.py

## Description

Returns information about all image policies on the controller.

## Example configuration file

Configuration file is not required.

## Example Usage

The example below uses environment variables for credentials, so no
arguments are required if credentials are defined as environment variables.

See [Running the Example Scripts] for details around specifying credentials
from the command line, from environment variables, from Ansible Vault, or a
combination of these credentials sources.

[Running the Example Scripts]: ../setup/running-the-example-scripts.md

``` bash
export ND_DOMAIN=local
export ND_IP4=10.1.1.2
export ND_PASSWORD=MySecret
export ND_USERNAME=admin
./image_policy_info_all.py
# Output not shown
```

## Example output

### One or more image policies exist on the controller

``` bash title="Successful response"
(.venv) AROBEL-M-G793% ./image_policy_info_all.py
{
    "changed": false,
    "diff": [
        {
            "nxos64-cs.10.2.5.M.bin_N9K_All": {
                "agnostic": false,
                "epldImgName": "",
                "fabricPolicyName": "nxos64-cs.10.2.5.M.bin",
                "imageName": "nxos64-cs.10.2.5.M.bin",
                "imagePresent": "Present",
                "nxosVersion": "10.2.5_nxos64-cs_64bit",
                "packageName": "",
                "platform": "N9K/N3K",
                "platformPolicies": "",
                "policyDescr": null,
                "policyName": "nxos64-cs.10.2.5.M.bin_N9K_All",
                "policyType": "FABRIC",
                "ref_count": 0,
                "role": "All",
                "rpmimages": "false",
                "unInstall": false
            },
            "sequence_number": 1
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "query_all_image_policies",
            "check_mode": false,
            "sequence_number": 1,
            "state": "query"
        }
    ],
    "response": [
        {
            "DATA": {
                "lastOperDataObject": [
                    {
                        "agnostic": false,
                        "epldImgName": "",
                        "fabricPolicyName": "nxos64-cs.10.2.5.M.bin",
                        "imageName": "nxos64-cs.10.2.5.M.bin",
                        "imagePresent": "Present",
                        "nxosVersion": "10.2.5_nxos64-cs_64bit",
                        "packageName": "",
                        "platform": "N9K/N3K",
                        "platformPolicies": "",
                        "policyDescr": null,
                        "policyName": "nxos64-cs.10.2.5.M.bin_N9K_All",
                        "policyType": "FABRIC",
                        "ref_count": 0,
                        "role": "All",
                        "rpmimages": "false",
                        "unInstall": false
                    }
                ],
                "message": "",
                "status": "SUCCESS"
            },
            "MESSAGE": "OK",
            "METHOD": "GET",
            "REQUEST_PATH": "https://10.1.1.2/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/policies",
            "RETURN_CODE": 200,
            "sequence_number": 1
        }
    ],
    "result": [
        {
            "found": true,
            "sequence_number": 1,
            "success": true
        }
    ]
}
(.venv) AROBEL-M-G793%
```

### No image policies exist on the controller

``` bash title="No image policies exist"
(.venv) AROBEL-M-G793% ./image_policy_info_all.py --nd-ip4 10.1.1.3
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
            "action": "query_all_image_policies",
            "check_mode": false,
            "sequence_number": 1,
            "state": "query"
        }
    ],
    "response": [
        {
            "DATA": {
                "lastOperDataObject": [],
                "message": "",
                "status": "SUCCESS"
            },
            "MESSAGE": "OK",
            "METHOD": "GET",
            "REQUEST_PATH": "https://10.1.1.3/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/policies",
            "RETURN_CODE": 200,
            "sequence_number": 1
        }
    ],
    "result": [
        {
            "found": true,
            "sequence_number": 1,
            "success": true
        }
    ]
}
(.venv) AROBEL-M-G793%
```
