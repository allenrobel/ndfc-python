# [Reachability]

## Description

Retrieve reachability information for a switch.

[Reachability]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/reachability.py

## Raises

### `ValueError`

* `fabric_name` does not exist on the controller.
* `nxos_password` is not set prior to calling `commit`.
* `nxos_username` is not set prior to calling `commit`.
* `rest_send` is not set prior to calling `commit`.
* `results` is not set prior to calling `commit`.
* `seed_ip` does not exist in fabric `fabric_name`.
* An error occurred when sending the `POST` request to the controller.

## Properties

### Mandatory

#### fabric_name

The name of the fabric containing the switch for which reachability information
is requested.

- default: None
- example: MyFabric
- type: str

#### nxos_password

The password for NX-OS switches in the fabric.
The controller refers to this as the discovery password.

- default: None
- example: MyNxosPassword
- type: str

#### nxos_username

The username for NX-OS switches in the fabric.
The controller refers to this as the discovery username.

- default: None
- example: admin
- type: str

#### seed_ip

The ipv4 address of the switch for which reachability information is requested.

- default: None
- example: 10.1.1.2
- type: str

### Optional

None

## Example script

See [examples/reachability.py](../scripts/reachability.md)

