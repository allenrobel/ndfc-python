# [NetworkDelete]

## Description

Delete a network

[NetworkDelete]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/network_delete.py

## Raises

### `ValueError`

  * `rest_send` is not set prior to calling `commit`.
  * `results` is not set prior to calling `commit`.
  * `network_name` is not set prior to calling `commit`.
  * `fabric_name` is not set prior to calling `commit`.
  * `fabric_name` does not exist on the controller.
  * `network_name` does not exist in fabric `fabric_name`.
  * An error occurred when sending the `DELETE` request to the controller.

## Properties

### Mandatory

#### fabric_name

The name of the fabric containing the network to be deleted.

- default: None
- example: MyFabric
- type: str

#### network_name

The name of the network to delete.

- default: None
- example: MyNet
- type: str

### Optional

None

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
from ndfc_python.network_delete import NetworkDelete
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
        description="DESCRIPTION: Delete a network.",
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
    print(msg)
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
    sys.exit(1)

rest_send = RestSend({})
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()

try:
    instance = NetworkDelete()
    instance.rest_send = rest_send
    instance.results = Results()
    instance.fabric_name = config.get("fabric_name")
    instance.network_name = config.get("network_name")
    instance.commit()
except ValueError as error:
    msg = "Error deleting network. "
    msg += f"Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

msg = f"Network {config.get('network_name')} "
msg += f"deleted from fabric {config.get('fabric_name')}"
print(msg)
```
