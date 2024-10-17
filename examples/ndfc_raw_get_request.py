#!/usr/bin/env python3
"""
Example: send a raw GET request to NDFC
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

# Some example URLs
url_issu = f"{url_base}"
url_issu += "/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/packagemgnt/issu"

url_fabrics = f"{url_base}"
url_fabrics += "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics"

url_image_platform = f"{url_base}"
url_image_platform += "/appcenter/cisco/ndfc/api/v1/imagemanagement/rest/policymgnt/platforms"

# Use of of the above example URLs
ndfc.get(url_fabrics)
print(f"{json.dumps(ndfc.response_json, indent=4)}")
