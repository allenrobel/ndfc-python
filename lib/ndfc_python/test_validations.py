#!/usr/bin/env python
"""
Name: test_validations
Description: unit tests for the validations in validations.py
"""
from ndfc_python.log import log
from ndfc_python.validations import Validations

logger = log("tmp_test_ndfc_common", "INFO", "DEBUG")
validations = Validations()


def bgp_asn(param):
    """
    test bgp_asn
    """
    try:
        validations.verify_bgp_asn(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def bgp_password_key_type(param):
    """
    test bgp_password_key_type
    """
    try:
        validations.verify_bgp_password_key_type(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def keys_to_str(param):
    """
    test keys_to_str
    """
    try:
        result = validations.keys_to_str(param)
        logger.info(result)
    except TypeError as err:
        msg = f"{err}"
        logger.error(msg)


def list_to_string(param):
    """
    test list_to_string
    """
    try:
        result = validations.list_to_str(param)
        logger.info(result)
    except TypeError as err:
        msg = f"{err}"
        logger.error(msg)


def loopback_id(param):
    """
    test loopback_id
    """
    try:
        validations.verify_loopback_id(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def macsec_algorithm(param):
    """
    test macsec_algorithm
    """
    try:
        validations.verify_macsec_algorithm(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def max_bgp_paths(param):
    """
    test max_bgp_paths
    """
    try:
        validations.verify_max_bgp_paths(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def mtu(param):
    """
    test mtu
    """
    try:
        validations.verify_mtu(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def nve_id(param):
    """
    test nve_id
    """
    try:
        validations.verify_nve_id(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def routing_tag(param):
    """
    test routing_tag
    """
    try:
        validations.verify_routing_tag(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def rp_count(param):
    """
    test rp_count
    """
    try:
        validations.verify_rp_count(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def string_length(params):
    """
    test string length
    params is a dict with expected keys:
       - length, int, expected length of test string
       - string, str, test string
    """
    try:
        validations.verify_string_length(params)
    except (KeyError, TypeError, ValueError) as err:
        msg = f"verify_string_length. {err}"
        logger.error(msg)


def vlan(param):
    """
    test vlan
    """
    try:
        validations.verify_vlan(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def vni(param):
    """
    test vni
    """
    try:
        validations.verify_vni(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


def vrf_vlan_id(param):
    """
    test vrf_vlan_id
    """
    try:
        validations.verify_vrf_vlan_id(param)
    except ValueError as err:
        msg = f"{err}"
        logger.error(msg)


bgp_asn("bb")
bgp_password_key_type("bb")
keys_to_str(10)
keys_to_str({1: "foo", 2: "bar", "3": "aaa", 4: 0})
list_to_string(10)
list_to_string([1, 2, 3, 4])
loopback_id("bb")
# valid value
macsec_algorithm("AES_128_CMA")
# bad value
macsec_algorithm("bad_macsec_algorithm")
max_bgp_paths("bb")
mtu("bb")
nve_id("bb")
routing_tag("bb")
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
vlan("bb")
vrf_vlan_id("bb")
vni("bb")
