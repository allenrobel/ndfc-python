# image_policy_create.py

## Description

Create or update one or more image policies.

## Example configuration file

``` yaml title="config/config_image_policy_create.yaml"
---
config:
    - name: KR5M
      agnostic: False
      description: KR5M
      epld_image: n9000-epld.10.2.5.M.img
      packages:
        install:
        - cfg_cmp-0.3.1.0-1.x86_64.rpm
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
./image_policy_create.py --config config/config_image_policy_create.yaml
# output not shown
```

## Example output

### Image policies created successfully

``` bash title="Image policies create success"
(.venv) AROBEL-M-G793% ./image_policy_create.py --config prod/config_image_policy_create.yaml
{
    "changed": true,
    "diff": [
        {
            "agnostic": false,
            "epldImgName": "n9000-epld.10.2.5.M.img",
            "nxosVersion": "10.2.5_nxos64-cs_64bit",
            "packageName": "cfg_cmp-0.3.1.0-1.x86_64.rpm",
            "platform": "N9K",
            "policyDescr": "KR5M",
            "policyName": "KR5M",
            "policyType": "PLATFORM",
            "role": null,
            "rpmimages": "mtx-grpctunnel-2.1.0.0-10.4.1.lib32_64_n9000",            "sequence_number": 1
            "unInstall": false
        },
        {
            "agnostic": false,
            "epldImgName": "n9000-epld.10.3.1.F.img",
            "nxosVersion": "10.3.1_nxos64-cs_64bit",
            "platform": "N9K",
            "policyDescr": "NR1F",
            "policyName": "NR1F",
            "policyType": "PLATFORM",
            "sequence_number": 2
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "create",
            "check_mode": false,
            "sequence_number": 1,
            "state": "merged"
        },
        {
            "action": "create",
            "check_mode": false,
            "sequence_number": 2,
            "state": "merged"
        }
    ],
    "response": [
        {
            "DATA": "Policy created successfully.",
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/platform-policy",
            "RETURN_CODE": 200,
            "sequence_number": 1
        },
        {
            "DATA": "Policy created successfully.",
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/platform-policy",
            "RETURN_CODE": 200,
            "sequence_number": 2
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
        }
    ]
}
(.venv) AROBEL-M-G793%
```

### Policy already exists, but requires a change to align with user's config

``` bash title="User config contains a modified description (policyDescr)"
(.venv) AROBEL-M-G793% ./image_policy_create.py --config prod/config_image_policy_create.yaml
{
    "changed": true,
    "diff": [
        {
            "agnostic": false,
            "epldImgName": "n9000-epld.10.2.5.M.img",
            "fabricPolicyName": null,
            "imagePresent": "Present",
            "nxosVersion": "10.2.5_nxos64-cs_64bit",
            "packageName": "cfg_cmp-0.3.1.0-1.x86_64.rpm",
            "platform": "N9K",
            "policyDescr": "KR5M-changed",
            "policyName": "KR5M",
            "policyType": "PLATFORM",
            "role": null,
            "rpmimages": "mtx-grpctunnel-2.1.0.0-10.4.1.lib32_64_n9000",            "sequence_number": 1,
            "unInstall": false
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "update",
            "check_mode": false,
            "sequence_number": 1,
            "state": "merged"
        }
    ],
    "response": [
        {
            "DATA": "Policy updated successfully.",
            "MESSAGE": "OK",
            "METHOD": "POST",
            "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/edit-policy",
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

### No changes to image policies are required

``` bash title="Image policies do not require changes"
(.venv) AROBEL-M-G793% ./image_policy_create.py --config prod/config_image_policy_create.yaml
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

### packages.install is set to a package name that does not exist on the controller

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
```

``` bash title="install package does not exist on the controller"
(.venv) AROBEL-M-G793% ./image_policy_create.py --config prod/config_image_policy_create.yaml
unable to create/update image policies
{
    "changed": false,
    "diff": [
        {
            "sequence_number": 1
        }
    ],
    "failed": true,
    "metadata": [
        {
            "action": "update",
            "check_mode": false,
            "sequence_number": 1,
            "state": "merged"
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
        }
    ],
    "result": [
        {
            "changed": false,
            "sequence_number": 1,
            "success": false
        }
    ]
}
(.venv) AROBEL-M-G793%
```
