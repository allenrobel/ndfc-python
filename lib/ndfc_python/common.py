# Common() - common/common.py
our_version = 112
'''
====================
Common() - common.py
====================

Description
-----------

Common methods used by NDFC Python

'''
import re
from os import path
import ipaddress

class Common(object):
    '''
    '''
    def __init__(self, log):
        self.class_name = __class__.__name__
        self.lib_version = our_version
        self.log = log
        self.properties_set = set()

        self.platform_buffer_boost = [9372]
        self.re_digits = re.compile('^\d+$')
        self.re_ipv4 = re.compile('^\s*\d+\.\d+\.\d+\.\d+\s*$')
        self.re_ipv4_with_mask = re.compile('^\s*(\d+\.\d+\.\d+\.\d+)\/(\d+)\s*$')
        self.re_ethernet_module_port                      = re.compile('^[Ee]thernet\d+\/\d+$')
        self.re_ethernet_module_port_subinterface         = re.compile('^[Ee]thernet\d+\/\d+\.\d+$')
        self.re_ethernet_module_port_subport              = re.compile('^[Ee]thernet\d+\/\d+\/\d+$')
        self.re_ethernet_module_port_subport_subinterface = re.compile('^[Ee]thernet\d+\/\d+\/\d+\.\d+$')
        self.re_loopback_interface = re.compile('^[Ll]oopback\d+$')
        self.re_management_interface = re.compile('^[Mm]gmt\d+$')
        self.re_nve_interface = re.compile('^[Nn]ve\d+$')
        self.re_vlan_interface = re.compile('^[Vv]lan\d+$')
        self.re_port_channel_interface = re.compile('^[Pp]ort-channel\d+$')
        self.re_port_channel_subinterface = re.compile('^[Pp]ort-channel\d+\.\d+$')

        self.re_mac_format_a = re.compile('^[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}$')
        self.re_mac_format_b = re.compile('^[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}$')
        self.re_mac_format_c = re.compile('^[0-9a-fA-F]{2}\-[0-9a-fA-F]{2}\-[0-9a-fA-F]{2}\-[0-9a-fA-F]{2}\-[0-9a-fA-F]{2}\-[0-9a-fA-F]{2}$')
        self.re_mac_format_d = re.compile('^[0-9a-fA-F]\.[0-9a-fA-F]\.[0-9a-fA-F]$')

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
        self.valid_enable_disable.add('enable')
        self.valid_enable_disable.add('disable')

        self.valid_enabled_disabled = set()
        self.valid_enabled_disabled.add('enabled')
        self.valid_enabled_disabled.add('disabled')

        self.valid_ip_interface = set()
        self.valid_ip_interface.add('Ethernet')
        self.valid_ip_interface.add('port-channel')
        self.valid_ip_interface.add('Vlan')
        self.valid_ip_interface.add('Loopback')
        self.valid_ip_interface.add('mgmt')
        self.valid_ip_interface.add('Stc')

        self.valid_ip_interface_or_default = set.union(self.valid_ip_interface)
        self.valid_ip_interface_or_default.add('default')

        # used only for self.fail expectation messages
        # Use self.is_*_interface() methods instead when verifying interface input
        self.valid_ip_pim_interface = set()
        self.valid_ip_pim_interface.add('Ethernet')
        self.valid_ip_pim_interface.add('port-channel')
        self.valid_ip_pim_interface.add('Vlan')
        self.valid_ip_pim_interface.add('Loopback')

        self.valid_interface = set.union(self.valid_ip_interface)
        self.valid_interface.add('nve')

        self.valid_interface_or_default = set.union(self.valid_interface)
        self.valid_interface_or_default.add('default')

        self.valid_lldp_interface = set()
        self.valid_lldp_interface.add('Ethernet')

        self.valid_nxos_ip_interface = set()
        self.valid_nxos_ip_interface.add('ethernet')
        self.valid_nxos_ip_interface.add('Ethernet')
        self.valid_nxos_ip_interface.add('port-channel')
        self.valid_nxos_ip_interface.add('vlan')
        self.valid_nxos_ip_interface.add('Vlan')
        self.valid_nxos_ip_interface.add('loopback')
        self.valid_nxos_ip_interface.add('Loopback')
        self.valid_nxos_ip_interface.add('mgmt0')

        self.valid_ospf_interface = set()
        self.valid_ospf_interface.add('Ethernet')
        self.valid_ospf_interface.add('port-channel')
        self.valid_ospf_interface.add('Vlan')
        self.valid_ospf_interface.add('Loopback')

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
        self.valid_replication_mode.add('Ingress')
        self.valid_replication_mode.add('Multicast')

        self.valid_state = set()
        self.valid_state.add('present')
        self.valid_state.add('absent')
        self.valid_state.add('default')
        self.valid_state.add('merged')

        self.valid_toggle = set()
        self.valid_toggle.add('no')
        self.valid_toggle.add('yes')

        self.valid_true_false = set()
        self.valid_true_false.add('false')
        self.valid_true_false.add('true')

    def all_set(self, d):
        '''
        given dict() d, return False if any key in d has a value == None
        Else, return True
        '''
        for key in d:
            if d[key] == None:
                return False
        return True

    def remove_null_keys(self, d):
        '''
        Given dict() d, return dict() with all key/values from d that
        are != None
        '''
        new_dict = dict()
        for key in d:
            if d[key] != None:
                new_dict[key] = d[key]
        return new_dict

    @property
    def vrf(self):
        return self.properties['vrf']
    @vrf.setter
    def vrf(self, x):
        '''
        Ansible enforces no spaces so we replace all spaces with "_"
        '''
        self.properties['vrf'] = self.spaces_to_underscore(x)

    def set_none(self, x, parameter):
        '''
        In subclasses of Common() we need to (re)set a given parameter
        to None if it had been previously set and we want the current task 
        not to include the parameter.  This method provides a way to do this
        while keeping the call site as simple as possible.

        Usage example, from NxosBgpNeighborAf() in nxos_bgp_neighbor_af.py:

        @property
        def afi(self):
            return self.properties['afi']
        @afi.setter
        def afi(self, x):
            parameter = 'afi'
            if self.set_none(x, parameter):
                return
            self.verify_afi(x, parameter)
            self.properties[parameter] = x
        '''
        if x != None:
            return False
        self.properties[parameter] = None
        return True

    def verify_integer_range(self, x, range_min, range_max, source_class='unspecified', source_method='unspecified'):
        '''
        Exit with appropriate error if x is not within range_min and range_max inclusive.

        See also: is_within_integer_range() if you want to test a range without failing.
        '''
        expectation = '[int() within range inclusive {} - {}]'.format(range_min, range_max)
        if self.is_within_integer_range(x, range_min, range_max):
            return
        self.fail(source_class, source_method, x, source_method, expectation)

    def msg(self, source_class, source_method, value):
        print('{}.{}: {}'.format(source_class, source_method, value))

    def fail(self, source_class, source_method, value, parameter, expectation):
        print('{}.{}: exiting.  unexpected value [{}] for parameter [{}]. Expected one of [{}]'.format(
            source_class, source_method, value, parameter, expectation))
        exit(1)

    def spaces_to_underscore(self,x):
        return re.sub(' ', '_', x)

    def any_defined(self, items):
        for item in items:
            if item != None:
                return True
        return False

    def all_defined(self, items):
        for item in items:
            if item == None:
                return False
        return True

    def is_within_integer_range(self, x, range_min, range_max):
        '''
        Return True if x is within range_min and range_max inclusive
        Return False otherwise

        See also: verify_integer_range() if you want to fail when x is out of range
        '''
        if not self.is_digits(x):
            return False
        if int(x) < range_min:
            return False
        if int(x) > range_max:
            return False
        return True

    def is_mac_address_format_a(self, x):
        '''
        verify x is a mac address with format: xxxx.xxxx.xxxx
        '''
        if self.re_mac_format_a.search(x):
            return True
        return False
    def is_mac_address_format_b(self, x):
        '''
        verify x is a mac address with format: xx:xx:xx:xx:xx:xx
        '''
        if self.re_mac_format_b.search(x):
            return True
        return False
    def is_mac_address_format_c(self, x):
        '''
        verify x is a mac address with format: xx-xx-xx-xx-xx-xx
        '''
        if self.re_mac_format_c.search(x):
            return True
        return False
    def is_mac_address_format_d(self, x):
        '''
        verify x is a mac address with format: x.x.x
        '''
        if self.re_mac_format_d.search(x):
            return True
        return False

    def is_mac_address(self, x):
        '''
        verify x i a mac address in any of the following formats:
        xxxx.xxxx.xxxx
        xx:xx:xx:xx:xx
        xx-xx-xx-xx-xx
        x.x.x  (NXOS will left-pad to 000x.000x.000x)
        '''
        if self.is_mac_address_format_a(x):
            return True
        if self.is_mac_address_format_b(x):
            return True
        if self.is_mac_address_format_c(x):
            return True
        if self.is_mac_address_format_d(x):
            return True
        return False

    def is_ipv4_address(self,x):
        '''
        verify x is an ipv4 address
        '''
        try:
            _tmp = ipaddress.IPv4Address(x)
        except:
            return False
        return True

    def is_ipv4_unicast_address(self,x):
        '''verify x is an ipv4 unicast address without prefixlen/mask e.g. 10.1.1.1'''
        try:
            _ip_unicast = ipaddress.IPv4Address(x)
        except ValueError as e:
            self.log.error("{} not a valid ipv4 address: {}".format(x, e))
            return False
        bad_type = ''
        if _ip_unicast.is_multicast:
            bad_type = 'is_multicast'
        elif _ip_unicast.is_loopback:
            bad_type = 'is_loopback'
        elif _ip_unicast.is_reserved:
            bad_type = 'is_reserved'
        elif _ip_unicast.is_unspecified:
            bad_type = 'is_unspecified'
        elif _ip_unicast.is_link_local:
            bad_type = 'is_link_local'
        elif re.search('\/',x):
            bad_type = 'is_subnet'
        if bad_type != '':
            self.log.debug("{} not a unicast ipv4 address -> {}".format(x, bad_type))
            return False
        return True

    def is_ethernet_interface(self, x):
        if self.re_ethernet_module_port.search(x):
            return True
        if self.re_ethernet_module_port_subport.search(x):
            return True
        return False

    def is_ethernet_subinterface(self, x):
        if self.re_ethernet_module_port_subinterface.search(x):
            return True
        if self.re_ethernet_module_port_subport_subinterface.search(x):
            return True
        return False

    def is_ipv4_multicast_address(self,x):
        '''
        verify x is an ipv4 multicast address
        '''
        try:
            _tmp = ipaddress.IPv4Address(x)
            if _tmp.is_multicast:
                return True
        except:
            return False
        return False

    def is_ipv4_multicast_range(self,x):
        '''
        verify x is an ipv4 multicast range
        '''
        if '/' not in x:
            return False
        try:
            _tmp = ipaddress.IPv4Interface(x)
            if _tmp.is_multicast:
                return True
        except:
            return False
        return False

    def is_ipv4_address_with_prefix(self,x):
        '''
        verify x is an ipv4 address with prefix of the form address/Y
        '''
        if '/' not in x:
            return False
        try:
            _tmp = ipaddress.ip_interface(x)
            del _tmp
        except:
            return False
        return True

    def is_ipv6_address_with_prefix(self,x):
        '''
        verify x is an ipv6 address with prefix of the form address/Y
        '''
        if '/' not in x:
            return False
        try:
            _tmp = ipaddress.ip_interface(x)
            del _tmp
        except:
            return False
        return True

    def is_ipv6_address(self, _x):
        '''
        verify _x is an ipv6 address
        '''
        try:
            _tmp = ipaddress.IPv6Address(_x)
            del _tmp
        except:
            return False
        return True

    def is_ipv4_network(self,x):
        try:
            _tmp = ipaddress.IPv4Network(x).subnets(new_prefix=32)
            del _tmp
        except:
            return False
        return True

    def is_ipv6_network(self,x):
        try:
            _tmp = ipaddress.IPv6Network(x).subnets(new_prefix=128)
            del _tmp
        except:
            return False
        return True

    def is_ipv4_interface(self,x):
        try:
            _tmp = ipaddress.IPv4Interface(x)
            del _tmp
        except:
            return False
        return True

    def is_ipv6_interface(self,x):
        try:
            _tmp = ipaddress.IPv6Interface(x)
            del _tmp
        except:
            return False
        return True

    def is_digits(self,x):
        '''
        verify x contains only digits i.e. is a positive integer
        '''
        if not self.re_digits.search(str(x)):
            return False
        return True

    def is_list(self,x):
        '''
        verify x is a python list()
        '''
        if not type(x) == type(list()):
            return False
        return True

    def is_loopback_interface(self, x):
        if self.re_loopback_interface.search(x):
            return True
        return False

    def is_management_interface(self, x):
        if self.re_management_interface.search(x):
            return True
        return False

    def is_nve_interface(self, x):
        if self.re_nve_interface.search(x):
            return True
        return False

    def is_port_channel_interface(self, x):
        if self.re_port_channel_interface.search(x):
            return True
        if self.re_port_channel_subinterface.search(x):
            return True
        return False

    def is_auto(self, x):
        if x == 'auto':
            return True
        return False

    def is_default(self, x):
        if x == 'default':
            return True
        return False

    def is_valid_rd(self, x):
        try:
            asn,nn = re.split(':', x)
        except:
            return False
        if self.is_digits(asn) and self.is_digits(nn):
            return True
        if self.is_ipv4_address(asn) and self.is_digits(nn):
            return True
        return False

    def is_vlan_interface(self, x):
        if self.re_vlan_interface.search(x):
            return True
        return False

    def verify_rd(self, x, parameter=''):
        source_class = self.class_name
        source_method = 'verify_rd'
        expectation = 'One of auto, default, x.x.x.x:x, x:x, where x is digits'
        if self.is_auto:
            return
        if self.is_default:
            return
        if not self.is_valid_rd(x):
            self.fail(source_class, source_method, x, parameter, expectation)

    def verify_rt(self, x, parameter=''):
        source_class = self.class_name
        source_method = 'verify_rt'
        expectation = 'auto, default, or python list of x.x.x.x:x, x:x, where x is digits'
        if self.is_auto:
            return
        if self.is_default:
            return
        if not self.is_list(x):
            self.fail(source_class, source_method, x, parameter, expectation)
        for item in x:
            if not self.is_valid_rd(item):
                self.fail(source_class, source_method, x, parameter, expectation)

    def is_16_bit(self, x):
        if not self.is_digits(x):
            return False
        x = int(str(x))
        if x >= 0 and x <= 65535:
            return True
        return False

    def is_32_bit(self, x):
        if not self.is_digits(x):
            return False
        x = int(str(x))
        if x >= 0 and x <= 4294967295:
            return True
        return False

    def is_bgp_asn(self, x):
        if self.is_digits(x):
            if self.is_32_bit and int(x) >= 1:
                return True
        m = re.search('^(\d+)\.(\d+)$', str(x))
        if not m:
            return False
        if not self.is_16_bit(m.group(1)):
            return False
        if not self.is_16_bit(m.group(2)):
            return False
        if int(m.group(1)) <= 0:
            return False
        return True

    def verify_bgp_asn(self, x, parameter='asn'):
        if self.is_bgp_asn(x):
            return
        source_class = self.class_name
        source_method = 'verify_bgp_asn'
        expectation = '["digits", "digits.digits"]'
        self.fail(source_class, source_method, x, parameter, expectation)

    def verify_bgp_password_key_type(self, x, parameter=''):
        if x in self.valid_bgp_password_key_type:
            return
        expectation = self.valid_bgp_password_key_type
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_digits(self, x, parameter='unspecified'):
        if self.is_digits(x):
            return
        expectation = 'digits'
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_digits_or_default(self, x, parameter='unspecified'):
        if self.is_default(x):
            return
        if self.is_digits(x):
            return
        expectation = "[digits, 'default']"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_address(self, x, parameter='unspecified'):
        if self.is_ipv4_address(x):
            return
        expectation = "[ipv4_address e.g. 192.168.1.2]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_ipv6(self, x, parameter='unspecified'):
        if self.is_ipv4_address(x):
            return
        if self.is_ipv6_address(x):
            return
        expectation = "[ipv4_address, ipv6_address]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_multicast_address(self, x, parameter='unspecified'):
        if self.is_ipv4_multicast_address(x):
            return
        expectation = "ipv4 multicast address without prefix e.g. 225.1.1.2"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_multicast_address_with_prefix(self, x, parameter='unspecified'):
        result = True
        if '/' not in x:
            result = False
        if not self.is_ipv4_multicast_address(re.split('/', x)[0]):
            result = False
        if result == True:
            return
        expectation = "ipv4 multicast address with prefixlen e.g. 225.1.0.0/16"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_address_with_prefix(self, x, parameter='unspecified'):
        if self.is_ipv4_address_with_prefix(x):
            return
        expectation = "[ipv6 address with prefixlen e.g. 2001:aaaa::1/64]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv6_address_with_prefix(self, x, parameter='unspecified'):
        if self.is_ipv6_interface(x):
            return
        expectation = "[ipv6 address with prefixlen e.g. 2001:aaaa::1/64]"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_ipv4_ipv6_address_or_network(self, x, parameter='unspecified'):
        '''
        see nxos_bgp_neighbor_af.py where we use to verify BGP peers
        that may be an address without prefix, or a network (prefix peering)
        '''
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

    def verify_ipv4_ipv6_or_default(self, x, parameter='unspecified'):
        if self.is_default(x):
            return
        if self.is_ipv4_address(x):
            return
        if self.is_ipv6_address(x):
            return
        expectation = "[ipv4_address, ipv6_address, 'default']"
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_enable_disable(self, x, parameter=''):
        '''
        verify x is either 'enable' or 'disable'

        used by (at least) nxos_pim
        '''
        for value in self.valid_enable_disable:
            if value in x:
                return
        expectation = self.valid_enable_disable
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_enabled_disabled(self, x, parameter=''):
        '''
        verify x is either 'enabled' or 'disabled'
        '''
        for value in self.valid_enabled_disabled:
            if value in x:
                return
        expectation = self.valid_enabled_disabled
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_file_exists(self, x, parameter=''):
        if path.exists(x):
            return
        self.log.error('exiting. {} does not exist: {}'.format(parameter, x))
        exit(1)

    def verify_interface_or_default(self, x, parameter=''):
        if self.is_default(x):
            return
        self.verify_interface(x, parameter)

    def verify_interface(self, x, parameter=''):
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

    def verify_ip_interface(self, x, parameter=''):
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
        for value in self.valid_lldp_interface:
            if value.lower() in x.lower():
                return True
        return False

    def verify_lldp_interface(self, x, parameter=''):
        for value in self.valid_lldp_interface:
            if value.lower() in x.lower():
                return
        expectation = self.valid_lldp_interface
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_list(self, x, parameter='unspecified'):
        if type(x) == type(list()):
            return
        expectation = 'list, e.g. [x, y, z]'
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_list_of_dict(self, x, parameter='unspecified'):
        expectation = 'list_of_dict, e.g. [{"x1": 1, "x2": "foo"}, {"y1": 10, "y2": "bar", "y3": "baz"}]'
        if type(x) != type(list()):
            self.fail(self.class_name, parameter, x, parameter, expectation)
        for d in x:
            if type(d) != type(dict()):
                self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_list_of_list(self, x, parameter='unspecified'):
        expectation = 'list_of_list, e.g. [[x, y], [z]]'
        if type(x) != type(list()):
            self.fail(self.class_name, parameter, x, parameter, expectation)
        for l in x:
            if type(l) != type(list()):
                self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_list_or_default(self, x, parameter='unspecified'):
        if type(x) == type(list()):
            return
        if self.is_default(x):
            return
        expectation = 'list_or_default, e.g. [x, y, z] or default'
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_replication_mode(self, x, parameter=''):
        verify_set = self.valid_replication_mode
        if x not in verify_set:
            expectation = ','.join(verify_set)
            self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_state(self, x, parameter=''):
        verify_set = self.valid_state
        if x not in verify_set:
            expectation = ','.join(verify_set)
            self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_toggle(self, x, parameter=''):
        if x not in self.valid_toggle:
            expectation = ','.join(self.valid_toggle)
            self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_true_false(self, x, parameter=''):
        if x not in self.valid_true_false:
            expectation = ','.join(self.valid_true_false)
            self.fail(self.class_name, parameter, x, parameter, expectation)

    def is_boolean(self, x):
        if x in [True, False]:
            return True
        return False
    def verify_boolean(self, x, parameter=''):
        if self.is_boolean(x):
            return
        expectation = 'bool(): True or False'
        self.fail(self.class_name, parameter, x, parameter, expectation)

    def verify_vlan(self, x, parameter='verify_vlan'):
        self.verify_integer_range(x, self.min_vlan, self.max_vlan, self.class_name, 'verify_vlan')

    def verify_vrf_vlan_id(self, x, parameter='verify_vrf_vlan_id'):
        self.verify_integer_range(x, self.min_vrf_vlan_id, self.max_vrf_vlan_id, self.class_name, 'verify_vlan')

    def verify_loopback_id(self, x, expectation, parameter='verify_loopback_id'):
        self.verify_integer_range(x, self.min_loopback_id, self.max_loopback_id, self.class_name, 'verify_loopback_id')

    def verify_max_bgp_paths(self, x, expectation, parameter='verify_max_bgp_paths'):
        self.verify_integer_range(x, self.min_max_bgp_paths, self.max_max_bgp_paths, self.class_name, 'verify_max_bgp_paths')

    def verify_mtu(self, x, expectation, parameter='verify_mtu'):
        self.verify_integer_range(x, self.min_mtu, self.max_mtu, self.class_name, 'verify_mtu')

    def verify_nve_id(self, x, expectation, parameter='verify_nve_id'):
        self.verify_integer_range(x, self.min_nve_id, self.max_nve_id, self.class_name, 'verify_nve_id')

    def verify_routing_tag(self, x, expectation, parameter='verify_routing_tag'):
        self.verify_integer_range(x, self.min_routing_tag, self.max_routing_tag, self.class_name, 'verify_routing_tag')

    def verify_vni(self, x, parameter='verify_vni'):
        self.verify_integer_range(x, self.min_vni, self.max_vni, self.class_name, 'verify_vni')

    def verify_vlan_list(self, x, parameter='unspecified'):
        '''
        verify that x is a quoted comma-separated list of vlans and vlan ranges e.g.:

        '10,20,30-40,510'
        '''
        expectation = 'comma-separated list of vlans and/or vlan ranges e.g.: "10,20,411-419" or a single vlan e.g. 10'
        def _verify_min_max(item):
            if int(item) < self.min_vlan:
                self.fail(self.class_name, parameter, x, parameter, expectation)
            if int(item) > self.max_vlan:
                self.fail(self.class_name, parameter, x, parameter, expectation)
        def _verify_int_range(int_range):
            item_list = re.split('-', int_range)
            if len(item_list) != 2:
                self.fail(self.class_name, parameter, x, parameter, expectation)
            for item in item_list:
                self.verify_vlan(item, expectation, parameter)
            if int(item_list[0]) >= int(item_list[1]):
                self.fail(self.class_name, parameter, x, parameter, expectation)

        vlan_list = re.split(',', x)
        for item in vlan_list:
            if '-' in item:
                _verify_int_range(item)
                continue
            if not self.is_digits(item): # don't use self.verify_digits() here since we have a different expectation
                self.fail(self.class_name, parameter, x, parameter, expectation)
            _verify_min_max(item)

    def fail(self, source_class, source_method, value, parameter, expectation):
        self.log.error('{}.{}: exiting.  unexpected value [{}] for parameter [{}]. Expected one of [{}]'.format(
            source_class, source_method, value, parameter, expectation))
        exit(1)


    def strip_netmask(self,ip):
        '''given ipv4/ipv6 address with /mask, strip /mask and return only address portion
           For example, given 10.0.1.1/31, return 10.0.1.1
        '''
        return re.sub('\/\d+','',ip)


    def list_to_str(self, l):
        return [str(x) for x in l]
    def keys_to_str(self, d):
        '''
        convert top-level keys in dictionary d to str()
        '''
        new_d = dict()
        for k in d:
            new_d[str(k)] = d[k]
        return new_d


    def to_set(self, item):
        if type(item) == type(set()):
            return item
        s = set()
        if type(item) == type(None):
            pass
        elif type(item) == type(list()):
            for element in item:
                s.add(element)
        else:
            s.add(item)
        return s
