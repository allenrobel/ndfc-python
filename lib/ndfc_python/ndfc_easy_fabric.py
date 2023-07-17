"""
Name: ndfc_easy_fabric.py
Description: Create fabric using the NDFC Easy_Fabric template
"""
import sys

from ndfc_python.ndfc_fabric import NdfcFabric

OUR_VERSION = 105


class NdfcEasyFabric(NdfcFabric):
    """
    Create site/child fabrics using Easy_Fabric template.

    Example create operation:

    instance = NdfcEasyFabric(ndfc)
    instance.fabric_name = 'bang'
    instance.bgp_as = 65011
    instance.replication_mode = 'Ingress'
    instance.create()

    TODO: Need a delete() method
    """

    def __init__(self, ndfc):
        super().__init__(ndfc)
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        self._init_properties_set()
        self._init_properties_mandatory_set()
        self._init_nv_pairs_default()
        self._init_nv_pairs_set()
        self._init_nv_pairs_mandatory_set()
        self._init_properties_default()
        self._init_properties()
        self._init_nv_pairs()

    def _init_properties_set(self):
        """
        Initialize a set containing all properties
        """
        self.properties_set = set()
        self.properties_set.add("fabric_name")

    def _init_properties_mandatory_set(self):
        """
        Initialize a set containing mandatory properties
        """
        self.properties_mandatory_set = set()
        self.properties_mandatory_set.add("fabric_name")

    def _init_nv_pairs_default(self):
        """
        Initialize default values for nv pairs
        """
        self._nv_pairs_default = {}
        self._nv_pairs_default["ANYCAST_RP_IP_RANGE"] = ""
        self._nv_pairs_default["DCI_SUBNET_RANGE"] = "10.33.0.0/16"
        self._nv_pairs_default["ENABLE_PVLAN"] = False
        self._nv_pairs_default["FABRIC_MTU"] = "9216"
        self._nv_pairs_default["LOOPBACK0_IP_RANGE"] = "10.2.0.0/22"
        self._nv_pairs_default["LOOPBACK1_IP_RANGE"] = "10.3.0.0/22"
        self._nv_pairs_default["REPLICATION_MODE"] = "Ingress"
        self._nv_pairs_default["SUBNET_RANGE"] = "10.4.0.0/16"
        self._nv_pairs_default[
            "network_extension_template"
        ] = "Default_Network_Extension_Universal"
        self._nv_pairs_default[
            "vrf_extension_template"
        ] = "Default_VRF_Extension_Universal"

    def _init_nv_pairs_set(self):
        """
        Initialize a set containing all nv pairs
        """
        self._nv_pairs_set = set()
        self._nv_pairs_set.add("ANYCAST_RP_IP_RANGE")
        self._nv_pairs_set.add("BGP_AS")
        self._nv_pairs_set.add("DCI_SUBNET_RANGE")
        self._nv_pairs_set.add("ENABLE_PVLAN")
        self._nv_pairs_set.add("FABRIC_MTU")
        self._nv_pairs_set.add("LOOPBACK0_IP_RANGE")
        self._nv_pairs_set.add("LOOPBACK1_IP_RANGE")
        self._nv_pairs_set.add("REPLICATION_MODE")
        self._nv_pairs_set.add("SUBNET_RANGE")
        self._nv_pairs_set.add("network_extension_template")
        self._nv_pairs_set.add("vrf_extension_template")

    def _init_nv_pairs_mandatory_set(self):
        """
        Initialize a set containing mandatory nv pairs
        """
        self.nv_pairs_mandatory_set = set()
        self.nv_pairs_mandatory_set = self._nv_pairs_set.difference(
            self._nv_pairs_default
        )

    def _init_properties_default(self):
        """
        Initialize default properties (currently there are no default properties)
        """
        self.properties_default = {}

    def _init_properties(self):
        """
        Initialize all properties
        """
        self.properties = {}
        for param in self.properties_set:
            if param in self.properties_default:
                self.properties[param] = self.properties_default[param]
            else:
                self.properties[param] = ""

    def _init_nv_pairs(self):
        """
        All properties, except fabric, live in nv_pairs
        """
        self._nv_pairs = {}
        for param in self._nv_pairs_set:
            if param in self._nv_pairs_default:
                self._nv_pairs[param] = self._nv_pairs_default[param]
            else:
                self._nv_pairs[param] = ""

    def _preprocess_properties(self):
        """
        1. Align the properties to the expectations of NDFC
        """

    def _final_verification(self):
        for param in self.properties_mandatory_set:
            if self.properties[param] == "":
                msg = f"exiting. call instance.{param.lower()} before calling instance.post()"
                self.ndfc.log.error(msg)
                sys.exit(1)
        for param in self.nv_pairs_mandatory_set:
            if self._nv_pairs[param] == "":
                msg = f"exiting. call instance.{param.lower()} before calling instance.post()"
                self.ndfc.log.error(msg)
                sys.exit(1)

    def create(self):
        """
        Create a fabric using Easy_Fabric template.
        """
        self._final_verification()
        self._preprocess_properties()

        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}/Easy_Fabric"

        headers = {}
        headers["Authorization"] = self.ndfc.bearer_token
        headers["Content-Type"] = "application/json"

        self.ndfc.post(url, headers, self._nv_pairs)

    # nvPairs
    @property
    def anycast_rp_ip_range(self):
        """
        return the current nv_pairs value of anycast_rp_ip_range
        """
        return self._nv_pairs["ANYCAST_RP_IP_RANGE"]

    @anycast_rp_ip_range.setter
    def anycast_rp_ip_range(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self._nv_pairs["ANYCAST_RP_IP_RANGE"] = param

    @property
    def bgp_as(self):
        """
        return the current nv_pairs value of bgp_as
        """
        return self._nv_pairs["BGP_AS"]

    @bgp_as.setter
    def bgp_as(self, param):
        self.ndfc.verify_bgp_asn(param)
        self._nv_pairs["BGP_AS"] = param

    @property
    def dci_subnet_range(self):
        """
        return the current nv_pairs value of dci_subnet_range
        """
        return self._nv_pairs["DCI_SUBNET_RANGE"]

    @dci_subnet_range.setter
    def dci_subnet_range(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self._nv_pairs["DCI_SUBNET_RANGE"] = param

    @property
    def enable_pvlan(self):
        """
        return the current nv_pairs value of enable_pvlan
        """
        return self._nv_pairs["ENABLE_PVLAN"]

    @enable_pvlan.setter
    def enable_pvlan(self, param):
        self._nv_pairs["ENABLE_PVLAN"] = param

    @property
    def fabric_mtu(self):
        """
        return the current nv_pairs value of fabric_mtu
        """
        return self._nv_pairs["FABRIC_MTU"]

    @fabric_mtu.setter
    def fabric_mtu(self, param):
        self._nv_pairs["FABRIC_MTU"] = param

    @property
    def loopback0_ip_range(self):
        """
        return the current nv_pairs value of loopback0_ip_range
        """
        return self._nv_pairs["LOOPBACK0_IP_RANGE"]

    @loopback0_ip_range.setter
    def loopback0_ip_range(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self._nv_pairs["LOOPBACK0_IP_RANGE"] = param

    @property
    def loopback1_ip_range(self):
        """
        return the current nv_pairs value of loopback1_ip_range
        """
        return self._nv_pairs["LOOPBACK1_IP_RANGE"]

    @loopback1_ip_range.setter
    def loopback1_ip_range(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self._nv_pairs["LOOPBACK1_IP_RANGE"] = param

    @property
    def replication_mode(self):
        """
        return the current nv_pairs value of replication_mode
        """
        return self._nv_pairs["REPLICATION_MODE"]

    @replication_mode.setter
    def replication_mode(self, param):
        self.ndfc.verify_replication_mode(param)
        self._nv_pairs["REPLICATION_MODE"] = param

    @property
    def subnet_range(self):
        """
        return the current nv_pairs value of subnet_range
        """
        return self._nv_pairs["SUBNET_RANGE"]

    @subnet_range.setter
    def subnet_range(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self._nv_pairs["SUBNET_RANGE"] = param
