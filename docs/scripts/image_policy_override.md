# image_policy_override.py

## Description

Override the image policies on the controller with the image policies
in the configuration file.

Any image policies on the controller that are not in the configuration
file will be deleted.  Any image policies that on the controller and
are in the configuration will be replaced with the image policies in
the configuration.

Use this script when you want the controller configuration to exactly
match the script configuration.

## Example configuration file

``` yaml title="config/config_image_policy_override.yaml"
---
config:
    - name: KR5M
      agnostic: False
      description: KR5M
      epld_image: n9000-epld.10.2.5.M.img
      platform: N9K
      release: 10.2.5_nxos64-cs_64bit
      type: PLATFORM
    - name: NR1F
      description: NR1F
      platform: N9K
      epld_image: n9000-epld.10.3.1.F.img
      release: 10.3.1_nxos64-cs_64bit
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
./image_policy_override.py --config config/config_image_policy_override.yaml
# output not shown
```

## Example output

### Image policy configurations overridden successfully

Below, an image policy on the controller (`FOO_DELETE_ME`) is deleted since it is
not represented in the configuration file.

Image policies `KR5M` and `NR1F` on the controller are updated to match the
configuration file.

``` bash title="Successful execution"
(.venv) AROBEL-M-G793% ./image_policy_override.py --config prod/config_image_policy_override.yaml
{
    "changed": true,
    "diff": [
        {
            "policyNames": [
                "FOO_DELETE_ME"
            ],
            "sequence_number": 1
        },
        {
            "agnostic": false,
            "epldImgName": "n9000-epld.10.2.5.M.img",
            "nxosVersion": "10.2.5_nxos64-cs_64bit",
            "packageName": "",
            "platform": "N9K",
            "policyDescr": "KR5M",
            "policyName": "KR5M",
            "policyType": "PLATFORM",
            "rpmimages": "",
            "sequence_number": 2
        },
        {
            "agnostic": false,
            "epldImgName": "n9000-epld.10.3.1.F.img",
            "nxosVersion": "10.3.1_nxos64-cs_64bit",
            "packageName": "",
            "platform": "N9K",
            "policyDescr": "NR1F",
            "policyName": "NR1F",
            "policyType": "PLATFORM",
            "rpmimages": "",
            "sequence_number": 3
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "delete",
            "check_mode": false,
            "sequence_number": 1,
            "state": "overridden"
        },
        {
            "action": "replace",
            "check_mode": false,
            "sequence_number": 2,
            "state": "overridden"
        },
        {
            "action": "replace",
            "check_mode": false,
            "sequence_number": 3,
            "state": "overridden"
        }
    ],
    "response": [
        {
            "DATA": "Selected policy(s) deleted successfully.",
            "MESSAGE": "OK",
            "METHOD": "DELETE",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/policy",
            "RETURN_CODE": 200,
            "sequence_number": 1
        },
        {
            "DATA": "Policy updated successfully.",
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/edit-policy",
            "RETURN_CODE": 200,
            "sequence_number": 2
        },
        {
            "DATA": "Policy updated successfully.",
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/edit-policy",
            "RETURN_CODE": 200,
            "sequence_number": 3
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
        }
    ]
}
```

### packages.install for image policy is set to a package name that does not exist on the controller

``` yaml title="Invalid config"
---
config:
    - name: KR5M
      agnostic: False
      description: KR5M
      epld_image: n9000-epld.10.2.5.M.img
      packages:
        install:
        - bad_package_name_which_does_not_exist.rpm
        uninstall:
        - mtx-grpctunnel-2.1.0.0-10.4.1.lib32_64_n9000
      platform: N9K
      release: 10.2.5_nxos64-cs_64bit
      type: PLATFORM
    - name: NR1F
      description: NR1F
      platform: N9K
      epld_image: n9000-epld.10.3.1.F.img
      release: 10.3.1_nxos64-cs_64bit
```

``` bash title="install package does not exist on the controller"
(.venv) AROBEL-M-G793% ./image_policy_override.py --config prod/config_image_policy_override.yaml
unable to override one or more image policies
{
    "changed": true,
    "diff": [
        {
            "sequence_number": 1
        },
        {
            "agnostic": false,
            "epldImgName": "n9000-epld.10.3.1.F.img",
            "nxosVersion": "10.3.1_nxos64-cs_64bit",
            "packageName": "",
            "platform": "N9K",
            "policyDescr": "NR1F",
            "policyName": "NR1F",
            "policyType": "PLATFORM",
            "rpmimages": "",
            "sequence_number": 2
        }
    ],
    "failed": true,
    "metadata": [
        {
            "action": "replace",
            "check_mode": false,
            "sequence_number": 1,
            "state": "overridden"
        },
        {
            "action": "replace",
            "check_mode": false,
            "sequence_number": 2,
            "state": "overridden"
        }
    ],
    "response": [
        {
            "DATA": "Invalid Package name(s).",
            "MESSAGE": "Internal Server Error",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/edit-policy",
            "RETURN_CODE": 500,
            "sequence_number": 1
        },
        {
            "DATA": "Policy updated successfully.",
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/edit-policy",
            "RETURN_CODE": 200,
            "sequence_number": 2
        }
    ],
    "result": [
        {
            "changed": false,
            "sequence_number": 1,
            "success": false
        },
        {
            "changed": true,
            "sequence_number": 2,
            "success": true
        }
    ]
}
(.venv) arobel@AROBEL-M-G793 examples %
```
