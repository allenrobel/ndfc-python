# [NetworkCreate]

## Description

Create a network

[NetworkCreate]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/network_create.py

## Raises

### `ValueError`

* `rest_send` is not set prior to calling `commit`.
* `results` is not set prior to calling `commit`.
* `network_name` is not set prior to calling `commit`.
* `fabric_name` is not set prior to calling `commit`.
* `network_id` is not set prior to calling `commit`.
* `vlan_id` is not set prior to calling `commit`.
* `vrf_name` is not set prior to calling `commit`.
* `fabric_name` does not exist on the controller.
* `vrf_name` does not exist in fabric `fabric_name`.
* `network_name` already exists in fabric `fabric_name`.
* An error occurred when sending the `POST` request to the controller.

## Properties

### Mandatory

#### fabric_name

The name of the fabric containing the network to be created.

- default: None
- example: MyFabric
- type: str

#### network_id

The ID the controller should assign to `network_name`.

- default: None
- example: 30000
- type: int

#### vrf_name

The VRF associated with `network_name`.

- default: None
- example: MyVrf
- type: str

### Optional

#### dhcp_server_addr_1

Set's the value of `dhcpServerAddr1` in the `Default_Network_Universal`
template.

The first DHCP server associated with `network_name`.

- default: None
- example: 10.1.1.2
- type: str

#### dhcp_server_addr_2

Set's the value of `dhcpServerAddr2` in the `Default_Network_Universal`
template.

The second DHCP server associated with `network_name`.

- default: None
- example: 10.1.1.3
- type: str

#### dhcp_server_addr_3

Set's the value of `dhcpServerAddr3` in the `Default_Network_Universal`
template.

The third DHCP server associated with `network_name`.

- default: None
- example: 10.1.1.4
- type: str

#### enable_netflow

Set's the value of `ENABLE_NETFLOW` in the `Default_Network_Universal`
template.

Netflow is supported only if it is enabled on fabric. For NX-OS only

- default: False
- example: True
- type: bool

#### enable_l3_on_border

Set's the value of `enableL3OnBorder` in the `Default_Network_Universal`
template.

Create SVI on borders and border gateways, including vPC border gateways and
anycast border gateways.

- default: False
- example: True
- type: bool

#### enable_l3_on_border_vpc_bgw

Set's the value of `enableL3OnBorderVpcBgw` in the `Default_Network_Universal`
template.

Create SVI on borders and vPC border gateways. Not applicable to anycast
border gateways.

- default: False
- example: True
- type: bool

#### gateway_ip_address

Set's the value of `gatewayIpAddress` in the `Default_Network_Universal`
template.

IPv4 Gateway/NetMask.

- default: None
- example: 192.0.2.1/24
- type: str

#### gateway_ipv6_address

Set's the value of `gatewayIpV6Address` in the `Default_Network_Universal`
template.

Comma-separated list of IPv6/Prefix.

- default: None
- example: 2001:db8::1/64,2001:db9::1/64
- type: str

#### igmp_version

If set to non-default value (1 or 3), the `ip igmp version` command is
generated on NX-OS and IOS-XE devices in `network_name`.

See note below for NX-OS.

- default: 2
- example: 3
- type: str
- min: 1
- max: 3
- note: min is 2 for NX-OS

#### intf_description

Set's the value of `intfDescription` in the `Default_Network_Universal`
template.

Interface Description.

- default: None
- example: Interface in MyNet
- type: str

#### is_layer2_only

Set's the value of `isLayer2Only` in the `Default_Network_Universal`
template.

If True, `network_name` will be a Layer 2 network.
If False, `network_name` will be a Layer 3 network.

- default: False
- example: True
- type: bool

#### loopback_id

Set's the value of `loopbackId` in the `Default_Network_Universal`
template.

Loopback ID for DHCP Relay interface

- default: None
- example: 10
- max: 1023
- min: 0
- type: int

#### mcast_group

Set's the value of `mcastGroup` in the `Default_Network_Universal`
template.

- default: ""
- example: 225.1.1.1
- type: str

#### mtu

Set's the value of `mtu` in the `Default_Network_Universal`
template.

NX-OS Specific

- default: 9216
- example: 1500
- type: int
- min: 68
- max: 9216

#### network_name

The name of the network to create.

- default: MyNetwork_`network_id`
- example: MyNet
- type: str

#### nve_id

Set's the value of `nveId` in the `Default_Network_Universal`
template.

- default: 1
- example: 1
- type: int
- min: 1
- max: 1

#### rt_both_auto

Set's the value of `rtBothAuto` in the `Default_Network_Universal`
template.

Might be set in the fabric config and be read-only here?
NX-OS Specific.

- default: False
- example: True
- type: bool

#### secondary_gw_1

Set's the value of `secondaryGW1` in the `Default_Network_Universal`
template.

