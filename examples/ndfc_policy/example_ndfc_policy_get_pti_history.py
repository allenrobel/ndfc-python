#!/usr/bin/env python3
"""
Name: example_ndfc_policy_get_pti_history.py
Description: Retrieve the PTI history for a switch
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_policy import NdfcPolicy

nc = NdfcCredentials()
ndfc = NDFC(log("ndfc_policy_create_log", "INFO", "DEBUG"))
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.login()

instance = NdfcPolicy(ndfc)
instance.description = "Management VRF Default Route"
instance.entity_type = "SWITCH"
instance.entity_name = "SWITCH"
instance.ip_address = "10.1.150.99"
instance.priority = 500
instance.serial_number = "FDO2443096H"
instance.source = ""
instance.switch_name = "cvd-1112-bgw"
instance.template_name = "static_route"
instance.template_content_type = "string"
instance.nv_pairs = {
    "VRF_NAME": "management",
    "ROUTES": "ip route 0.0.0.0/0 10.1.150.1",
}
instance.create()
instance.log(f"Response text: {instance.ndfc.response.text}")
