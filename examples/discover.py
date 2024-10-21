#!/usr/bin/env python3
"""
Name: discover.py
Description:

Run NDFC's device discovery using credentials read from environment variables.

Usage

1. Sender() credentials
    Sender() reads credentials from environment variables unless
    you override them with:

    sender = Sender()
    sender.domain = "local"
    sender.ip4 = "10.1.1.1"
    sender.password = "MyNdfcPassword"
    sender.username = "MyNdfcUsername"

    Environment variables read by Sender()

    export NDFC_DOMAIN=local
    export NDFC_IP4=10.1.1.1
    export NDFC_PASSWORD=MyNdfcPassword
    export NDFC_USERNAME=MyNdfcUsername

2. Script variables

    Set the following script variables appropriately for your setup.

    FABRIC_NAME = "MyFabric"
    SEED_IPS = ["10.1.1.1", "10.1.1.2"]
    DISCOVER_PASSWORD = "MySwitchPassword"
    DISCOVER_USERNAME = "admin"


"""
import logging
import sys

from ndfc_python.log_v2 import Log
from ndfc_python.ndfc_discover import NdfcDiscover
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.common.sender_requests import Sender

FABRIC_NAME = "MyFabric"
SEED_IPS = ["10.1.1.1", "10.1.1.2"]
DISCOVER_PASSWORD = "MySwitchPassword"
DISCOVER_USERNAME = "admin"

try:
    logger = Log()
    logger.commit()
except ValueError as error:
    MSG = "Error while instantiating Log(). "
    MSG += f"Error detail: {error}"
    print(MSG)
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

instance = NdfcDiscover()
instance.rest_send = rest_send
instance.results = Results()
instance.fabric_name = FABRIC_NAME
instance.cdp_second_timeout = 5
instance.max_hops = 0
instance.discover_password = DISCOVER_PASSWORD
instance.discover_username = DISCOVER_USERNAME
instance.preserve_config = True

for seed_ip in SEED_IPS:
    instance.seed_ip = seed_ip
    try:
        instance.discover()
    except (TypeError, ValueError) as error:
        msg = f"Error detail: {error}"
        raise ValueError(msg) from error
    print(f"discover_status_code {instance.discover_status_code}")
    print(f"discover_response {instance.discover_response}")
