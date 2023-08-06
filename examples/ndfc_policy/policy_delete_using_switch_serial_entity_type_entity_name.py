#!/usr/bin/env python3
"""
Name:
example_ndfc_policy_delete_using_switch_serial_entity_type_entity_name.py
Description:
Delete policies matching switch serial number, entity type, and entity name
"""
import sys

from ndfc_python.log import log
from ndfc_python.ndfc import NDFC, NdfcRequestError
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_policy import NdfcPolicy

nc = NdfcCredentials()
logger = log("ndfc_policy_create_log", "INFO", "DEBUG")
ndfc = NDFC()
ndfc.logger = logger
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcPolicy()
instance.logger = logger
instance.ndfc = ndfc
# device's serial number
instance.serial_number = "FDO2443096H"
# the policy type
instance.entity_type = "INTERFACE"
# In the case of an INTERFACE policy, we need to specify
# the interface to which the policy is associated.
instance.entity_name = "loopback1"
try:
    instance.delete()
except ValueError as err:
    msg = f"exiting. Exception detail: {err}"
    instance.logger.error(msg)
    sys.exit(1)
except NdfcRequestError as err:
    msg = f"exiting. Exception detail: {err}"
    instance.logger.error(msg)
    sys.exit(1)
instance.logger.info("Delete request succeeded")
