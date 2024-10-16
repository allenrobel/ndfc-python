#!/usr/bin/env python3
"""
Example of a raw GET request to NDFC
"""
import json

from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials

payload = {
    "devices": [{"serialNumber": "FDO21120U5D", "policyName": "KR5M"}],
    "issu": True,
    "epld": False,
    "packageInstall": False,
}

logger = log("ndfc_login_log", "INFO", "DEBUG")
nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()
url = f"https://{ndfc.ip4}/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/imageupgrade/install-options"
ndfc.post(url, payload=payload)
print(f"{json.dumps(ndfc.response_json, indent=4)}")
