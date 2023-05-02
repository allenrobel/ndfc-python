"""
Common() - common.py

Description:

Common methods, tests, constants, etc, for libraries in this repository
"""
import ipaddress
import re
import sys
from os import path

OUR_VERSION = 115


class Common:
    """
    Common methods, tests, constants, etc, for libraries in this repository
    """

    def __init__(self, log):
        self.class_name = __class__.__name__
        self.lib_version = OUR_VERSION
        self.log = log
        self.properties_set = set()

        self.platform_buffer_boost = [9372]
        self.re_digits = re.compile(r"^\d+$")
        self.re_ipv4 = re.compile(r"^\s*\d+\.\d+\.\d+\.\d+\s*$")
        self.re_ipv4_with_mask = re.compile(r"^\s*(\d+\.\d+\.\d+\.\d+)\/(\d+)\s*$")
        self.re_ethernet_module_port = re.compile(r"^[Ee]thernet\d+\/\d+$")
        self.re_ethernet_module_port_subinterface = re.compile(
            r"^[Ee]thernet\d+\/\d+\.\d+$"
        )
        self.re_ethernet_module_port_subport = re.compile(r"^[Ee]thernet\d+\/\d+\/\d+$")
        self.re_ethernet_module_port_subport_subinterface = re.compile(
            r"^[Ee]thernet\d+\/\d+\/\d+\.\d+$"
        )
        self.re_loopback_interface = re.compile(r"^[Ll]oopback\d+$")
        self.re_management_interface = re.compile(r"^[Mm]gmt\d+$")
        self.re_nve_interface = re.compile(r"^[Nn]ve\d+$")
        self.re_vlan_interface = re.compile(r"^[Vv]lan\d+$")
        self.re_port_channel_interface = re.compile(r"^[Pp]ort-channel\d+$")
        self.re_port_channel_subinterface = re.compile(r"^[Pp]ort-channel\d+\.\d+$")

        # 0011.22aa.bbcc
        self.re_mac_format_a = re.compile(
            r"^[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}$"
        )
        # 00:11:22:aa:bb:cc
        self.re_mac_format_b = re.compile(r"^([0-9a-fA-F]{2}\:){5}[0-9a-fA-F]{2}$")
        # 00-11-22-aa-bb-cc
        self.re_mac_format_c = re.compile(r"^([0-9a-fA-F]{2}\-){5}[0-9a-fA-F]{2}$")

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

        self.valid_enable_disable = set()
        self.valid_enable_disable.add("enable")
        self.valid_enable_disable.add("disable")

        self.valid_enabled_disabled = set()
        self.valid_enabled_disabled.add("enabled")
        self.valid_enabled_disabled.add("disabled")

        self.valid_ip_interface = set()
        self.valid_ip_interface.add("Ethernet")
        self.valid_ip_interface.add("port-channel")
        self.valid_ip_interface.add("Vlan")
        self.valid_ip_interface.add("Loopback")
        self.valid_ip_interface.add("mgmt")
        self.valid_ip_interface.add("Stc")

        self.valid_ip_interface_or_default = set.union(self.valid_ip_interface)
        self.valid_ip_interface_or_default.add("default")

        # used only for self.fail expectation messages
        # Use self.is_*_interface() methods instead when verifying interface input
        self.valid_ip_pim_interface = set()
        self.valid_ip_pim_interface.add("Ethernet")
        self.valid_ip_pim_interface.add("port-channel")
        self.valid_ip_pim_interface.add("Vlan")
        self.valid_ip_pim_interface.add("Loopback")

        self.valid_interface = set.union(self.valid_ip_interface)
        self.valid_interface.add("nve")

        self.valid_interface_or_default = set.union(self.valid_interface)
        self.valid_interface_or_default.add("default")

        self.valid_lldp_interface = set()
        self.valid_lldp_interface.add("Ethernet")

        self.valid_nxos_ip_interface = set()
        self.valid_nxos_ip_interface.add("ethernet")
        self.valid_nxos_ip_interface.add("Ethernet")
        self.valid_nxos_ip_interface.add("port-channel")
        self.valid_nxos_ip_interface.add("vlan")
        self.valid_nxos_ip_interface.add("Vlan")
        self.valid_nxos_ip_interface.add("loopback")
        self.valid_nxos_ip_interface.add("Loopback")
        self.valid_nxos_ip_interface.add("mgmt0")

        self.valid_ospf_interface = set()
        self.valid_ospf_interface.add("Ethernet")
        self.valid_ospf_interface.add("port-channel")
        self.valid_ospf_interface.add("Vlan")
        self.valid_ospf_interface.add("Loopback")

        self.valid_platforms = set()
        self.valid_platforms.add(3064)
        self.valid_platforms.add(3132)
        self.valid_platforms.add(3164)
        self.valid_platforms.add(3172)
        self.valid_platforms.add(3232)
        self.valid_platforms.add(3264)
        self.valid_platforms.add(31108)
        self.valid_platforms.add(7700)
        self.valid_platforms.add(9236)
        self.valid_platforms.add(9332)
        self.valid_platforms.add(9336)
        self.valid_platforms.add(9372)
        self.valid_platforms.add(9504)
        self.valid_platforms.add(9508)
        self.valid_platforms.add(92160)
        self.valid_platforms.add(92304)
        self.valid_platforms.add(93180)

        self.valid_replication_mode = set()
        self.valid_replication_mode.add("Ingress")
        self.valid_replication_mode.add("Multicast")

        self.valid_state = set()
        self.valid_state.add("present")
        self.valid_state.add("absent")
        self.valid_state.add("default")
        self.valid_state.add("merged")

        self.valid_toggle = set()
        self.valid_toggle.add("no")
        self.valid_toggle.add("yes")

        self.valid_true_false = set()
        self.valid_true_false.add("false")
        self.valid_true_false.add("true")

    def all_set(self, d):
        """
        given dict() d, return False if any key in d has a value is None
        Else, return True
        """
        for key in d:
            if d[key] is None:
                return False
        return True

    def remove_null_keys(self, d):
        """
        Given dict() d, return dict() with all key/values from d that
        are not None
        """
        new_dict = {}
        for key in d:
            if d[key] is not None:
                new_dict[key] = d[key]
        return new_dict

    def verify_integer_range(self, params):
        """
        Given dictionary params, with the following key / values:

        params["value"] - The integer value to be tested.
        params["min"] - The minimum range for params["value"]
        params["max"] - The maximum range for params["value"]
        params["source_class"] - Optional, the name of the caller class
        params["source_method"] - Optional, the name of the caller method

        Exit with appropriate error if params["value"] is not within
        integer-range params["min"] and params["max"] inclusive.

        See also: is_within_integer_range() if you want to test a range without failing.
        """
        if not isinstance(params, dict):
            message = (
                "Exiting. Expected params to be a python dict()."
                f" Got type {type(params)} with value {params}."
            )
            self.log.error(message)
            sys.exit(1)
        mandatory_keys = ("value", "min", "max")
        for key in mandatory_keys:
            if key not in params:
                message = f"Exiting. params is missing mandatory key {key}"
                self.log.error(message)
                sys.exit(1)
        if "source_class" not in params:
            params["source_class"] = "unspecified"
        if "source_method" not in params:
            params["source_method"] = "unspecified"
        expectation = (
            f"[int() within range inclusive: {params['min']} - {params['max']}]"
        )
        if self.is_within_integer_range(params["value"], params["min"], params["max"]):
            return
        self.fail(
            params["source_class"],
            params["source_method"],
            params["value"],
            params["source_method"],
            expectation,
        )

    def fail(self, source_class, source_method, value, parameter, expectation):
        """
        log.error() a message and exit.
        """
        message = (
            f"Exiting. {source_class}.{source_method}:"
            f" Unexpected value [{value}] for parameter [{parameter}]."
            f" Expected one of [{expectation}]"
        )
        self.log.error(message)
        sys.exit(1)

    def spaces_to_underscore(self, x):
        """
        Convert all spaces in x to underscores.
        """
        return re.sub(" ", "_", x)

    def any_defined(self, items):
        """
        Return True if any elements of items is not None
        Return False otherwise
        """
        for item in items:
            if item is not None:
                return True
        return False

    def all_defined(self, items):
        """
        Return True if all elements of items are not None
        Return False otherwise
        """
        for item in items:
            if item is None:
                return False
        return True

    def is_within_integer_range(self, x, range_min, range_max):
        """
        Return True if x is within range_min and range_max inclusive
        Return False otherwise

        See also: verify_integer_range() if you want to fail when x is out of range
        """
        if not self.is_digits(x):
            return False
        if int(x) < range_min:
            return False
        if int(x) > range_max:
            return False
        return True

    def is_mac_address_format_a(self, x):
        """
        Return True if x is a mac address with format: xxxx.xxxx.xxxx
        Return False otherwise.
        """
        if self.re_mac_format_a.search(x):
            return True
        return False

    def is_mac_address_format_b(self, x):
        """
        Return True if x is a mac address with format: xx:xx:xx:xx:xx:xx
        Return False otherwise.
        """
        if self.re_mac_format_b.search(x):
            return True
        return False

    def is_mac_address_format_c(self, x):
        """
        Return True if x is a mac address with format: xx-xx-xx-xx-xx-xx
        Return False otherwise.
        """
        if self.re_mac_format_c.search(x):
            return True
        return False

    def is_mac_address(self, x):
        """
        Return True if x is a mac address in any of the following formats:
        xxxx.xxxx.xxxx
        xx:xx:xx:xx:xx
        xx-xx-xx-xx-xx
        x.x.x  (NXOS will left-pad to 000x.000x.000x)
        Return False otherwise.
        """
        if self.is_mac_address_format_a(x):
            return True
        if self.is_mac_address_format_b(x):
            return True
        if self.is_mac_address_format_c(x):
            return True
        return False

    def is_ipv4_address(self, x):
        """
        Return True if x is an IPv4 address
        Return False otherwise
        """
        try:
            ipaddress.IPv4Address(x)
        except ipaddress.AddressValueError as exception:
            message = f"{x} is not a valid ipv4 address: {exception}"
            self.log.error(message)
            return False
        return True

    def is_ipv4_unicast_address(self, x):
        """
        Return True if x is an IPv4 unicast address without prefixlen/mask e.g. 10.1.1.1
        Return False otherwise
        """
        if not self.is_ipv4_address(x):
            return False
        _ip_unicast = ipaddress.IPv4Address(x)
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
        elif re.search(r"\/", x):
            bad_type = "is_subnet"
        if bad_type != "":
            message = f"{x} not a unicast ipv4 address -> {bad_type}"
            self.log.debug(message)
            return False
        return True

    def is_ethernet_interface(self, x):
        """
        Return True if x is an Ethernet interface
        Return False otherwise

        Valid:
            Ethernet1/1
            ethernet1/1
            Ethernet3/2/2
        Invalid:
            Eth1/1.1
            Eth1/1/2
            Ethernet1
        """
        if self.re_ethernet_module_port.search(x):
            return True
        if self.re_ethernet_module_port_subport.search(x):
            return True
        return False

    def is_ethernet_subinterface(self, x):
        """
        Return True if x is an Ethernet subinterface
        Return False otherwise

        Valid:
            Ethernet1/1.1
            ethernet1/1.1
            Ethernet1/2/15.4
        Invalid:
            Eth1/1.1
            Ether1/1.5
        """
        if self.re_ethernet_module_port_subinterface.search(x):
            return True
        if self.re_ethernet_module_port_subport_subinterface.search(x):
            return True
        return False

    def is_ipv4_multicast_address(self, x):
        """
        Return True if x is an IPv4 multicast address
        Return False otherwise
        """
        try:
            _tmp = ipaddress.IPv4Address(x)
            if _tmp.is_multicast:
                return True
        except ipaddress.AddressValueError:
            return False
        return False

    def is_ipv4_multicast_range(self, x):
        """
        Return True if x is an IPv4 multicast range
        Return False otherwise
        """
        if "/" not in x:
            return False
        try:
            if ipaddress.IPv4Interface(x).is_multicast:
                return True
        except ipaddress.AddressValueError as exception:
            print(f"Exception {exception}")
            return False
        except ipaddress.NetmaskValueError as exception:
            print(f"Exception {exception}")
            return False
        return False

    def is_ipv4_address_with_prefix(self, x):
        """
        Return True if x is an IPv4 address with prefix of the form address/Y
        Return False otherwise
        """
        if "/" not in x:
            return False
        try:
            ipaddress.ip_interface(x)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv6_address_with_prefix(self, x):
        """
        Return True if x is an IPv6 address with prefix of the form address/Y
        Return False otherwise
        """
        if "/" not in x:
            return False
        try:
            ipaddress.IPv6Network(x)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv6_address(self, _x):
        """
        Return True if x is an IPv6 address
        Return False otherwise
        """
        try:
            ipaddress.IPv6Address(_x)
        except ipaddress.AddressValueError:
            return False
        return True

    def is_ipv4_network(self, x):
        """
        Return True if x is an IPv4 network
        Return False otherwise
        """
        try:
            ipaddress.IPv4Network(x).subnets(new_prefix=32)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv6_network(self, x):
        """
        Return True if x is an IPv6 network
        Return False otherwise
        """
        try:
            ipaddress.IPv6Network(x).subnets(new_prefix=128)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv4_interface(self, x):
        """
        Return True if x is an IPv4 interface
        Return False otherwise
        """
        try:
            ipaddress.IPv4Interface(x)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_ipv6_interface(self, x):
        """
        Return True if x is an IPv6 interface
        Return False otherwise
        """
        try:
            ipaddress.IPv6Interface(x)
        except ipaddress.AddressValueError:
            return False
        except ipaddress.NetmaskValueError:
            return False
        return True

    def is_digits(self, x):
        """
        verify x contains only digits i.e. is a positive integer
        """
        if not self.re_digits.search(str(x)):
            return False
        return True

    def is_list(self, x):
        """
        verify x is a python list()
        """
        if not isinstance(x, list):
            return False
        return True

    def is_loopback_interface(self, x):
        """
        Return True if x conforms to a loopback interface specification.
        Return False otherwise.
        """
        if self.re_loopback_interface.search(x):
            return True
        return False

    def is_management_interface(self, x):
        """
        Return True if x conforms to a management interface specification.
        Return False otherwise.
        """
        if self.re_management_interface.search(x):
            return True
        return False

    def is_nve_interface(self, x):
        """
        Return True if x conforms to an NVE interface specification.
        Return False otherwise.
        """
        if self.re_nve_interface.search(x):
            return True
        return False

    def is_port_channel_interface(self, x):
        """
        Return True if x conforms to a port-channel interface specification.
        Return False otherwise.
        """
        if self.re_port_channel_interface.search(x):
            return True
        if self.re_port_channel_subinterface.search(x):
            return True
        return False

    def is_auto(self, x):
        """
        Return True if x == "auto"
        Return False otherwise
        """
        if x == "auto":
            return True
        return False

    def is_default(self, x):
        """
        Return True if x == "default"
        Return False otherwise
        """
        if x == "default":
            return True
        return False

    def is_vlan_interface(self, x):
        """
        Return true if x conforms to a vlan interface specification.
        Else, return False.

        Vlan10 conforms.
        Vl10 does not conform.
        """
        if self.re_vlan_interface.search(x):
            return True
        return False

    def is_valid_rd(self, x):
        """
        Return True if x is a route descriptor.
        Else, return false.

        Valid:
            172.20.1.1:65001
            64000:65
        Invalid:
            172.20.1:65001
            6bn:yy
        """
        try:
            asn, nn = re.split(":", x)
        except TypeError:
            return False
        except ValueError:
            return False
        if self.is_digits(asn) and self.is_digits(nn):
            return True
        if self.is_ipv4_address(asn) and self.is_digits(nn):
            return True
        return False

    def verify_rd(self, x, parameter=""):
        """
        Verify x is a valid argument for the NX-OS RD configuration CLI
        Exit if this is not the case.
        """
        source_class = self.class_name
        source_method = "verify_rd"
        expectation = "One of auto, default, x.x.x.x:x, x:x, where x is digits"
        if self.is_auto(x):
            return
        if self.is_default(x):
            return
        if not self.is_valid_rd(x):
            self.fail(source_class, source_method, x, parameter, expectation)

    def verify_rt(self, x, parameter=""):
        """
        Verify x is a valid argument for the NX-OS route-target configuration CLI
        Exit if this is not the case.
        """
        source_class = self.class_name
        source_method = "verify_rt"
        expectation = (
            "auto, default, or python list of x.x.x.x:x, x:x, where x is digits"
        )
        if self.is_auto(x):
            return
        if self.is_default(x):
            return
        if not self.is_list(x):
            self.fail(source_class, source_method, x, parameter, expectation)
        for item in x:
            if not self.is_valid_rd(item):
                self.fail(source_class, source_method, x, parameter, expectation)

    def is_16_bit(self, x):
        """
        Verify x fits within a 16 bit value
        """
        if not self.is_digits(x):
            return False
        x = int(str(x))
        if x in range(0, 65536):
            return True
        return False

    def is_32_bit(self, x):
        """
        Verify x fits within a 32 bit value
        """
        if not self.is_digits(x):
            return False
        x = int(str(x))
        if x in range(0, 4294967296):
            return True
        return False

    def is_bgp_asn(self, x):
        """
        Return True if x is a BGP ASN
        Else return False
        """
        if self.is_digits(x):
            if self.is_32_bit and int(x) >= 1:
                return True
        m = re.search(r"^(\d+)\.(\d+)$", str(x))
        if not m:
            return False
        if not self.is_16_bit(m.group(1)):
            return False
        if not self.is_16_bit(m.group(2)):
            return False
        if int(m.group(1)) <= 0:
            return False
        return True

    def verify_bgp_asn(self, x, parameter="asn"):
        """
        Verify x is a BGP ASN.
        Exit if this is not the case.
        """
        if self.is_bgp_asn(x):
            return
        source_class = self.class_name
        source_method = "verify_bgp_asn"
        expectation = '["digits", "digits.digits"]'
        self.fail(source_class, source_method, x, parameter, expectation)

    def verify_bgp_password_key_type(self, x, parameter=""):
        """
        Return if x is a valid BGP password key type (currently 3, or 7)
        Otherwise exit with error.
        """
        if x in self.valid_bgp_password_key_type:
            return
        expectation = self.valid_bgp_password_key_type
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_digits(self, x, parameter="unspecified"):
        """
        Return if x is digits.
        Otherwise exit with error.
        """
        if self.is_digits(x):
            return
        expectation = "digits"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_digits_or_default(self, x, parameter="unspecified"):
        """
        Return if x is digits, or the string "default"
        Otherwise exit with error.
        """
        if self.is_default(x):
            return
        if self.is_digits(x):
            return
        expectation = "[digits, 'default']"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_address(self, x, parameter="unspecified"):
        """
        Return if x is an IPv4 address
        Otherwise exit with error.
        """
        if self.is_ipv4_address(x):
            return
        expectation = "[ipv4_address e.g. 192.168.1.2]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_ipv6(self, x, parameter="unspecified"):
        """
        Return if x is an IPv6 address
        Otherwise exit with error.
        """
        if self.is_ipv4_address(x):
            return
        if self.is_ipv6_address(x):
            return
        expectation = "[ipv4_address, ipv6_address]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_multicast_address(self, x, parameter="unspecified"):
        """
        Return if x is an IPv4 multicast address without prefix.
        Otherwise exit with error.
        """
        if self.is_ipv4_multicast_address(x):
            return
        expectation = "ipv4 multicast address without prefix e.g. 225.1.1.2"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_multicast_address_with_prefix(self, x, parameter="unspecified"):
        """
        Return if x is an IPv4 multicast address with prefix.
        Otherwise exit with error.
        """
        result = True
        if "/" not in x:
            result = False
        if not self.is_ipv4_multicast_address(re.split("/", x)[0]):
            result = False
        if result is True:
            return
        expectation = "ipv4 multicast address with prefixlen e.g. 225.1.0.0/16"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_address_with_prefix(self, x, parameter="unspecified"):
        """
        Return if x is an IPv4 address with prefix.
        Otherwise exit with error.
        """
        if self.is_ipv4_address_with_prefix(x):
            return
        expectation = "[ipv6 address with prefixlen e.g. 2001:aaaa::1/64]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv6_address_with_prefix(self, x, parameter="unspecified"):
        """
        Return if x is an IPv6 address with prefix.
        Otherwise exit with error.
        """
        if self.is_ipv6_interface(x):
            return
        expectation = "[ipv6 address with prefixlen e.g. 2001:aaaa::1/64]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_ipv6_address_or_network(self, x, parameter="unspecified"):
        """
        Return if x is an IPv4 or IPv6 address or network.
        Otherwise exit with error.

        see nxos_bgp_neighbor_af.py where we use to verify BGP peers
        that may be an address without prefix, or a network (prefix peering)
        """
        if self.is_ipv4_address(x):
            return
        if self.is_ipv4_network(x):
            return
        if self.is_ipv6_address(x):
            return
        if self.is_ipv6_network(x):
            return
        expectation = "[ipv4_address, ipv4_network, ipv6_address, ipv6_network]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_ipv6_or_default(self, x, parameter="unspecified"):
        """
        Return if x is an IPv4 or IPv6 address or the string "default".
        Otherwise exit with error.
        """
        if self.is_default(x):
            return
        if self.is_ipv4_address(x):
            return
        if self.is_ipv6_address(x):
            return
        expectation = "[ipv4_address, ipv6_address, 'default']"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_enable_disable(self, x, parameter=""):
        """
        Return if x is either "enable" or "disable"
        Otherwise exit with error.

        used by (at least) nxos_pim
        """
        for value in self.valid_enable_disable:
            if value in x:
                return
        expectation = self.valid_enable_disable
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_enabled_disabled(self, x, parameter=""):
        """
        Return if x is either "enabled" or "disabled"
        Otherwise exit with error.
        """
        for value in self.valid_enabled_disabled:
            if value in x:
                return
        expectation = self.valid_enabled_disabled
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_file_exists(self, x, parameter=""):
        """
        Return if the file path x exists.
        Otherwise exit with error.
        """
        if path.exists(x):
            return
        self.log.error(f"exiting. {parameter} does not exist: {x}")
        sys.exit(1)

    def verify_interface_or_default(self, x, parameter=""):
        """
        Return if x is an NX-OS interface or is the string "default"
        Otherwise exit with error.
        """
        if self.is_default(x):
            return
        self.verify_interface(x, parameter)

    def verify_interface(self, x, parameter=""):
        """
        Return if x is an NX-OS interface.
        Otherwise exit with error.
        """
        if self.is_ethernet_interface(x):
            return
        if self.is_ethernet_subinterface(x):
            return
        if self.is_port_channel_interface(x):
            return
        if self.is_management_interface(x):
            return
        if self.is_loopback_interface(x):
            return
        if self.is_nve_interface(x):
            return
        if self.is_vlan_interface(x):
            return
        expectation = self.valid_interface
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ip_interface(self, x, parameter=""):
        """
        Return if x is an NX-OS interface capable of L3 configuration.
        Otherwise exit with error.
        """
        if self.is_ethernet_interface(x):
            return
        if self.is_ethernet_subinterface(x):
            return
        if self.is_port_channel_interface(x):
            return
        if self.is_loopback_interface(x):
            return
        if self.is_management_interface(x):
            return
        if self.is_vlan_interface(x):
            return
        expectation = self.valid_ip_interface
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def is_lldp_interface(self, x):
        """
        Return True if x is an LLDP-capable NX-OS interface.
        Otherwise return False.
        """
        for value in self.valid_lldp_interface:
            if value.lower() in x.lower():
                return True
        return False

    def verify_lldp_interface(self, x, parameter=""):
        """
        Return if x is an LLDP-capable NX-OS interface.
        Otherwise exit with error.
        """
        for value in self.valid_lldp_interface:
            if value.lower() in x.lower():
                return
        expectation = self.valid_lldp_interface
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_list(self, x, parameter="unspecified"):
        """
        Return if x is a python list().
        Otherwise exit with error.
        """
        if isinstance(x, list):
            return
        expectation = "list, e.g. [x, y, z]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_list_of_dict(self, x, parameter="unspecified"):
        """
        Return if x is a python list() of dict().
        Otherwise exit with error.
        """
        expectation = (
            'list_of_dict, e.g. [{"x1": 1, "x2": "foo"}, {"y1": 10, "y2": "bar"}]'
        )
        if not isinstance(x, list):
            self.fail(self.class_name, parameter, x, parameter, expectation)
        for d in x:
            if not isinstance(d, dict):
                self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_list_of_list(self, x, parameter="unspecified"):
        """
        Return if x is a python list() of list()s
        Otherwise, exit with error.
        """
        expectation = "list_of_list, e.g. [[x, y], [z]]"
        if not isinstance(x, list):
            self.fail(self.class_name, parameter, x, parameter, expectation)
        for _list in x:
            if not isinstance(_list, list):
                self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_list_or_default(self, x, parameter="unspecified"):
        """
        Return True if x is a python list() or is the string "default"
        Otherwise, exit with error.
        """
        if isinstance(x, list):
            return
        if self.is_default(x):
            return
        expectation = "list_or_default, e.g. [x, y, z] or default"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_replication_mode(self, x, parameter=""):
        """
        Return True if x is a valid replication mode (see self.valid_replication_mode).
        Otherwise, exit with error.
        """
        verify_set = self.valid_replication_mode
        if x not in verify_set:
            expectation = ",".join(verify_set)
            self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_state(self, x, parameter=""):
        """
        Return True if x is a valid state (see self.valid_state).
        Otherwise, exit with error.
        """
        verify_set = self.valid_state
        if x not in verify_set:
            expectation = ",".join(verify_set)
            self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_toggle(self, x, parameter=""):
        """
        Return True if x is a valid toggle (see self.valid_toggle).
        Otherwise, exit with error.
        """
        if x not in self.valid_toggle:
            expectation = ",".join(self.valid_toggle)
            self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_true_false(self, x, parameter=""):
        """
        Return True if x is a valid true or false string (see self.valid_true_false).
        Otherwise, exit with error.
        """
        if x not in self.valid_true_false:
            expectation = ",".join(self.valid_true_false)
            self.fail(self.class_name, parameter, x, parameter, expectation)

    def is_boolean(self, x):
        """
        Return True if x is a boolean.
        Return False otherwise.
        """
        if x in [True, False]:
            return True
        return False

    def verify_boolean(self, x, parameter=""):
        """
        Return if x x is a python boolean type.
        Otherwise, exit with error.
        """
        if self.is_boolean(x):
            return
        expectation = "bool(): True or False"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_vlan(self, x, parameter="verify_vlan"):
        """
        Return if x conforms to a valid NX-OS vlan ID
        Otherwise, exit with error.
        """
        params = {}
        params["value"] = x
        params["min"] = self.min_vlan
        params["max"] = self.max_vlan
        params["source_class"] = self.class_name
        params["source_method"] = parameter
        self.verify_integer_range(params)

    def verify_vrf_vlan_id(self, x, parameter="verify_vrf_vlan_id"):
        """
        Return if x is within an integer range.
        Otherwise, exit with error.
        """
        params = {}
        params["value"] = x
        params["min"] = self.min_vrf_vlan_id
        params["max"] = self.max_vrf_vlan_id
        params["source_class"] = self.class_name
        params["source_method"] = parameter
        self.verify_integer_range(params)

    def verify_loopback_id(self, x, parameter="verify_loopback_id"):
        """
        Return if x conforms to a valid NX-OS loopback interface ID.
        Otherwise, exit with error.
        """
        params = {}
        params["value"] = x
        params["min"] = self.min_loopback_id
        params["max"] = self.max_loopback_id
        params["source_class"] = self.class_name
        params["source_method"] = parameter
        self.verify_integer_range(params)

    def verify_max_bgp_paths(self, x, parameter="verify_max_bgp_paths"):
        """
        Return if x conforms to a valid NX-OS max-bgp-paths value.
        Otherwise, exit with error.
        """
        params = {}
        params["value"] = x
        params["min"] = self.min_max_bgp_paths
        params["max"] = self.max_max_bgp_paths
        params["source_class"] = self.class_name
        params["source_method"] = parameter
        self.verify_integer_range(params)

    def verify_mtu(self, x, parameter="verify_mtu"):
        """
        Return if x conforms to a valid NX-OS MTU value,
        Otherwise, exit with error.
        """
        params = {}
        params["value"] = x
        params["min"] = self.min_mtu
        params["max"] = self.max_mtu
        params["source_class"] = self.class_name
        params["source_method"] = parameter
        self.verify_integer_range(params)

    def verify_nve_id(self, x, parameter="verify_nve_id"):
        """
        Return if x conforms to a valid NX-OS NVE ID.
        Otherwise, exit with error.
        """
        params = {}
        params["value"] = x
        params["min"] = self.min_nve_id
        params["max"] = self.max_nve_id
        params["source_class"] = self.class_name
        params["source_method"] = parameter
        self.verify_integer_range(params)

    def verify_routing_tag(self, x, parameter="verify_routing_tag"):
        """
        Return if x conforms to a valid NX-OS routing tag.
        Otherwise, exit with error.
        """
        params = {}
        params["value"] = x
        params["min"] = self.min_routing_tag
        params["max"] = self.max_routing_tag
        params["source_class"] = self.class_name
        params["source_method"] = parameter
        self.verify_integer_range(params)

    def verify_vni(self, x, parameter="verify_vni"):
        """
        Return if x conforms to a valid NX-OS VNI.
        Otherwise, exit with error.
        """
        params = {}
        params["value"] = x
        params["min"] = self.min_vni
        params["max"] = self.max_vni
        params["source_class"] = self.class_name
        params["source_method"] = parameter
        self.verify_integer_range(params)

    def verify_vlan_list(self, x, parameter="verify_vlan_list"):
        """
        Return if x is a quoted comma-separated list of vlans and vlan ranges.
        Otherwise, exit with error.
        Valid:
            '10,20,30-40,510'
        Not Valid:
            '10-15-20,510'
            'a-b, c'
            '10:20:10-20
        """
        expectation = (
            "comma-separated list of vlans and/or vlan ranges"
            " e.g.: '10,20,411-419' or a single vlan e.g. 10"
        )

        def _verify_min_max(item):
            if int(item) < self.min_vlan:
                self.fail(self.class_name, parameter, x, parameter, expectation)
            if int(item) > self.max_vlan:
                self.fail(self.class_name, parameter, x, parameter, expectation)

        def _verify_int_range(int_range):
            item_list = re.split("-", int_range)
            if len(item_list) != 2:
                self.fail(self.class_name, parameter, x, parameter, expectation)
            for item in item_list:
                self.verify_vlan(item, parameter)
            if int(item_list[0]) >= int(item_list[1]):
                self.fail(self.class_name, parameter, x, parameter, expectation)

        vlan_list = re.split(",", x)
        for item in vlan_list:
            if "-" in item:
                _verify_int_range(item)
                continue
            if not self.is_digits(
                item
            ):  # don't use self.verify_digits() here since we have a different expectation
                self.fail(self.class_name, parameter, x, parameter, expectation)
            _verify_min_max(item)

    def strip_netmask(self, ip):
        """
        Given an IPv4/IPv6 address with /mask, strip /mask and return only address portion
        For example, given 10.0.1.1/31, return 10.0.1.1
        """
        return re.sub(r"\/\d+", "", ip)

    def list_to_str(self, _list):
        """
        Convert all the elements of list _list to str().

        For example:
            [10, "Tree", True, [10,20,30], {"foo": "bar", "baz": 10}]
        Becomes:
            ["10", "Tree", "True", "[10,20,30]", "{'foo': 'bar', 'baz': 10}"]
        """
        return [str(x) for x in _list]

    def keys_to_str(self, d):
        """
        Convert the top-level keys in dictionary d to str()
        """
        new_d = {}
        for k in d:
            new_d[str(k)] = d[k]
        return new_d

    def to_set(self, item):
        """
        Convert item to a set().
        For example:
        if item == "a" -> Return {"a"}
        if item == {"a"} -> Return {"a"}
        if item == 10 -> Return {10}
        if item == None -> Return {None}
        if item == [10, 11, 11] -> Return {10, 11}
        if item == {"foo": "bar", "baz": 10} -> Return {("foo", "bar"), ("baz", 10)}
        """
        if isinstance(item, set):
            return item
        s = set()
        if isinstance(item, dict):
            for k, v in item.items():
                s.add((k, v))
        elif isinstance(item, list):
            for element in item:
                s.add(element)
        else:
            s.add(item)
        return s
