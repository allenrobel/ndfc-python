#!/usr/bin/env python
"""
Name: example_ndfc_login.py
Description:

Login to an NDFC controller and print the returned auth token.

Usage:

1. Set the following environment variables appropriately for your setup:

    export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
    export NDFC_PYTHON_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/config/config.yml
    export NDFC_USERNAME=admin
    export NDFC_PASSWORD=MyPassword
    export NDFC_DOMAIN=local
    export NDFC_IP4=10.1.1.1

1a. Alternately, you can override NDFC_USERNAME, NDFC_PASSWORD,
    NDFC_DOMAIN, and NDFC_IP4 within the script.  Examples:

    Explicitly setting these:

    sender = Sender()
    sender.username = "admin"
    sender.password = "MyPassword"
    sender.domain = "local"
    sender.ip4 = "10.1.1.1"
    sender.login()

    Using your Ansible vault:

    nc = NdfcCredentials()
    sender = Sender()
    sender.username = nc.username
    sender.password = nc.password
    sender.domain = nc.nd_domain
    sender.ip4 = nc.ndfc_ip
    sender.login()


2. Edit the YAML file pointed to by NDFC_PYTHON_CONFIG to contain at least:

3. In your shell, export the following e
---
ansible_vault: "/path/to/your/ansible/vault"

"""
import json
import logging
import sys
# We are using our local copy of log_v2.py which is modified to
# console logging.  The copy in the DCNM Ansible Collection specifically
# disallows console logging.
from ndfc_python.log_v2 import Log
from plugins.module_utils.common.api.v1.lan_fabric.rest.control.fabrics.fabrics import EpFabricDetails
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.sender_requests import Sender

try:
    logger = Log()
    logger.commit()
except ValueError as error:
    msg = "Error while instantiating Log(). "
    msg += f"Error detail: {error}"
    print(msg)

log = logging.getLogger(f"ndfc_python.main")

ep_fabric_details = EpFabricDetails()
ep_fabric_details.fabric_name = "f1"
sender = Sender()

try:
    sender.login()
except ValueError as error:
    msg = "unable to login to the controller."
    log.error(msg)

msg = f"Sender().token: {sender.token}"
log.info(msg)

rest_send = RestSend({})
rest_send.sender = sender
rest_send.response_handler = ResponseHandler()
rest_send.path = ep_fabric_details.path
rest_send.verb = ep_fabric_details.verb
try:
    rest_send.commit()
except ValueError as error:
    msg = f"Could not login to the controller. "
    msg += f"Error detail: {error}"
    log.error(msg)
    sys.exit(1)

msg = f"{json.dumps(rest_send.response_current["DATA"], indent=4, sort_keys=True)}"
print(msg)
