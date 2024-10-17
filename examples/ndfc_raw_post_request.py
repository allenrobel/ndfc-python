#!/usr/bin/env python3
"""
Example of a raw GET request to NDFC
"""
import json

from ndfc_python.log_v2 import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials

try:
    log = Log()
    log.commit()
except ValueError as error:
    MSG = "Error while instantiating Log(). "
    MSG += f"Error detail: {error}"
    print(MSG)

nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()
url_base = f"https://{ndfc.ip4}"

url = f"{url_base}"
url += "/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/platform-policy"

payload = {
    "policyName": "MyPolicy",
    "policyType": "PLATFORM",
    "nxosVersion": "10.3.1_nxos64-cs_64bit",
    "packageName": "",
    "platform": "N9K",
    "policyDescr": "Policy notes",
    "epldImgName": "",
    "rpmimages": "",
    "agnostic": True
}

ndfc.post(url, payload=payload)
print(f"{json.dumps(ndfc.response_json, indent=4)}")
