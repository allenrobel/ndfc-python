# policy_delete.py

## Description

Delete one or more policies.

## Notes

1. All policy scripts use `description` as a unique key to identify a policy.

The implication when deleting policies is that a delete request will be rejected if multiple policies on the controller have the same `description`.

## Example configuration file

``` yaml title="config/policy_delete.yaml"
---
config:
  - switch_name: LE3
    fabric_name: SITE3
    description: management vrf static route to syslog server
  - switch_name: LE4
    fabric_name: SITE4
    description: management vrf static route to syslog server
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
export ND_IP4=192.168.7.7
export ND_PASSWORD=MySecretPassword
export ND_USERNAME=admin
./policy_delete.py --config config/policy_delete.yaml
# output not shown
```

## Example output

### Success

``` bash title="Policies deleted successfully"
(ndfc-python) arobel@Allen-M4 examples % ./policy_delete.py --config config/s12/policy_delete.yaml
Deleted fabric SITE1, switch LE1, policy_id POLICY-76120
Deleted fabric SITE2, switch LE2, policy_id POLICY-76130
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure - Policies do not exist

``` bash title="Policies do not exist"
(ndfc-python) arobel@Allen-M4 examples % ./policy_delete.py --config config/s12/policy_delete.yaml
Error deleting policy for fabric SITE1, switch LE1, policy description 'management vrf static route to syslog server'. Error detail: PolicyDelete._set_policy_ids: fabric_name SITE1, switch_name LE1: No policies found with description 'management vrf static route to syslog server'
Error deleting policy for fabric SITE2, switch LE2, policy description 'management vrf static route to syslog server'. Error detail: PolicyDelete._set_policy_ids: fabric_name SITE2, switch_name LE2: No policies found with description 'management vrf static route to syslog server'
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure - Policy delete request rejected because multiple policies with the same description exist on the controller

``` bash title="Policy exists"
(ndfc-python) arobel@Allen-M4 examples % ./policy_delete.py --config config/s12/policy_delete.yaml
Error deleting policy for fabric SITE1, switch LE1, policy description 'management vrf static route to syslog server'. Error detail: PolicyDelete._set_policy_ids: Expected to find exactly one policy with description 'management vrf static route to syslog server' on switch LE1 in fabric SITE1. Found 2 policies with that description. Cannot proceed with delete operation. Manually delete the duplicate policies and try again. policy_ids: ['POLICY-76140', 'POLICY-76150'],
(ndfc-python) arobel@Allen-M4 examples %
```
