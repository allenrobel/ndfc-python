#!/usr/bin/env python3
"""
Example of a raw GET request to NDFC
"""
import json
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials

logger = log("ndfc_login_log", "INFO", "DEBUG")
nc = NdfcCredentials()
ndfc = NDFC()
ndfc.domain = nc.nd_domain
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.password = nc.password
ndfc.username = nc.username
ndfc.login()
url_issu = f"https://{ndfc.ip4}/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/packagemgnt/issu"
url = f"https://{ndfc.ip4}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics"
ndfc.get(url_issu)
print(f"{json.dumps(ndfc.response_json, indent=4)}")
