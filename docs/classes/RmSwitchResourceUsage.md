# [RmSwitchResourceUsage]

## Description

Get switch resource usage from the controller.

[RmSwitchResourceUsage]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/rm_switch_resource_usage.py

## Raises

### `ValueError`

* `rest_send` is not set prior to calling `commit`.
* `results` is not set prior to calling `commit`.
* `serial_number` is not set prior to calling `commit`.
* An error occurred when sending the `GET` request to the controller.

## Properties

### Mandatory

#### serial_number

The serial number of the switch for which to retrieve resource usage.

* default: None
* example: FDO1234567A
* type: str

### Optional

#### filter

An optional filter to apply to the output results. Valid values are:

* ALL
* DISCOVERED_VLAN
* SERVICE_NETWORK_VLAN
* TOP_DOWN_VRF_VLAN
* TOP_DOWN_NETWORK_VLAN
* VPC_PEER_LINK_VLAN

* default: ALL
* example: TOP_DOWN_NETWORK_VLAN
* type: str

#### resource_usage

A list of resource usage information for the switch. If `filter` is set, only entries matching the filter are returned.

* default: []
* type: list

## Example script

```py title="Example Script"
import logging
import sys
from ndfc_python.rm_switch_resource_usage import RmSwitchResourceUsage
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.common.response_handler import ResponseHandler

# Setup logging as needed
log = logging.getLogger("ndfc_python.main")

# Setup REST send and results objects
rest_send = RestSend({})
rest_send.response_handler = ResponseHandler()

# Instantiate and configure the resource usage object
instance = RmSwitchResourceUsage()
instance.rest_send = rest_send
instance.results = Results()
instance.serial_number = "FDO1234567A"  # Set your switch serial number here
# instance.filter = "TOP_DOWN_NETWORK_VLAN"  # Optional filter

try:
    instance.commit()
    usage = instance.resource_usage
    print(f"Resource usage for switch {instance.serial_number}:")
    for entry in usage:
        print(entry)
except ValueError as error:
    log.error(f"Error retrieving switch resource usage: {error}")
    sys.exit(1)
```
