# [CredentialSelector]

[CredentialSelector]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/credential_selector.py

## Summary

Decide which credential source to use for a credential (e.g. `nd_password`)
and return the value of the credential from that source.

## Raises

### ValueError

- If `credential_name` cannot be found in any source.
- If `script_args` is not a parser.parse_args() instance.
- If ansible_vault is found in `script_args`, and an error
    occurs when reading the vault from the location provided.

## Properties

### Mandatory

#### credential_name

The name of the credential from which to retrieve the value.  See
[Credentials](../setup/set-credentials.md) for the list of supported
credential names.

#### script_args

An instance of `parser.parse_args()` (from Python's `argparse` library)
containing zero or more [Credentials](../setup/set-credentials.md).

If `script_args` contains `ansible_vault` i.e. the user passed
`--ansible-vault /path/to/vault` on the script command-line, then
Ansible Vault is considered as a credential source and the script,
when run, will ask for the vault password.

### Optional

None

## Description

There can be many (currently three) credentials sources.  This class decides
among command-line arguments, environment variables, and Ansible Vault
(if the `--ansible-vault` location is passed to the script).  It
prioritizes them as follows:

1. Command line argument(s)
2. Environment variable(s)
3. Ansible Vault (assuming the `--ansible-vault` argument is used and points
   to a valid vault file)

## Usage example

See most any script in `./examples/*.py` for example usage. [Reachability] is a
good example in that it demonstrates how to read and use `nxos_password` and
`nxos_username` in addition to the Nexus Dashboard credentials.

[Reachability]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/reachability.py

## See also

- [Credentials](../setup/set-credentials.md)
- [Running the example scripts](../setup/running-the-example-scripts.md)
