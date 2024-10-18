#!/usr/bin/env python3
"""
Example of a raw GET request to NDFC

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
import sys

from ndfc_python.log_v2 import Log
from ndfc_python.ndfc import NDFC, NdfcRequestError
from ndfc_python.ndfc_credentials import NdfcCredentials

try:
    log = Log()
    log.commit()
except ValueError as error:
    msg = "Error while instantiating Log(). "
    msg += f"Error detail: {error}"
    print(msg)
    sys.exit(1)

log = logging.getLogger("ndfc_python.main")

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
    "agnostic": True,
}

try:
    ndfc.post(url, payload=payload)
except NdfcRequestError as error:
    msg = "Error posting request. "
    msg += f"Error detail: {error}"
    log.error(msg)
    sys.exit(1)
log.info(f"{json.dumps(ndfc.response_json, indent=4)}")