- default: ""
- example: 192.0.2.1/24
- type: str

#### secondary_gw_2

Set's the value of `secondaryGW2` in the `Default_Network_Universal`
template.

- default: ""
- example: 192.0.2.2/24
- type: str

#### secondary_gw_3

Set's the value of `secondaryGW3` in the `Default_Network_Universal`
template.

- default: ""
- example: 192.0.2.3/24
- type: str

#### secondary_gw_4

Set's the value of `secondaryGW4` in the `Default_Network_Universal`
template.

- default: ""
- example: 192.0.2.4/24
- type: str

#### segment_id

Set's the value of `segmentId` in the `Default_Network_Universal`
template.

- default: ""
- example: 30000
- type: int

#### suppress_arp

Set's the value of `suppressArp` in the `Default_Network_Universal`
template.

ARP suppression is only supported if SVI is present when `is_layer2_only` is set to False.

NX-OS Specific

- default: False
- example: NA
- type: bool

#### svi_netflow_monitor

Set's the value of `SVI_NETFLOW_MONITOR` in the `Default_Network_Universal`
template.

Applicable only if `is_layer2_only` is False and `enable_netflow` is True.
Value must be a monitor name defined in fabric setting for Layer 3 Record.
For NX-OS only.

- default: ""
- example: NA
- type: str

#### tag

Set's the value of `tag` in the `Default_Network_Universal`
template. NX-OS Specific

Routing tag.

- default: 12345
- example: 54321
- type: int
- min: 0
- max: 4294967295

#### trm_enabled

Set's the value of `trmEnabled` in the `Default_Network_Universal`
template.

If True, enable IPv4 Tenant Routed Multicast.

- default: False
- example: True
- type: bool

#### trm_v6_enabled

Set's the value of `trmV6Enabled` in the `Default_Network_Universal`
template.

If True, enable IPv6 Tenant Routed Multicast.

- default: False
- example: True
- type: bool

#### vrf_dhcp

Set's the value of `vrfDhcp` in the `Default_Network_Universal`
template.

- default: ""
- example: NA
- type: str

#### vlan_name

Set's the value of `vlanName` in the `Default_Network_Universal`
template.

If greater than 32 chars, enable `system vlan long-name` for NX-OS.
Disable `VTPv1` and `VTPv2` or switch to `VTPv3` for IOS-XE.

- default: ""
- example: MyVlan
- type: str

#### vlan_id

Set's the value of `vlanId` in the `Default_Network_Universal`
template.

- default: ""
- example: 1111
- type: int
- min: 1
- max: 4094

#### vlan_netflow_monitor

Set's the value of `VLAN_NETFLOW_MONITOR` in the `Default_Network_Universal`
template.

Applicable only if `enable_netflow` is True.

Value must be a monitor name defined in fabric setting for Layer 3 Record.
For NX-OS only

- default: ""
- example: NA
- type: str

## Example script

```py title="Example Script"
import argparse
import logging
import sys

# We are using our local copy of log_v2.py which is modified to allow
# console logging.  The copy in the DCNM Ansible Collection specifically
# disallows console logging.
from ndfc_python.ndfc_python_config import NdfcPythonConfig
from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.network_create import NetworkCreate
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_controller_domain import parser_controller_domain
from ndfc_python.parsers.parser_controller_ip4 import parser_controller_ip4
from ndfc_python.parsers.parser_controller_password import parser_controller_password
from ndfc_python.parsers.parser_controller_username import parser_controller_username
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        parents=[
            parser_config,
            parser_loglevel,
            parser_controller_domain,
            parser_controller_ip4,
            parser_controller_password,
            parser_controller_username,
        ],
        description="DESCRIPTION: Create a network.",
    )
    return parser.parse_args()

args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

try:
    ndfc_sender = NdfcPythonSender()
    ndfc_sender.args = args
    ndfc_sender.commit()
except ValueError as error:
    msg = f"Exiting.  Error detail: {error}"
    log.error(msg)
    sys.exit(1)

try:
    ndfc_config = NdfcPythonConfig()
    ndfc_config.filename = args.config
    ndfc_config.commit()
    config = ndfc_config.contents["config"]
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit()

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()

try:
    instance = NetworkCreate()
    instance.rest_send = rest_send
    instance.results = Results()
    instance.fabric_name = config.get("fabric_name")
    instance.network_name = config.get("network_name")
    instance.enable_ir = config.get("enable_ir")
    instance.gateway_ip_address = config.get("gateway_ip_address")
    instance.network_id = config.get("network_id")
    instance.vlan_id = config.get("vlan_id")
    instance.vrf_name = config.get("vrf_name")
    instance.commit()
except ValueError as error:
    msg = "Error creating network. "
    msg += f"Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

msg = f"Network {config.get('network_name')} "
msg += f"created in fabric {config.get('fabric_name')}"
print(msg)
```
