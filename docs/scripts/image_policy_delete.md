# image_policy_delete.py

## Description

Create or update one or more image policies.

## Example configuration file

Delete image policies KR5M and NR1F, if they exist.

``` yaml title="config/image_policy_delete.yaml"
---
config:
    - name: KR5M
    - name: NR1F
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
./image_policy_delete.py --config config/image_policy_delete.yaml
# output not shown
```

## Example output

### Image policies deleted successfully

``` bash title="Image policies delete success"
{
    "changed": true,
    "diff": [
        {
            "policyNames": [
                "KR5M",
                "NR1F"
            ],
            "sequence_number": 1
        }
    ],
    "failed": false,
    "metadata": [
        {
            "action": "delete",
            "check_mode": false,
            "sequence_number": 1,
            "state": "deleted"
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

### The specified image policies do not exist

``` bash title="Image policies do not exist"
(.venv) AROBEL-M-G793% ./image_policy_delete.py --config prod/image_policy_delete.yaml
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
            "action": "delete",
            "check_mode": false,
            "sequence_number": 1,
            "state": "deleted"
        }
    ],
    "response": [
        {
            "MESSAGE": "No image policies to delete.",
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
(.venv) AROBEL-M-G793%
```

### One or more image policies have device(s) attached

``` bash title="Image policies have non-zero ref_count"
(.venv) AROBEL-M-G793% ./image_policy_delete.py --config prod/image_policy_delete.yaml
Exiting.  Error detail: ImagePolicyDelete._get_policies_to_delete: ImagePolicyDelete._verify_image_policy_ref_count: One or more policies have devices attached. Detach these policies from all devices first using the dcnm_image_upgrade module, with state == deleted. policy_name: KR5M, ref_count: 1.
(.venv) AROBEL-M-G793%
```
