"""
Name: validations.py
Description: Validation methods for libraries in this repository
"""

import ipaddress
import re

from ndfc_python.ndfc import NDFC  # verify_ndfc()

OUR_VERSION = 121


class Validations:
    """
    Validation methods and constants for libraries in this repository
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.lib_version = OUR_VERSION

        self._ndfc_fabric_name_length = 64

        self.re_digits = re.compile(r"^\d+$")
        self.re_ipv4 = re.compile(r"^\s*\d+\.\d+\.\d+\.\d+\s*$")
        pattern = re.compile(r"^\s*(\d+\.\d+\.\d+\.\d+)\/(\d+)\s*$")
        self.re_ipv4_with_mask = pattern
        self.re_ethernet_module_port = re.compile(r"^[Ee]thernet\d+\/\d+$")
        self.re_ethernet_module_port_subinterface = re.compile(r"^[Ee]thernet\d+\/\d+\.\d+$")
        pattern = re.compile(r"^[Ee]thernet\d+\/\d+\/\d+$")
        self.re_ethernet_module_port_subport = pattern
        self.re_ethernet_module_port_subport_subinterface = re.compile(r"^[Ee]thernet\d+\/\d+\/\d+\.\d+$")
        self.re_loopback_interface = re.compile(r"^[Ll]oopback\d+$")
        self.re_management_interface = re.compile(r"^[Mm]gmt\d+$")
        self.re_nve_interface = re.compile(r"^[Nn]ve\d+$")
        self.re_vlan_interface = re.compile(r"^[Vv]lan\d+$")
        self.re_port_channel_interface = re.compile(r"^[Pp]ort-channel\d+$")
        pattern = re.compile(r"^[Pp]ort-channel\d+\.\d+$")
        self.re_port_channel_subinterface = pattern

        # 0011.22aa.bbcc
        self.re_mac_format_a = re.compile(r"^[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}$")
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

        self.min_igmp_version = 1
        self.max_igmp_version = 3
        self.valid_igmp_versions = [1, 2, 3]

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

        # dictionary, keyed on property name, containing
        # valid values for properties whose values are a
        # list of specific choices.
        self._valid = {}
        self._valid["dhcp_ipv6_enable"] = {"DHCPv4"}
        self._valid["fabric_interface_type"] = {"p2p", "unnumbered"}
        self._valid["link_state_routing"] = {"is-is", "ospf"}
        self._valid["macsec_algorithm"] = {"AES_128_CMAC", "AES_256_CMAC"}
        self._valid["macsec_cipher_suite"] = {
            "GCM-AES-XPN-256",
            "GCM-AES-128",
            "GCM-AES-256",
            "GCM-AES-XPN-128",
        }
        self._valid["rp_count"] = {2, 4}
        self._valid["rr_count"] = {2, 4}
        self._valid["rp_mode"] = {"asm", "bidir"}
        self._valid["stp_root_option"] = {"mst", "rpvst+", "unmanaged"}

        self._valid["bgp_password_key_type"] = set()
        self._valid["bgp_password_key_type"].add(3)
        self._valid["bgp_password_key_type"].add(7)

        self._valid["border_gwy_connections"] = set()
        self._valid["border_gwy_connections"].add("Manual")
        self._valid["border_gwy_connections"].add("Direct_To_BGWS")
        value = "Centralized_To_Route_Server"
        self._valid["border_gwy_connections"].add(value)

        self._valid["replication_mode"] = set()
        self._valid["replication_mode"].add("Ingress")
        self._valid["replication_mode"].add("Multicast")
        self._valid["vpc_peer_keep_alive_option"] = set()
        self._valid["vpc_peer_keep_alive_option"].add("management")
        self._valid["vpc_peer_keep_alive_option"].add("loopback")

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

    @staticmethod
    def verify_hypenated_range(params):
        """
        Given a string with format "X-Y" where:
            X is convertable to integer, e.g. "1", "1532"
            Y is convertable to integer
        Verify the following:
            int(X) >= params["min"]
            int(Y) <= params["max"]
            int(X) < int(Y)
        raise KeyError if params does not contain all expected keys
        raise ValueError if any of the above verifications fail
        raise ValueError if params["value"] is not of format "digits-digits"
        raise TypeError if params["min"] or params["max"] are not type int

        Example params:

        params = {
            "value": "15-26000",
            "min": 1,
            "max": 28740
        }
        """
        if not isinstance(params, dict):
            msg = f"expected dict, got type {type(params).__name__} "
            msg += f"with value {params}"
            raise TypeError(msg)
        mandatory_keys = {"value", "min", "max"}
        if not mandatory_keys.issubset(params):
            msg = "missing expected key. "
            msg += f"expected {mandatory_keys}, got {params.keys()}"
            raise KeyError(msg)
        if not isinstance(params["max"], int):
            msg = f"expected type int for max, got {params['max']}."
            raise TypeError(msg)
        if not isinstance(params["min"], int):
            msg = f"expected type int for min, got {params['min']}."
            raise TypeError(msg)
        try:
            _match = re.search(r"^(\d+)-(\d+)$", params["value"])
        except TypeError as err:
            msg = f"expected string with format X-Y. Got {params['value']} "
            msg += f"(type {type(params['value']).__name__}). "
            msg += f"Error detail: {err}"
            raise ValueError(msg) from err
        if not _match:
            msg = "expected string with format X-Y, where X "
            msg += f"and Y are digits.  Got {params['value']}"
            raise ValueError(msg)
        try:
            _lower = int(_match.group(1))
            _upper = int(_match.group(2))
        except ValueError as err:
            msg = "hyphenated range values not convertable "
            msg += "to int().  expected integer-integer, got "
            msg += f"{params['value']}"
            raise ValueError(msg) from err
        if not _lower >= params["min"]:
            msg = f"expected X-Y, where X >= {params['min']}. "
            msg += f"got X {_lower}"
            raise ValueError(msg)
        if not _upper <= params["max"]:
            msg = f"expected X-Y, where Y <= {params['max']}. "
            msg += f"got Y {_upper}"
            raise ValueError(msg)
        if _lower >= _upper:
            msg = "expected X-Y, X < Y. "
            msg += f"got X {_lower}, Y {_upper}"
            raise ValueError(msg)

    @staticmethod
    def verify_keys(args):
        """
        Verify that args["keys"] are present in args["dict"]

        args is a dict() with the following keys:
        - keys: a set() of keys that are expected in dict
        - dict: the dictionary to test

        raise TypeError if args is not a dict
        raise KeyError if args does not contain keys "keys" and "dict"
        raise TypeError if args["keys"] is not a set()
        raise TypeError if args["dict"] is not a dict()
        raise KeyError if args["dict"] does not contain all args["keys"]
        """
        if not isinstance(args, dict):
            msg = f"expected dict. got {args}"
            raise TypeError(msg)
        mandatory_keys = {"keys", "dict"}
        if not mandatory_keys.issubset(args):
            msg = "missing internal keys. "
            msg += f"expected {mandatory_keys} "
            msg += f"got: {args.keys()}"
            raise KeyError(msg)
        if not isinstance(args["keys"], set):
            msg = "keys (bad type): expected python set(). "
            msg += f"got {type(args['keys']).__name__}"
            raise TypeError(msg)
        if not isinstance(args["dict"], dict):
            msg = "keys (bad type): expected python dict(). "
            msg += f"got {type(args['dict']).__name__}"
            raise TypeError(msg)
        if not args["keys"].issubset(args["dict"]):
            msg = f"missing keys. expected {','.join(sorted(args['keys']))}, "
            msg += f"got {','.join(sorted(args['dict'].keys()))}"
            raise KeyError(msg)

    @staticmethod
    def is_integer_even(param):
        """
        Return True if param is even
        Return False otherwise
        raise TypeError if param is not an integer
        """
        if not isinstance(param, int):
            msg = f"expected integer, got {param}"
            raise TypeError(msg)
        if param % 2 == 0:
            return True
        return False

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

    @staticmethod
    def is_ipv4_address(param):
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

    @staticmethod
    def is_ipv4_multicast_address(param):
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

    @staticmethod
    def is_ipv4_multicast_range(param):
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

    @staticmethod
    def is_ipv4_address_with_prefix(param):
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

    @staticmethod
    def is_ipv4_network_range(param):
        """
        Check if param is a valid network range (per NDFC's expectations).

        NDFC expects a "/" in address ranges, whereas ipaddress considers
        e.g. 10.0.0.0 to be a valid network i.e. 10.0.0.0/32.  Hence,
        we make an additional check for "/" in param.

        Also, NDFC expects a smaller prefix than the host prefix (/32),
        so we check for that too.
        """
        if not isinstance(param, str):
            return False
        if "/" not in param:
            return False
        try:
            value = ipaddress.IPv4Network(param)
        except ipaddress.AddressValueError:
            return False
        if "/32" in str(value):
            return False
        return True

    @staticmethod
    def is_ipv6_address_with_prefix(param):
        """
        Return True if param is an IPv6 address with prefix of the
        form address/Y
        Return False otherwise
        """
        if not isinstance(param, str):
            return False
        if "/" not in param:
            return False
        try:
            ipaddress.IPv6Network(param)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    @staticmethod
    def is_ipv6_address(param):
        """
        Return True if x is an IPv6 address
        Return False otherwise
        """
        try:
            ipaddress.IPv6Address(param)
        except ipaddress.AddressValueError:
            return False
        return True

    def is_ipv6_unicast_address(self, param):
        """
        Return True if param is an IPv4 unicast address without
        prefixlen/mask e.g. 2001::1
        Return False otherwise
        """
        if not self.is_ipv6_address(param):
            return False
        _addr = ipaddress.IPv6Address(param)
        bad_type = ""
        if _addr.is_multicast:
            bad_type = "is_multicast"
        elif _addr.is_loopback:
            bad_type = "is_loopback"
        elif _addr.is_reserved:
            bad_type = "is_reserved"
        elif _addr.is_unspecified:
            bad_type = "is_unspecified"
        elif _addr.is_link_local:
            bad_type = "is_link_local"
        elif re.search(r"\/", param):
            bad_type = "is_subnet"
        if bad_type != "":
            return False
        return True

    @staticmethod
    def is_ipv6_network_range(param):
        """
        Check if param is a valid network range (per NDFC's expectations).

        NDFC expects a "/" in address ranges, whereas ipaddress considers
        e.g. 2001::0 to be a valid network i.e. 2001::0/128.  Hence,
        we make an additional check for "/" in param.

        Also, NDFC expects a smaller prefix than the host prefix (/128),
        so we check for that too.
        """
        if not isinstance(param, str):
            return False
        if "/" not in param:
            return False
        try:
            value = ipaddress.IPv6Network(param)
        except ipaddress.AddressValueError:
            return False
        if "/128" in str(value):
            return False
        return True

    @staticmethod
    def is_ipv4_network(param):
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

    @staticmethod
    def is_ipv6_network(param):
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

    @staticmethod
    def is_ipv4_interface(param):
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

    @staticmethod
    def is_ipv6_interface(param):
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

    @staticmethod
    def is_list(param):
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

    @staticmethod
    def is_auto(param):
        """
        Return True if param == "auto"
        Return False otherwise
        """
        if param == "auto":
            return True
        return False

    @staticmethod
    def is_default(param):
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
        raise ValueError if asn does not conform to the following
        NDFC constraint

        1-4294967295 | 1-65535[.0-65535]
        """

        def _verify_asn_asplain(item):
            """
            raise ValueError if item is not a number in range 1-4294967295
            This differs from verify_asn_high_order only in the message
            returned
            """
            if int(item) < 1 or int(item) > 4294967295:
                msg = "asplain asn format, asn must be within range "
                msg += f"1-4294967295, got {item}"
                raise ValueError(msg)

        def _verify_asn_high_order(item):
            """
            raise ValueError if item is not a number in range 1-4294967295
            """
            if int(item) < 1 or int(item) > 4294967295:
                msg = "asdot asn format (x.y), x must be within range "
                msg += f"1-4294967295, got {item}"
                raise ValueError(msg)

        def _verify_asn_low_order(item):
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
            _verify_asn_asplain(asn)
        elif len(str(asn).split(".")) == 2:
            (high_order, low_order) = str(asn).split(".")
            try:
                int(high_order)
                int(low_order)
            except ValueError as err:
                msg = "asdot asn format (x.y), x and y must be numbers, "
                msg += f"got {asn}"
                raise ValueError(msg) from err
            _verify_asn_high_order(high_order)
            _verify_asn_low_order(low_order)
        else:
            msg = "invalid asn format, expected "
            msg += f"1-4294967295 | 1-65535[.0-65535], got {asn}"
            raise ValueError(msg)

    def verify_bgp_password_key_type(self, param):
        """
        raise ValueError if bgp_password_key_type is not what NDFC expects.
        caller is optional.  Use if you want your error message to include
        that information.
        """
        if param not in self._valid["bgp_password_key_type"]:
            msg = f"expected one of {self._valid['bgp_password_key_type']}, "
            msg += f"got {param}"
            raise ValueError(msg)

    def verify_bgp_rp_asn_list(self, param):
        """
        raise TypeError if param is not a list.
        raise ValueError if any element in param does not meet NDFC's
        expectations for a BGP ASN.
        """
        if not isinstance(param, list):
            msg = f"expected python list, got {type(param).__name__} ({param})"
            raise TypeError(msg)
        try:
            for asn in param:
                self.verify_bgp_asn(asn)
        except ValueError as err:
            raise ValueError(err) from err

    def verify_border_gwy_connections(self, param):
        """
        raise ValueError if param does not match a valid border gateway
        connection type.
        """
        if param in self._valid["border_gwy_connections"]:
            return
        connections = ",".join(self._valid["border_gwy_connections"])
        msg = f"Invalid value ({param}). "
        msg += f"Expected one of [{connections}]"
        raise ValueError(msg)

    @staticmethod
    def verify_disable_enable(param):
        """
        raise ValueError if param is not one of "Disable" or "Enable"
        """
        _valid = ["Disable", "Enable"]
        if param in _valid:
            return
        msg = f"expected one of {_valid}, got {param}"
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

    def verify_fabric_name(self, param):
        """
        raise TypeError if param is not a string
        raise ValueError if param does not conform to NDFC's constraints
        on fabric_name.

        Else, return.

        NDFC's constraints are:

        1. alphanumeric (a-z, A-Z, 0-9), underscore(_) and hyphen(-) accepted
        2. numbers alone, not accepted
        3. max length is 64 characters

        TODO: Move this to a common library
        """
        if not isinstance(param, str):
            raise TypeError(f"expected str. got {type(param).__name__}")
        if len(param) > self._ndfc_fabric_name_length:
            msg = f"fabric_name must be <= 64 characters, got {param} "
            raise ValueError(msg)
        if not re.match("^[a-zA-Z0-9_-]+$", param):
            msg = "fabric_name must contain only upper/lowercase letters, "
            msg += f"numbers, hyphen, and underscore, got {param} "
            raise ValueError(msg)
        if re.match("^[0-9]+$", param):
            msg = f"fabric_name cannot contain ONLY numbers, got {param}"
            raise ValueError(msg)

    def verify_ndfc(self, param):
        """
        raise AttributeError if param is None or ""
        raise TypeError if param is not an NDFC() instance
        """
        if param is None or param == "":
            msg = "exiting. instance.ndfc is not set.  "
            msg += "Call instance.ndfc = <ndfc instance> to interact with "
            msg += "your NDFC."
            raise AttributeError(msg)
        if not isinstance(param, NDFC):
            msg = "exiting. expected instance of NDFC. "
            msg += f"got {type(param).__name__}"
            raise TypeError(msg)

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

    def verify_ipv4_network_range(self, param):
        """
        raise ipaddress.AddressValueError if param is not an IPv4 network range
        """
        if self.is_ipv4_network_range(param):
            return
        msg = "expected ipv4 network range e.g. 10.1.0.0/X, "
        msg += f" where X <= 31. got {param}"
        raise ipaddress.AddressValueError(msg)

    def verify_ipv6_network_range(self, param):
        """
        raise ipaddress.AddressValueError if param is not an IPv6 network range
        """
        if self.is_ipv6_network_range(param):
            return
        msg = "expected ipv6 network range e.g. 2001::0/X, "
        msg += f" where X <= 127. got {param}"
        raise ipaddress.AddressValueError(msg)

    def verify_list(self, param):
        """
        raise TypeError if param is not a list()
        """
        if not isinstance(param, list):
            msg = f"expected list(), got {type(param).__name__}"
            raise TypeError(msg)

    @staticmethod
    def verify_list_lengths_are_equal(list_a, list_b):
        """
        raise ValueError if lists are not of equal length
        raise TypeError if either list_a or list_b  is not a python list
        """
        if not isinstance(list_a, list):
            raise TypeError(f"not a list. {list_a}")
        if not isinstance(list_b, list):
            raise TypeError(f"not a list. {list_b}")
        if len(list_a) != len(list_b):
            msg = "lists must be of equal length, got lengths "
            msg += f"{len(list_a)} and {len(list_b)} for lists "
            msg += f"{list_a} and {list_b}"
            raise ValueError(msg)

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

    def verify_macsec_algorithm(self, param):
        """
        raise ValueError if param does not conform to NDFC's expectations
        for macsec algorithm
        """
        if param in self._valid["macsec_algorithm"]:
            return
        msg = "expected one of "
        msg += f"{self._valid['macsec_algorithm']}, got {param}"
        raise ValueError(msg)

    @staticmethod
    def verify_property_has_value(param, value):
        """
        raise ValueError if value of param is "" or None
        """
        if value == "" or value is None:
            msg = f"missing value for mandatory property {param}"
            raise ValueError(msg)

    def verify_replication_mode(self, param):
        """
        raise ValueError if param is not a valid NDFC replication mode
        """
        if param in self._valid["replication_mode"]:
            return
        msg = "not a valid replication mode, "
        msg += f"expected one of {','.join(self._valid['replication_mode'])} "
        msg += f"got {param}"
        raise ValueError(msg)

    @staticmethod
    def verify_string_length(params):
        """
        Given params dictionary with the following keys:

        string : the string to be validated
        length : integer, max length for string

        Verify that string is <= length

        raise KeyError if all mandatory keys are not present in params
        raise TypeError if params["string"] is not str() type
        raise TypeError if params["length"] is not int() type
        raise ValueError if string length validation fails
        """
        if not isinstance(params, dict):
            msg = "expected params to be dict, got params with type "
            msg += f"{type(params).__name__}, value {params}"
            raise TypeError(msg)
        mandatory_keys = ["string", "length"]
        for key in mandatory_keys:
            if key not in params:
                msg = f"params is missing mandatory key {key} "
                msg += f"expected keys: {','.join(mandatory_keys)}"
                raise KeyError(msg)
        if not isinstance(params["string"], str):
            msg = "expected str() type for param string. "
            msg += f"got type {type(params['string']).__name__} with "
            msg += f"value {params['string']}"
            raise TypeError(msg)
        if not isinstance(params["length"], int):
            msg = "expected int() type for param length. "
            msg += f"got type {type(params['length']).__name__} with "
            msg += f"value {params['length']}"
            raise TypeError(msg)
        if len(params["string"]) > params["length"]:
            msg = f"expected string with <= {params['length']} characters, "
            msg += f"got {params['string']}"
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
            msg = "expected params to be a python dict()." f" got type {type(params)}, value {params}."
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
        msg = f"{params['value']} not within range "
        msg += f"{params['min']}-{params['max']}"
        raise ValueError(msg)

    def verify_rp_count(self, param):
        """
        verify rp_count conforms to NDFC's expectations
        """
        if param in self._valid["rp_count"]:
            return
        msg = "expected integer with value in: "
        msg += f"{self._valid['rp_count']}. got {param}"
        raise ValueError(msg)

    def verify_rp_mode(self, param):
        """
        verify rp_mode conforms to NDFC's expectations
        """
        if param in self._valid["rp_mode"]:
            return
        msg = "expected string with value in: "
        msg += f"{self._valid['rp_mode']}. got {param}"
        raise ValueError(msg)

    def verify_rp_server_ip_list(self, param):
        """
        raise TypeError if param is not a python list
        raise ipaddress.AddressValueError if any element in param is not an
        ipv4 address with format X.X.X.X e.g. 10.1.1.1
        """
        if not isinstance(param, list):
            msg = "expected python list. "
            msg += f"got {param}"
            raise TypeError(msg)
        for item in param:
            try:
                self.verify_ipv4_address(item)
            except ipaddress.AddressValueError as err:
                raise ipaddress.AddressValueError(err) from err

    def verify_rr_count(self, param):
        """
        verify rr_count conforms to NDFC's expectations
        """
        if param in self._valid["rr_count"]:
            return
        msg = "expected integer with value in: "
        msg += f"{self._valid['rr_count']}. got {param}"
        raise ValueError(msg)

    def verify_stp_root_option(self, param):
        """
        raise ValueError of stp_root_option does not conforms to
        NDFC's expectations.
        """
        if param in self._valid["stp_root_option"]:
            return
        msg = "expected string with value in: "
        msg += f"{self._valid['stp_root_option']}. Got {param}"
        raise ValueError(msg)

    def verify_vlan(self, param):
        """
        raise ValueError if param is not a valid NDFC vlan ID
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_vlan
        params["max"] = self.max_vlan
        params["item"] = "vlan_id"
        self.verify_integer_range(params)

    def verify_vpc_peer_keepalive_option(self, param):
        """
        verify vpc_peer_keepalive_option conforms to NDFC's expectations
        """
        if param in self._valid["vpc_peer_keepalive_option"]:
            return
        msg = "expected string with value in: "
        msg += f"{self._valid['vpc_peer_keepalive_option']}. got {param}"
        raise ValueError(msg)

    def verify_vrf_vlan_id(self, param):
        """
        raise ValueError if param is not a valid NDFC vrf vlan ID
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_vrf_vlan_id
        params["max"] = self.max_vrf_vlan_id
        params["item"] = "vrf_vlan_id"
        self.verify_integer_range(params)

    def verify_loopback_id(self, param):
        """
        raise ValueError if param is not a valid NDFC loopback interface ID
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_loopback_id
        params["max"] = self.max_loopback_id
        params["item"] = "loopback_id"
        self.verify_integer_range(params)

    def verify_max_bgp_paths(self, param):
        """
        raise ValueError if param is not a valid value
        for NDFC max_bgp_paths
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_max_bgp_paths
        params["max"] = self.max_max_bgp_paths
        params["item"] = "max_bgp_paths"
        self.verify_integer_range(params)

    def verify_mtu(self, param):
        """
        raise ValueError if param is not a valid NDFC MTU
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_mtu
        params["max"] = self.max_mtu
        params["item"] = "mtu"
        self.verify_integer_range(params)

    def verify_nve_id(self, param):
        """
        raise ValueError if param is not a valid NDFC nve ID
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_nve_id
        params["max"] = self.max_nve_id
        params["item"] = "nve_id"
        self.verify_integer_range(params)

    def verify_routing_tag(self, param):
        """
        raise ValueError if param is not a valid NDFC routing tag
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_routing_tag
        params["max"] = self.max_routing_tag
        params["item"] = "routing_tag"
        self.verify_integer_range(params)

    def verify_vni(self, param):
        """
        raise ValueError if param is not a valid NDFC vni value
        """
        params = {}
        params["value"] = param
        params["min"] = self.min_vni
        params["max"] = self.max_vni
        params["item"] = "vni"
        self.verify_integer_range(params)

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
