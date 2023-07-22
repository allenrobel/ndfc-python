"""
Common() - common.py

Description:

Common methods, tests, constants, etc, for libraries in this repository
"""
import ipaddress
import re
import sys

OUR_VERSION = 116


class NdfcBgpPasswordKeytypeError(Exception):
    """
    raise for errors related to NDFC bgp password key types
    see e.g. Common().verify_bgp_password_key_type()
    """


class Common:
    """
    Common methods, tests, constants, etc, for libraries in this repository
    """

    def __init__(self, log):
        self.class_name = __class__.__name__
        self.lib_version = OUR_VERSION
        self.log = log

        self.re_digits = re.compile(r"^\d+$")
        self.re_ipv4 = re.compile(r"^\s*\d+\.\d+\.\d+\.\d+\s*$")
        pattern = re.compile(r"^\s*(\d+\.\d+\.\d+\.\d+)\/(\d+)\s*$")
        self.re_ipv4_with_mask = pattern
        self.re_ethernet_module_port = re.compile(r"^[Ee]thernet\d+\/\d+$")
        self.re_ethernet_module_port_subinterface = re.compile(
            r"^[Ee]thernet\d+\/\d+\.\d+$"
        )
        pattern = re.compile(r"^[Ee]thernet\d+\/\d+\/\d+$")
        self.re_ethernet_module_port_subport = pattern
        self.re_ethernet_module_port_subport_subinterface = re.compile(
            r"^[Ee]thernet\d+\/\d+\/\d+\.\d+$"
        )
        self.re_loopback_interface = re.compile(r"^[Ll]oopback\d+$")
        self.re_management_interface = re.compile(r"^[Mm]gmt\d+$")
        self.re_nve_interface = re.compile(r"^[Nn]ve\d+$")
        self.re_vlan_interface = re.compile(r"^[Vv]lan\d+$")
        self.re_port_channel_interface = re.compile(r"^[Pp]ort-channel\d+$")
        pattern = re.compile(r"^[Pp]ort-channel\d+\.\d+$")
        self.re_port_channel_subinterface = pattern

        # 0011.22aa.bbcc
        self.re_mac_format_a = re.compile(
            r"^[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}$"
        )
        # 00:11:22:aa:bb:cc
        pattern = re.compile(r"^([0-9a-fA-F]{2}\:){5}[0-9a-fA-F]{2}$")
        self.re_mac_format_b = pattern
        # 00-11-22-aa-bb-cc
        pattern = re.compile(r"^([0-9a-fA-F]{2}\-){5}[0-9a-fA-F]{2}$")
        self.re_mac_format_c = pattern

        self.min_vlan = 1
        self.max_vlan = 4094

        self.min_vrf_vlan_id = 2
        self.max_vrf_vlan_id = 3967

        self.min_loopback_id = 1
        self.max_loopback_id = 1023

        self.min_max_bgp_paths = 1
        self.max_max_bgp_paths = 64

        self.min_mtu = 1500
        self.max_mtu = 9216

        self.min_nve_id = 1
        self.max_nve_id = 1

        self.min_routing_tag = 0
        self.max_routing_tag = 4294967295

        self.min_vni = 1
        self.max_vni = 16777214

        self.valid_bgp_password_key_type = set()
        self.valid_bgp_password_key_type.add(3)
        self.valid_bgp_password_key_type.add(7)

        self.valid_replication_mode = set()
        self.valid_replication_mode.add("Ingress")
        self.valid_replication_mode.add("Multicast")

    def verify_integer_range(self, params):
        """
        raise ValueError if params.value is not with range
        params.min and params.max

        raise TypeError if params is not a dict()
        raise KeyError if params does not contain the keys below

        params["value"] - The integer value to be tested.
        params["min"] - The minimum range for params["value"]
        params["max"] - The maximum range for params["value"]

        See also: is_within_integer_range() if you want to test a range
        without throwing an exception.
        """
        if not isinstance(params, dict):
            msg = (
                "expected params to be a python dict()."
                f" got type {type(params)} with value {params}."
            )
            raise TypeError(msg)
        mandatory_keys = ("value", "min", "max")
        for key in mandatory_keys:
            if key not in params:
                msg = f"params is missing mandatory key {key}, "
                msg += f"params must contain keys {mandatory_keys}"
                raise KeyError(msg)
        _value = params["value"]
        _min = params["min"]
        _max = params["max"]
        if self.is_within_integer_range(_value, _min, _max):
            return
        msg = f"value {params['value']} not within range "
        msg += f"{params['min']}-{params['max']}"
        raise ValueError(msg)

    def is_within_integer_range(self, param, range_min, range_max):
        """
        Return True if param is within range_min and range_max inclusive
        Return False otherwise

        See also:
        verify_integer_range() throw an exception when param is out of range
        """
        if not self.is_digits(param):
            return False
        if int(param) < range_min:
            return False
        if int(param) > range_max:
            return False
        return True

    def is_mac_address_format_a(self, param):
        """
        Return True if param is a mac address with format: xxxx.xxxx.xxxx
        Return False otherwise.
        """
        if self.re_mac_format_a.search(param):
            return True
        return False

    def is_mac_address_format_b(self, param):
        """
        Return True if param is a mac address with format: xx:xx:xx:xx:xx:xx
        Return False otherwise.
        """
        if self.re_mac_format_b.search(param):
            return True
        return False

    def is_mac_address_format_c(self, param):
        """
        Return True if param is a mac address with format: xx-xx-xx-xx-xx-xx
        Return False otherwise.
        """
        if self.re_mac_format_c.search(param):
            return True
        return False

    def is_mac_address(self, param):
        """
        Return True if x is a mac address in any of the following formats:
        xxxx.xxxx.xxxx
        xx:xx:xx:xx:xx
        xx-xx-xx-xx-xx
        x.x.x  (NXOS will left-pad to 000x.000x.000x)
        Return False otherwise.
        """
        if self.is_mac_address_format_a(param):
            return True
        if self.is_mac_address_format_b(param):
            return True
        if self.is_mac_address_format_c(param):
            return True
        return False

    def is_ipv4_address(self, param):
        """
        Return True if param is an IPv4 address
        Return False otherwise
        """
        try:
            ipaddress.IPv4Address(param)
        except ipaddress.AddressValueError:
            return False
        return True

    def is_ipv4_unicast_address(self, param):
        """
        Return True if param is an IPv4 unicast address without
        prefixlen/mask e.g. 10.1.1.1
        Return False otherwise
        """
        if not self.is_ipv4_address(param):
            return False
        _ip_unicast = ipaddress.IPv4Address(param)
        bad_type = ""
        if _ip_unicast.is_multicast:
            bad_type = "is_multicast"
        elif _ip_unicast.is_loopback:
            bad_type = "is_loopback"
        elif _ip_unicast.is_reserved:
            bad_type = "is_reserved"
        elif _ip_unicast.is_unspecified:
            bad_type = "is_unspecified"
        elif _ip_unicast.is_link_local:
            bad_type = "is_link_local"
        elif re.search(r"\/", param):
            bad_type = "is_subnet"
        if bad_type != "":
            return False
        return True

    def is_ipv4_multicast_address(self, param):
        """
        Return True if param is an IPv4 multicast address
        Return False otherwise
        """
        try:
            _tmp = ipaddress.IPv4Address(param)
            if _tmp.is_multicast:
                return True
        except ipaddress.AddressValueError:
            return False
        return False

    def is_ipv4_multicast_range(self, param):
        """
        Return True if param is an IPv4 multicast range
        Return False otherwise
        """
        if "/" not in param:
            return False
        try:
            if ipaddress.IPv4Interface(param).is_multicast:
                return True
        except ipaddress.AddressValueError as exception:
            print(f"Exception {exception}")
            return False
        except ipaddress.NetmaskValueError as exception:
            print(f"Exception {exception}")
            return False
        return False

    def is_ipv4_address_with_prefix(self, param):
        """
        Return True if x is an IPv4 address with prefix of the form address/Y
        Return False otherwise
        """
        if "/" not in param:
            return False
        try:
            ipaddress.ip_interface(param)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv6_address_with_prefix(self, param):
        """
        Return True if param is an IPv6 address with prefix of the
        form address/Y
        Return False otherwise
        """
        if "/" not in param:
            return False
        try:
            ipaddress.IPv6Network(param)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv6_address(self, param):
        """
        Return True if x is an IPv6 address
        Return False otherwise
        """
        try:
            ipaddress.IPv6Address(param)
        except ipaddress.AddressValueError:
            return False
        return True

    def is_ipv4_network(self, param):
        """
        Return True if x is an IPv4 network
        Return False otherwise
        """
        try:
            ipaddress.IPv4Network(param).subnets(new_prefix=32)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv6_network(self, param):
        """
        Return True if x is an IPv6 network
        Return False otherwise
        """
        try:
            ipaddress.IPv6Network(param).subnets(new_prefix=128)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv4_interface(self, param):
        """
        Return True if x is an IPv4 interface
        Return False otherwise
        """
        try:
            ipaddress.IPv4Interface(param)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv6_interface(self, param):
        """
        Return True if param is an IPv6 interface
        Return False otherwise
        """
        try:
            ipaddress.IPv6Interface(param)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_digits(self, param):
        """
        verify param contains only digits i.e. is a positive integer
        """
        if not self.re_digits.search(str(param)):
            return False
        return True

    def is_list(self, param):
        """
        verify param is a python list()
        """
        if not isinstance(param, list):
            return False
        return True

    def is_loopback_interface(self, param):
        """
        Return True if param conforms to a loopback interface spec.
        Return False otherwise.
        """
        if self.re_loopback_interface.search(param):
            return True
        return False

    def is_management_interface(self, param):
        """
        Return True if param conforms to a management interface spec.
        Return False otherwise.
        """
        if self.re_management_interface.search(param):
            return True
        return False

    def is_nve_interface(self, param):
        """
        Return True if param conforms to an NVE interface spec.
        Return False otherwise.
        """
        if self.re_nve_interface.search(param):
            return True
        return False

    def is_port_channel_interface(self, param):
        """
        Return True if param conforms to a port-channel interface spec.
        Return False otherwise.
        """
        if self.re_port_channel_interface.search(param):
            return True
        if self.re_port_channel_subinterface.search(param):
            return True
        return False

    def is_auto(self, param):
        """
        Return True if param == "auto"
        Return False otherwise
        """
        if param == "auto":
            return True
        return False

    def is_default(self, param):
        """
        Return True if param == "default"
        Return False otherwise
        """
        if param == "default":
            return True
        return False

    @staticmethod
    def verify_bgp_asn(asn):
        """
        Verify that asn conforms to the following NDFC constraint

        1-4294967295 | 1-65535[.0-65535]
        """

        def verify_asn_asplain(item):
            """
            raise ValueError if item is not a number in range 1-4294967295
            This differs from verify_asn_high_order only in the message
            returned
            """
            if int(item) < 1 or int(item) > 4294967295:
                msg = "asplain asn format, asn must be within range "
                msg += f"1-4294967295, got {item}"
                raise ValueError(msg)

        def verify_asn_high_order(item):
            """
            raise ValueError if item is not a number in range 1-4294967295
            """
            if int(item) < 1 or int(item) > 4294967295:
                msg = "asdot asn format (x.y), x must be within range "
                msg += f"1-4294967295, got {item}"
                raise ValueError(msg)

        def verify_asn_low_order(item):
            """
            raise ValueError if item is not a number in range 0-4294967295
            """
            if int(item) < 0 or int(item) > 4294967295:
                msg = "asdot asn format (x.y), y must be within range "
                msg += f"0-4294967295, got {item}"
                raise ValueError(msg)

        asn = str(asn)
        if len(asn.split(".")) == 1:
            try:
                int(asn)
            except ValueError as err:
                msg = "expected asplain (number) or asdot (x.y) "
                msg += f"asn notation, got {asn}"
                raise ValueError(msg) from err
            verify_asn_asplain(asn)
        elif len(str(asn).split(".")) == 2:
            (high_order, low_order) = str(asn).split(".")
            try:
                int(high_order)
                int(low_order)
            except ValueError as err:
                msg = "asdot asn format (x.y), x and y must be numbers, "
                msg += f"got {asn}"
                raise ValueError(msg) from err
            verify_asn_high_order(high_order)
            verify_asn_low_order(low_order)
        else:
            msg = "invalid asn format, expected "
            msg += f"1-4294967295 | 1-65535[.0-65535], got {asn}"
            raise ValueError(msg)

    def verify_bgp_password_key_type(self, param):
        """
        raise ValueError if bgp_password_key_type is not what NDFC expects.
        """
        if param not in self.valid_bgp_password_key_type:
            msg = "bgp_password_key_type must match one of "
            msg += f"{self.valid_bgp_password_key_type}"
            raise ValueError(msg)

    def verify_digits(self, param):
        """
        raise ValueError if param is not digits
        """
        if self.is_digits(param):
            return
        msg = f"expected digits, got {param}"
        raise ValueError(msg)

    def verify_digits_or_default(self, param):
        """
        raise ValueError if param is not digits, or the string 'default'
        """
        if self.is_default(param):
            return
        if self.is_digits(param):
            return
        msg = f"expected digits or the string 'default', got {param}"
        raise ValueError(msg)

    def verify_ipv4_address(self, param):
        """
        raise ipaddress.AddressValueError if param is not an IPv4 address
        """
        if self.is_ipv4_address(param):
            return
        msg = f"expected ipv4 address, got {param}"
        raise ipaddress.AddressValueError(msg)

    def verify_ipv6_address(self, param):
        """
        raise ipaddress.AddressValueError if param is not an IPv6 address
        """
        if self.is_ipv6_address(param):
            return
        msg = f"expected ipv6 address, got {param}"
        raise ipaddress.AddressValueError(msg)

    def verify_ipv4_multicast_address(self, param):
        """
        raise ipaddress.AddressValueError if param is not an IPv4 multicast
        address without prefix
        """
        if self.is_ipv4_multicast_address(param):
            return
        msg = "expected ipv4 multicast address without prefix "
        msg += f"e.g. 225.1.1.2, got {param}"
        raise ipaddress.AddressValueError(msg)

    def verify_ipv4_multicast_address_with_prefix(self, param):
        """
        raise ipaddress.AddressValueError if param is not an IPv4 multicast
        address with prefix
        """
        result = True
        if "/" not in param:
            result = False
        if not self.is_ipv4_multicast_address(re.split("/", param)[0]):
            result = False
        if result is True:
            return
        msg = "expected ipv4 multicast address with prefix "
        msg += f"e.g. 225.1.0.0/16, got {param}"
        raise ipaddress.AddressValueError(msg)

    def verify_ipv4_address_with_prefix(self, param):
        """
        raise ipaddress.AddressValueError if param is not an IPv4 address
        with prefix
        """
        if self.is_ipv4_address_with_prefix(param):
            return
        msg = "expected ipv4 address with prefix e.g. 10.1.0.0/16, "
        msg += f"got {param}"
        raise ipaddress.AddressValueError(msg)

    def verify_ipv6_address_with_prefix(self, param):
        """
        raise ipaddress.AddressValueError if param is not an IPv6 address
        with prefix
        """
        if self.is_ipv6_interface(param):
            return
        msg = "expected ipv6 address with prefix e.g. 2001:aaaa::1/64, "
        msg += f"got {param}"
        raise ipaddress.AddressValueError(msg)

    def verify_list(self, param):
        """
        raise TypeError if param is not a list()
        """
        if not isinstance(param, list):
            msg = f"expected list(), got {type(param).__name__}"
            raise TypeError(msg)

    def verify_list_of_dict(self, param):
        """
        raise TypeError if param is not a list() of dict()
        """
        if not isinstance(param, list):
            msg = f"expected list(), got {type(param).__name__}"
            raise TypeError(msg)
        for elem in param:
            if not isinstance(elem, dict):
                msg = "expected list() of dict(), "
                msg = f" got {type(elem).__name__} for at least one "
                msg += "list element"
                raise TypeError(msg)

    def verify_list_of_list(self, param):
        """
        raise TypeError if param is not a list() of list()
        """
        if not isinstance(param, list):
            msg = f"expected list(), got {type(param).__name__}"
            raise TypeError(msg)
        for elem in param:
            if not isinstance(elem, list):
                msg = "expected list() of list(), "
                msg = f" got {type(elem).__name__} for at least one "
                msg += "list element"
                raise TypeError(msg)

    def verify_list_or_default(self, param):
        """
        raise TypeError if param is not a list() or string "default"
        """
        if isinstance(param, list):
            return
        if self.is_default(param):
            return
        msg = "expected list(), or the string 'default', "
        msg += f"got {type(param).__name__}"
        raise TypeError(msg)

    def verify_replication_mode(self, param):
        """
        raise ValueError if param is not a valid NDFC replication mode
        """
        if param in self.valid_replication_mode:
            return
        msg = "not a valid replication mode, "
        msg += f"expected one of {','.join(self.valid_replication_mode)} "
        msg += f"got {param}"
        raise ValueError(msg)

    def is_boolean(self, param):
        """
        Return True if param is a boolean.
        Return False otherwise.
        """
        if isinstance(param, bool):
            return True
        return False

    def verify_boolean(self, param):
        """
        raise TypeError if param is not a boolean
        """
        if self.is_boolean(param):
            return
        msg = f"expected boolean, got {param}"
        raise TypeError(msg)

    def verify_vlan(self, param):
        """
        raise ValueError if param is not a valid NDFC vlan ID
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_vlan
        params["max"] = self.max_vlan
        try:
            self.verify_integer_range(params)
        except ValueError as err:
            msg = f"vlan id {param} is out of range {err}"
            self.log.error(msg)
            raise
        except TypeError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)

    def verify_vrf_vlan_id(self, param):
        """
        raise ValueError if param is not a valid NDFC vrf vlan ID
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_vrf_vlan_id
        params["max"] = self.max_vrf_vlan_id
        try:
            self.verify_integer_range(params)
        except ValueError as err:
            msg = f"vrf_vlan_id {param} is out of range {err}"
            self.log.error(msg)
            raise
        except TypeError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)

    def verify_loopback_id(self, param):
        """
        raise ValueError if param is not a valid NDFC loopback interface ID
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_loopback_id
        params["max"] = self.max_loopback_id
        try:
            self.verify_integer_range(params)
        except ValueError as err:
            msg = f"loopback_id {param} is out of range {err}"
            self.log.error(msg)
            raise
        except TypeError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)

    def verify_max_bgp_paths(self, param):
        """
        raise ValueError if param is not a valid value
        for NDFC max_bgp_paths
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_max_bgp_paths
        params["max"] = self.max_max_bgp_paths
        try:
            self.verify_integer_range(params)
        except ValueError as err:
            msg = f"max_bgp_paths {param} is out of range {err}"
            raise ValueError(msg) from err
        except TypeError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)

    def verify_mtu(self, param):
        """
        raise ValueError if param is not a valid NDFC MTU
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_mtu
        params["max"] = self.max_mtu
        try:
            self.verify_integer_range(params)
        except ValueError as err:
            msg = f"mtu {param} is out of range {err}"
            self.log.error(msg)
            raise
        except TypeError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)

    def verify_nve_id(self, param):
        """
        raise ValueError if param is not a valid NDFC nve ID
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_nve_id
        params["max"] = self.max_nve_id
        try:
            self.verify_integer_range(params)
        except ValueError as err:
            msg = f"nve_id {param} is out of range {err}"
            self.log.error(msg)
            raise
        except TypeError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)

    def verify_routing_tag(self, param):
        """
        raise ValueError if param is not a valid NDFC routing tag
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_routing_tag
        params["max"] = self.max_routing_tag
        try:
            self.verify_integer_range(params)
        except ValueError as err:
            msg = f"routing_tag {param} is out of range {err}"
            self.log.error(msg)
            raise
        except TypeError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)

    def verify_vni(self, param):
        """
        raise ValueError if param is not a valid NDFC vni value
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_vni
        params["max"] = self.max_vni
        try:
            self.verify_integer_range(params)
        except ValueError as err:
            msg = f"vni {param} is out of range {err}"
            self.log.error(msg)
            raise
        except TypeError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"exiting {err}"
            self.log.error(msg)
            sys.exit(1)

    def strip_netmask(self, param):
        """
        Given an IPv4/IPv6 address with /mask, strip /mask and
        return the address portion.

        For example, given 10.0.1.1/31, return 10.0.1.1
        """
        return re.sub(r"\/\d+", "", param)

    def list_to_str(self, param):
        """
        Convert all the elements of list param to str().
        Raise TypeError if param is not a list.

        For example:
            [10, "Tree", True, [10,20,30], {"foo": "bar", "baz": 10}]
        Becomes:
            ["10", "Tree", "True", "[10,20,30]", "{'foo': 'bar', 'baz': 10}"]
        """
        if self.is_list(param):
            return [str(item) for item in param]
        msg = f"expected list, got type {type(param).__name__} "
        msg += f"for param {param}"
        raise TypeError(msg)

    def keys_to_str(self, param):
        """
        Convert the top-level keys in dictionary param to str()
        """
        if isinstance(param, dict):
            # break this out from the comprehension only to avoid
            # conflict between black and pylint linter opinions on
            # line length...
            zipped = zip(param.keys(), param.values())
            return {str(key): value for key, value in zipped}
        msg = f"expected dict, got type {type(param).__name__} "
        msg += f"for param {param}"
        raise TypeError(msg)

    def to_set(self, item):
        """
        Convert item to a set().
        For example:
        if item == "a" -> {"a"}
        if item == {"a"} -> {"a"}
        if item == 10 -> {10}
        if item == None -> {None}
        if item == [10, 11, 11] -> {10, 11}
        if item == {"foo": "bar", "baz": 10} -> {("foo", "bar"), ("baz", 10)}
        """
        if isinstance(item, set):
            return item
        _set = set()
        if isinstance(item, dict):
            for key, value in item.items():
                _set.add((key, value))
        elif isinstance(item, list):
            for element in item:
                _set.add(element)
        else:
            _set.add(item)
        return _set
