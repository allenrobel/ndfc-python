# policy_create.py

## Description

Create one or more policies.

## Notes

1. All policy scripts use `description` as a unique key to identify a policy.

The implication when creating policies is that a create request will be rejected if a policy is found on the controller with the same `description` as the policy being created.

## Example configuration file

``` yaml title="config/policy_create.yaml"
---
config:
  - switch_name: LE1
    fabric_name: SITE1
    description: management vrf static route to syslog server
    entity_name: SWITCH
    entity_type: SWITCH
    priority: 200
    source: ""
    template_name: vrf_static_route
    nv_pairs:
      IP_PREFIX: 192.168.7.1/32
      NEXT_HOP_IP: 192.168.12.1
      VRF_NAME: management
  - switch_name: LE2
    fabric_name: SITE2
    description: management vrf static route to syslog server
    entity_name: SWITCH
    entity_type: SWITCH
    priority: 200
    source: ""
    template_name: vrf_static_route
    nv_pairs:
      IP_PREFIX: 192.168.7.1/32
      NEXT_HOP_IP: 192.168.12.1
      VRF_NAME: management
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
./policy_create.py --config config/policy_create.yaml
# output not shown
```

## Example output

### Success

``` bash title="Policies created successfully"
(ndfc-python) arobel@Allen-M4 examples % ./policy_create.py --config config/s12/policy_create.yaml
Created fabric SITE1, switch LE1, policy_id POLICY-76120.
Created fabric SITE2, switch LE2, policy_id POLICY-76130.
(ndfc-python) arobel@Allen-M4 examples %
```

### Failure - Policy create request rejected because a policy with the same description already exists

``` bash title="Policy exists"
(ndfc-python) arobel@Allen-M4 examples % ./policy_create.py --config config/s12/policy_create.yaml
Error creating fabric SITE1, switch LE1, policy (template_name: vrf_static_route). Error detail: PolicyCreate._validate_no_policy_name_conflict: Policy ID POLICY-76120 with description 'management vrf static route to syslog server' already exists on switch LE1 in fabric SITE1. Use a unique policy description or delete the existing policy.
Error creating fabric SITE2, switch LE2, policy (template_name: vrf_static_route). Error detail: PolicyCreate._validate_no_policy_name_conflict: Policy ID POLICY-76130 with description 'management vrf static route to syslog server' already exists on switch LE2 in fabric SITE2. Use a unique policy description or delete the existing policy.
(ndfc-python) arobel@Allen-M4 examples %
```
