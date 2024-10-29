#!/usr/bin/env python3
"""
# Name

rest_get_request.py

# Description

Send a REST GET request to the controller.

# NOTES

1.  Set the following environment variables before running this script.

PYTHONPATH should include this repository and the ansible-dcnm repository.

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible-dcnm
```

2. Optional, enable logging by setting the following environment variable.

NDFC_LOGGING_CONFIG should point to a valid logging dictConfig file.

https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json

3. Edit rest_send.path in the script below.

The value should be a valid NDFC REST API endpoint.  A couple example endpoints
are provided for you to try (ep_fabrics, and ep_issu)

"""
import argparse
import json
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_controller_domain import parser_controller_domain
from ndfc_python.parsers.parser_controller_ip4 import parser_controller_ip4
from ndfc_python.parsers.parser_controller_password import parser_controller_password
from ndfc_python.parsers.parser_controller_username import parser_controller_username
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        parents=[
            parser_loglevel,
            parser_controller_domain,
            parser_controller_ip4,
            parser_controller_password,
            parser_controller_username,
        ],
        description="DESCRIPTION: Send a REST GET request to the controller.",
    )
    return parser.parse_args()


args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

# By default, sender reads environment variables for its ND credentials.
# These can be overridden on the command line.  Run the script with --help
# for details.

try:
    sender = NdfcPythonSender()
    sender.args = args
    sender.commit()
except ValueError as error:
    msg = f"Exiting.  Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

rest_send = RestSend({})
rest_send.sender = sender.sender
rest_send.response_handler = ResponseHandler()

# Some example NDFC endpoints
ep_fabrics = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics"
ep_issu = "/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/packagemgnt/issu"

try:
    # Use one of the above example endpoints
    rest_send.path = ep_fabrics
    rest_send.verb = "GET"
    rest_send.commit()
except (TypeError, ValueError) as error:
    msg = "Error sending request. "
    msg += f"Error detail: {error}"
    log.error(msg)
    sys.exit(1)

msg = f"{json.dumps(rest_send.response_current, indent=4)}"
log.info(msg)
print(msg)
