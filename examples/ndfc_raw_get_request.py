#!/usr/bin/env python3
"""
Example: send a raw GET request to NDFC

NOTES:

1.  Set the following environment variables before running this script
    (edit appropriately for your setup)

export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/netbox-tools/lib
export NDFC_PYTHON_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/config/config.yml

Optional, to enable logging:
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
"""
import json
import logging

from ndfc_python.log_v2 import Log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials

try:
    log = Log()
    log.commit()
except ValueError as error:
    msg = "Error while instantiating Log(). "
    msg += f"Error detail: {error}"
    print(msg)

log = logging.getLogger("ndfc_python.main")

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
log.info(f"{json.dumps(ndfc.response_json, indent=4)}")
