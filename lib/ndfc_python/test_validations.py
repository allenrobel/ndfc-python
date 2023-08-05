#!/usr/bin/env python

from ndfc_python.validations import Validations
from ndfc_python.log import log

logger = log("tmp_test_ndfc_common", "INFO", "DEBUG")
validations = Validations()

def macsec_algorithm(param):
    """
    test macsec algorithm
    """
    try:
        validations._verify_macsec_algorithm(param)
    except ValueError as err:
        logger.error(f"verify_macsec_algorithm. {err}")

def rp_count(param):
    """
    test rp_count
    """
    try:
        validations._verify_rp_count(param)
    except ValueError as err:
        logger.error(f"verify_rp_count. {err}")

def string_length(params):
    """
    test string length
    params is a dict with expected keys:
       - length, int, expected length of test string
       - string, str, test string
    """
    try:
        validations._verify_string_length(params)
    except (KeyError, TypeError, ValueError) as err:
        logger.error(f"verify_string_length. {err}")

# valid value
macsec_algorithm("AES_128_CMA")
# bad value
macsec_algorithm("bad_macsec_algorithm")
# valid value
rp_count(4)
# bad value
rp_count(3)
# bad type
rp_count("bad_rp_count")
# valid case
string_length({"length": 13, "string": "test_string"})
# string too long
string_length({"length": 2, "string": "too_long"})
# missing mandatory key
string_length({"length": 2})
# bad string type
string_length({"length": 2, "string": 10})
# bad length type
string_length({"length": "bad_len", "string": "test_string"})
# params not a dict
string_length("bad_params")

try:
    validations._verify_bgp_asn("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_bgp_password_key_type("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_vlan("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_vrf_vlan_id("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_loopback_id("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_max_bgp_paths("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_mtu("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_nve_id("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_routing_tag("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    validations._verify_vni("bb")
except ValueError as err:
    logger.error(f"{err}")

try:
    # param = [1,2,3,4]
    param = 10
    result = validations.list_to_str(param)
    logger.info(result)
except TypeError as err:
    logger.error(f"{err}")

try:
    # param = {1: 'foo', 2: 'bar', "3": 'aaa', 4: 0}
    param = 10
    result = validations.keys_to_str(param)
    logger.info(result)
except TypeError as err:
    logger.error(f"{err}")
