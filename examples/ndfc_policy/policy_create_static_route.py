#!/usr/bin/env python3
"""
Name: example_ndfc_policy_create_static_route.py
Description: Create NDFC static_route policy
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
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
instance.description = "Management VRF Default Route"
instance.entity_type = "SWITCH"
instance.entity_name = "SWITCH"
# IP address of the device to which the policy will be associated
instance.ip_address = "172.22.150.102"
# Priority of the policy. This determines the order in
# which the policy's CLI will be applied on the device
instance.priority = 500
# device's serial number
instance.serial_number = "FDO21120U5D"
instance.source = ""
# device's name
instance.switch_name = "leaf1"
# template_name of the policy
instance.template_name = "static_route"
instance.template_content_type = "string"
# nv_pairs are different for every policy.  To learn what a given policy
# template requires, take the following path in NDFC's GUI:
# Operations -> Templates -> Select a template -> Actions
# -> Edit Template Content
instance.nv_pairs = {
    "VRF_NAME": "management",
    "ROUTES": "ip route 0.0.0.0/0 172.22.150.1",
}
instance.create()
msg = f"Response text: {instance.ndfc.response.text}"
instance.logger.info(msg)
