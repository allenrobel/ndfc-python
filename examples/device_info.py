#!/usr/bin/env python3
"""
Name: device_info.py
Description:

Retrieve various information about a device, given its ip address.

Usage:

Edit the vars below to match your setup
    - SWITCH_IP4
"""
import logging
import sys

from ndfc_python.log_v2 import Log
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.common.sender_requests import Sender
from plugins.module_utils.common.switch_details import SwitchDetails

SWITCH_IP4 = "10.1.1.1"

try:
    logger = Log()
    logger.commit()
except ValueError as error:
    msg = "Error while instantiating Log(). "
    msg += f"Error detail: {error}"
    print(msg)
    sys.exit(1)

log = logging.getLogger("ndfc_python.main")

try:
    sender = Sender()
    sender.login()
except ValueError as error:
    msg = "unable to login to the controller. "
    msg += f"Error detail: {error}"
    log.error(msg)

rest_send = RestSend({})
rest_send.sender = sender
rest_send.response_handler = ResponseHandler()

try:
    instance = SwitchDetails()
    instance.results = Results()
    instance.rest_send = rest_send
    instance.refresh()
except ValueError as error:
    msg = "Unable to get switch details. "
    msg += f"Error details: {error}"
    log.error(msg)
    sys.exit(1)

instance.filter = SWITCH_IP4
try:
    print(f"fabric_name: {instance.fabric_name}")
    print(f"serial_number: {instance.serial_number}")
    print(f"status: {instance.status}")
    print(f"model: {instance.model}")
except ValueError as error:
    msg = "Unable to get switch details. "
    msg += f"Error details: {error}"
    log.error(msg)
# etc, see additional properties in SwitchDetails()
