# image_policy_replace.py

## Description

Replace one or more image policies.

The configurations for the image policies on the controller will be replaced
by the configurations provided in the configuration file.

## Example configuration file

``` yaml title="config/image_policy_replace.yaml"
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
./image_policy_replace.py --config config/image_policy_replace.yaml
# output not shown
```

## Example output

### Image policy configurations replaced successfully

``` bash title="Successful execution"
(.venv) AROBEL-M-G793% ./image_policy_replace.py --config prod/image_policy_replace.yaml
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
            "rpmimages": "mtx-grpctunnel-2.1.0.0-10.4.1.lib32_64_n9000",
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
    "failed": false,
    "metadata": [
        {
            "action": "replace",
            "check_mode": false,
            "sequence_number": 1,
            "state": "replaced"
        },
        {
            "action": "replace",
            "check_mode": false,
            "sequence_number": 2,
            "state": "replaced"
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
```

### Image policies do not exist on the controller

``` bash title="Image policies no not exist"
(.venv) AROBEL-M-G793% ./image_policy_replace.py --config prod/image_policy_replace.yaml
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
(.venv) AROBEL-M-G793% ./image_policy_replace.py --config prod/image_policy_replace.yaml
unable to replace image policy configuration(s)
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
            "action": "replace",
            "check_mode": false,
            "sequence_number": 1,
            "state": "replaced"
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
(.venv) arobel@AROBEL-M-G793 examples %
```
