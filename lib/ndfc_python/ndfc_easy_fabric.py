"""
Name: ndfc_easy_fabric.py
Description: Create fabric using the NDFC Easy_Fabric template
"""
import copy
import json
import sys
from ipaddress import AddressValueError
from re import sub

from ndfc_python.ndfc_fabric import NdfcFabric, NdfcRequestError

OUR_VERSION = 112


class NdfcEasyFabric(NdfcFabric):
    """
    Create fabrics using the NDFC Easy_Fabric template.

    Example create operation:

    from ndfc_python.log import log
    from ndfc_python.ndfc import NDFC
    from ndfc_python.ndfc_fabric import NdfcFabric

    logger = log('example_log', 'INFO', 'DEBUG')
    ndfc = NDFC()
    ndfc.log = logger
    ndfc.username = "admin"
    ndfc.password = "mypassword"
    ndfc.login()

    instance = NdfcEasyFabric()
    instance.ndfc = ndfc
    instance.logger = logger
    instance.fabric_name = 'bang'
    instance.bgp_as = 65011
    instance.replication_mode = 'Ingress'
    instance.create()

    TODO: Need a delete() method
    """

    def __init__(self):
        super().__init__()
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__

        self._init_ndfc_param_to_property_map()

    def _init_properties_default(self):
        """
        Initialize default properties
        """
        self._properties_default = {}
        self._properties_default["deviceType"] = "n9k"
        self._properties_default["fabricTechnology"] = "VXLANFabric"
        self._properties_default["fabricTechnologyFriendly"] = "VXLAN Fabric"
        self._properties_default["fabricType"] = "Switch_Fabric"
        self._properties_default["fabricTypeFriendly"] = "Switch Fabric"
        self._properties_default[
            "networkExtensionTemplate"
        ] = "Default_Network_Extension_Universal"
        value = "Default_Network_Universal"
        self._properties_default["networkTemplate"] = value
        self._properties_default["provisionMode"] = "DCNMTopDown"
        self._properties_default["replicationMode"] = "Multicast"
        self._properties_default["siteId"] = ""
        self._properties_default["templateName"] = "Easy_Fabric"
        self._properties_default[
            "vrfExtensionTemplate"
        ] = "Default_VRF_Extension_Universal"
        self._properties_default["vrfTemplate"] = "Default_VRF_Universal"

    def _init_properties_set(self):
        """
        Initialize a set containing all properties
        """
        self._properties_set = set()
        self._properties_set.add("deviceType")
        self._properties_set.add("fabricTechnology")
        self._properties_set.add("fabricTechnologyFriendly")
        self._properties_set.add("fabricType")
        self._properties_set.add("fabricTypeFriendly")
        self._properties_set.add("networkExtensionTemplate")
        self._properties_set.add("networkTemplate")
        self._properties_set.add("provisionMode")
        self._properties_set.add("replicationMode")
        self._properties_set.add("siteId")
        self._properties_set.add("templateName")
        self._properties_set.add("vrfExtensionTemplate")
        self._properties_set.add("vrfTemplate")
        self._properties_set.add("fabric_name")

    def _init_properties_mandatory_set(self):
        """
        Initialize a set containing mandatory properties
        """
        self._properties_mandatory_set = set()
        self._properties_mandatory_set.add("fabric_name")

    def _init_ndfc_param_to_property_map(self):
        """
        This class standardizes on lowercase dunder property names,
        while NDFC uses both camelCase and upper-case SNAKE_CASE names.
        For messages involving the original NDFC parameter names,
        self._ndfc_param_to_property_map provides a way to map these
        into the property name conventions of this class.

        self._ndfc_param_to_property_map is keyed on NDFC parameter names.
        The value is the name used in this class.
        """
        self._ndfc_param_to_property_map = {}
        for param in self._ndfc_params_set.union(self._nv_pairs_set):
            # convert all dunder params to lowercase
            if "_" in param:
                self._ndfc_param_to_property_map[param] = param.lower()
                continue
            # The regex below does not handle UPPERCASE with no "_"
            # e.g. AAA would become a_a_a, so we special-case it here
            if param.isupper() and "_" not in param:
                self._ndfc_param_to_property_map[param] = param.lower()
                continue
            # convert camel case to dunder
            pattern = r"(?<!^)(?=[A-Z])"
            value = sub(pattern, "_", param).lower()
            self._ndfc_param_to_property_map[param] = value
        # for key,value in sorted(self._ndfc_param_to_property_map.items()):
        #     print("{:<40} {:<40}".format(key,value))

    def _init_ndfc_params_default(self):
        """
        Initialize default NDFC top-level parameters
        See also: _init_nv_pairs*
        """
        self._ndfc_params_default = {}
        self._ndfc_params_default["deviceType"] = "n9k"
        self._ndfc_params_default["fabricTechnology"] = "VXLANFabric"
        self._ndfc_params_default["fabricTechnologyFriendly"] = "VXLAN Fabric"
        self._ndfc_params_default["fabricType"] = "Switch_Fabric"
        self._ndfc_params_default["fabricTypeFriendly"] = "Switch Fabric"
        self._ndfc_params_default[
            "networkExtensionTemplate"
        ] = "Default_Network_Extension_Universal"
        value = "Default_Network_Universal"
        self._ndfc_params_default["networkTemplate"] = value
        self._ndfc_params_default["provisionMode"] = "DCNMTopDown"
        self._ndfc_params_default["replicationMode"] = "Multicast"
        self._ndfc_params_default["siteId"] = ""
        self._ndfc_params_default["templateName"] = "Easy_Fabric"
        self._ndfc_params_default[
            "vrfExtensionTemplate"
        ] = "Default_VRF_Extension_Universal"
        self._ndfc_params_default["vrfTemplate"] = "Default_VRF_Universal"

    def _init_ndfc_params(self):
        """
        This is used to build the payload in self.create()
        and also verified in self._final_verification()
        """
        self._ndfc_params = self._ndfc_params_default
        for item in self._ndfc_params_mandatory_set:
            self._ndfc_params[item] = ""

    def _init_ndfc_params_set(self):
        """
        Initialize a set containing all NDFC parameters
        """
        self._ndfc_params_set = set()
        self._ndfc_params_set.add("asn")
        self._ndfc_params_set.add("deviceType")
        self._ndfc_params_set.add("fabricName")
        self._ndfc_params_set.add("fabricTechnology")
        self._ndfc_params_set.add("fabricTechnologyFriendly")
        self._ndfc_params_set.add("fabricType")
        self._ndfc_params_set.add("fabricTypeFriendly")
        self._ndfc_params_set.add("networkExtensionTemplate")
        self._ndfc_params_set.add("networkTemplate")
        self._ndfc_params_set.add("provisionMode")
        self._ndfc_params_set.add("replicationMode")
        self._ndfc_params_set.add("siteId")
        self._ndfc_params_set.add("templateName")
        self._ndfc_params_set.add("vrfExtensionTemplate")
        self._ndfc_params_set.add("vrfTemplate")

    def _init_ndfc_params_mandatory_set(self):
        """
        Initialize a set containing mandatory NDFC parameters
        """
        self._ndfc_params_mandatory_set = set()
        self._ndfc_params_mandatory_set = self._ndfc_params_set.difference(
            self._ndfc_params_default
        )

    def _init_nv_pairs_default(self):
        """
        Initialize a dictionary containing default values for nvPairs
        These values are derived from the POST request NDFC makes when
        no user modifications (except FABRIC_NAME and BGP_AS) are made to
        the fields presented in the NDFC GUI.

        User-modified nvPairs (in this case FABRIC_NAME and BGP_AS) are
        omitted.
        """
        self._nv_pairs_default = {}
        self._nv_pairs_default["AAA_REMOTE_IP_ENABLED"] = False
        self._nv_pairs_default["AAA_SERVER_CONF"] = ""
        self._nv_pairs_default["ACTIVE_MIGRATION"] = False
        self._nv_pairs_default["ADVERTISE_PIP_BGP"] = False
        self._nv_pairs_default["AGENT_INTF"] = "eth0"
        self._nv_pairs_default["ANYCAST_BGW_ADVERTISE_PIP"] = False
        self._nv_pairs_default["ANYCAST_GW_MAC"] = "2020.0000.00aa"
        self._nv_pairs_default["ANYCAST_LB_ID"] = ""
        self._nv_pairs_default["ANYCAST_RP_IP_RANGE"] = "10.254.254.0/24"
        self._nv_pairs_default["ANYCAST_RP_IP_RANGE_INTERNAL"] = ""
        self._nv_pairs_default["AUTO_SYMMETRIC_DEFAULT_VRF"] = False
        self._nv_pairs_default["AUTO_SYMMETRIC_VRF_LITE"] = False
        self._nv_pairs_default["AUTO_VRFLITE_IFC_DEFAULT_VRF"] = False
        self._nv_pairs_default["BFD_AUTH_ENABLE"] = False
        self._nv_pairs_default["BFD_AUTH_KEY"] = ""
        self._nv_pairs_default["BFD_AUTH_KEY_ID"] = ""
        self._nv_pairs_default["BFD_ENABLE"] = False
        self._nv_pairs_default["BFD_IBGP_ENABLE"] = False
        self._nv_pairs_default["BFD_ISIS_ENABLE"] = False
        self._nv_pairs_default["BFD_OSPF_ENABLE"] = False
        self._nv_pairs_default["BFD_PIM_ENABLE"] = False
        self._nv_pairs_default["BGP_AS"] = "1"
        self._nv_pairs_default["BGP_AS_PREV"] = ""
        self._nv_pairs_default["BGP_AUTH_ENABLE"] = False
        self._nv_pairs_default["BGP_AUTH_KEY"] = ""
        self._nv_pairs_default["BGP_AUTH_KEY_TYPE"] = ""
        self._nv_pairs_default["BGP_LB_ID"] = "0"
        self._nv_pairs_default["BOOTSTRAP_CONF"] = ""
        self._nv_pairs_default["BOOTSTRAP_ENABLE"] = False
        self._nv_pairs_default["BOOTSTRAP_ENABLE_PREV"] = False
        self._nv_pairs_default["BOOTSTRAP_MULTISUBNET"] = ""
        self._nv_pairs_default["BOOTSTRAP_MULTISUBNET_INTERNAL"] = ""
        self._nv_pairs_default["BRFIELD_DEBUG_FLAG"] = "Disable"
        self._nv_pairs_default[
            "BROWNFIELD_NETWORK_NAME_FORMAT"
        ] = "Auto_Net_VNI$$VNI$$_VLAN$$VLAN_ID$$"
        key = "BROWNFIELD_SKIP_OVERLAY_NETWORK_ATTACHMENTS"
        self._nv_pairs_default[key] = False
        self._nv_pairs_default["CDP_ENABLE"] = False
        self._nv_pairs_default["COPP_POLICY"] = "strict"
        self._nv_pairs_default["DCI_SUBNET_RANGE"] = "10.33.0.0/16"
        self._nv_pairs_default["DCI_SUBNET_TARGET_MASK"] = "30"
        self._nv_pairs_default["DEAFULT_QUEUING_POLICY_CLOUDSCALE"] = ""
        self._nv_pairs_default["DEAFULT_QUEUING_POLICY_OTHER"] = ""
        self._nv_pairs_default["DEAFULT_QUEUING_POLICY_R_SERIES"] = ""
        self._nv_pairs_default["DEFAULT_VRF_REDIS_BGP_RMAP"] = ""
        self._nv_pairs_default["DEPLOYMENT_FREEZE"] = False
        self._nv_pairs_default["DHCP_ENABLE"] = False
        self._nv_pairs_default["DHCP_END"] = ""
        self._nv_pairs_default["DHCP_END_INTERNAL"] = ""
        self._nv_pairs_default["DHCP_IPV6_ENABLE"] = ""
        self._nv_pairs_default["DHCP_IPV6_ENABLE_INTERNAL"] = ""
        self._nv_pairs_default["DHCP_START"] = ""
        self._nv_pairs_default["DHCP_START_INTERNAL"] = ""
        self._nv_pairs_default["DNS_SERVER_IP_LIST"] = ""
        self._nv_pairs_default["DNS_SERVER_VRF"] = ""
        self._nv_pairs_default["ENABLE_AAA"] = False
        self._nv_pairs_default["ENABLE_AGENT"] = False
        self._nv_pairs_default["ENABLE_DEFAULT_QUEUING_POLICY"] = False
        self._nv_pairs_default["ENABLE_EVPN"] = True
        self._nv_pairs_default["ENABLE_FABRIC_VPC_DOMAIN_ID"] = False
        self._nv_pairs_default["ENABLE_FABRIC_VPC_DOMAIN_ID_PREV"] = ""
        self._nv_pairs_default["ENABLE_MACSEC"] = False
        self._nv_pairs_default["ENABLE_NETFLOW"] = False
        self._nv_pairs_default["ENABLE_NETFLOW_PREV"] = ""
        self._nv_pairs_default["ENABLE_NGOAM"] = True
        self._nv_pairs_default["ENABLE_NXAPI"] = True
        self._nv_pairs_default["ENABLE_NXAPI_HTTP"] = True
        self._nv_pairs_default["ENABLE_PBR"] = False
        self._nv_pairs_default["ENABLE_PVLAN"] = False
        self._nv_pairs_default["ENABLE_PVLAN_PREV"] = ""
        self._nv_pairs_default["ENABLE_TENANT_DHCP"] = True
        self._nv_pairs_default["ENABLE_TRM"] = False
        self._nv_pairs_default["ENABLE_VPC_PEER_LINK_NATIVE_VLAN"] = False
        self._nv_pairs_default["EXTRA_CONF_INTRA_LINKS"] = ""
        self._nv_pairs_default["EXTRA_CONF_LEAF"] = ""
        self._nv_pairs_default["EXTRA_CONF_SPINE"] = ""
        self._nv_pairs_default["EXTRA_CONF_TOR"] = ""
        self._nv_pairs_default["FABRIC_INTERFACE_TYPE"] = "p2p"
        self._nv_pairs_default["FABRIC_MTU"] = "9216"
        self._nv_pairs_default["FABRIC_MTU_PREV"] = "9216"
        self._nv_pairs_default["FABRIC_NAME"] = "easy-fabric"
        self._nv_pairs_default["FABRIC_TYPE"] = "Switch_Fabric"
        self._nv_pairs_default["FABRIC_VPC_DOMAIN_ID"] = ""
        self._nv_pairs_default["FABRIC_VPC_DOMAIN_ID_PREV"] = ""
        self._nv_pairs_default["FABRIC_VPC_QOS"] = False
        self._nv_pairs_default["FABRIC_VPC_QOS_POLICY_NAME"] = ""
        self._nv_pairs_default["FEATURE_PTP"] = False
        self._nv_pairs_default["FEATURE_PTP_INTERNAL"] = False
        self._nv_pairs_default["FF"] = "Easy_Fabric"
        self._nv_pairs_default["GRFIELD_DEBUG_FLAG"] = "Disable"
        self._nv_pairs_default["HD_TIME"] = "180"
        self._nv_pairs_default["HOST_INTF_ADMIN_STATE"] = True
        self._nv_pairs_default["IBGP_PEER_TEMPLATE"] = ""
        self._nv_pairs_default["IBGP_PEER_TEMPLATE_LEAF"] = ""
        self._nv_pairs_default["INBAND_DHCP_SERVERS"] = ""
        self._nv_pairs_default["INBAND_MGMT"] = False
        self._nv_pairs_default["INBAND_MGMT_PREV"] = False
        self._nv_pairs_default["ISIS_AUTH_ENABLE"] = False
        self._nv_pairs_default["ISIS_AUTH_KEY"] = ""
        self._nv_pairs_default["ISIS_AUTH_KEYCHAIN_KEY_ID"] = ""
        self._nv_pairs_default["ISIS_AUTH_KEYCHAIN_NAME"] = ""
        self._nv_pairs_default["ISIS_LEVEL"] = ""
        self._nv_pairs_default["ISIS_OVERLOAD_ELAPSE_TIME"] = ""
        self._nv_pairs_default["ISIS_OVERLOAD_ENABLE"] = False
        self._nv_pairs_default["ISIS_P2P_ENABLE"] = False
        self._nv_pairs_default["L2_HOST_INTF_MTU"] = "9216"
        self._nv_pairs_default["L2_HOST_INTF_MTU_PREV"] = "9216"
        self._nv_pairs_default["L2_SEGMENT_ID_RANGE"] = "30000-49000"
        self._nv_pairs_default["L3VNI_MCAST_GROUP"] = ""
        self._nv_pairs_default["L3_PARTITION_ID_RANGE"] = "50000-59000"
        self._nv_pairs_default["LINK_STATE_ROUTING"] = "ospf"
        self._nv_pairs_default["LINK_STATE_ROUTING_TAG"] = "UNDERLAY"
        self._nv_pairs_default["LINK_STATE_ROUTING_TAG_PREV"] = ""
        self._nv_pairs_default["LOOPBACK0_IPV6_RANGE"] = ""
        self._nv_pairs_default["LOOPBACK0_IP_RANGE"] = "10.2.0.0/22"
        self._nv_pairs_default["LOOPBACK1_IPV6_RANGE"] = ""
        self._nv_pairs_default["LOOPBACK1_IP_RANGE"] = "10.3.0.0/22"
        self._nv_pairs_default["MACSEC_ALGORITHM"] = ""
        self._nv_pairs_default["MACSEC_CIPHER_SUITE"] = ""
        self._nv_pairs_default["MACSEC_FALLBACK_ALGORITHM"] = ""
        self._nv_pairs_default["MACSEC_FALLBACK_KEY_STRING"] = ""
        self._nv_pairs_default["MACSEC_KEY_STRING"] = ""
        self._nv_pairs_default["MACSEC_REPORT_TIMER"] = ""
        self._nv_pairs_default["MGMT_GW"] = ""
        self._nv_pairs_default["MGMT_GW_INTERNAL"] = ""
        self._nv_pairs_default["MGMT_PREFIX"] = ""
        self._nv_pairs_default["MGMT_PREFIX_INTERNAL"] = ""
        self._nv_pairs_default["MGMT_V6PREFIX"] = "64"
        self._nv_pairs_default["MGMT_V6PREFIX_INTERNAL"] = ""
        self._nv_pairs_default["MPLS_HANDOFF"] = False
        self._nv_pairs_default["MPLS_LB_ID"] = ""
        self._nv_pairs_default["MPLS_LOOPBACK_IP_RANGE"] = ""
        self._nv_pairs_default["MSO_CONNECTIVITY_DEPLOYED"] = ""
        self._nv_pairs_default["MSO_CONTROLER_ID"] = ""
        self._nv_pairs_default["MSO_SITE_GROUP_NAME"] = ""
        self._nv_pairs_default["MSO_SITE_ID"] = ""
        self._nv_pairs_default["MST_INSTANCE_RANGE"] = ""
        self._nv_pairs_default["MULTICAST_GROUP_SUBNET"] = "239.1.1.0/25"
        self._nv_pairs_default["NETFLOW_EXPORTER_LIST"] = ""
        self._nv_pairs_default["NETFLOW_MONITOR_LIST"] = ""
        self._nv_pairs_default["NETFLOW_RECORD_LIST"] = ""
        self._nv_pairs_default["NETWORK_VLAN_RANGE"] = "2300-2999"
        self._nv_pairs_default["NTP_SERVER_IP_LIST"] = ""
        self._nv_pairs_default["NTP_SERVER_VRF"] = ""
        self._nv_pairs_default["NVE_LB_ID"] = "1"
        self._nv_pairs_default["OSPF_AREA_ID"] = "0.0.0.0"
        self._nv_pairs_default["OSPF_AUTH_ENABLE"] = False
        self._nv_pairs_default["OSPF_AUTH_KEY"] = ""
        self._nv_pairs_default["OSPF_AUTH_KEY_ID"] = ""
        self._nv_pairs_default["OVERLAY_MODE"] = "config-profile"
        self._nv_pairs_default["OVERLAY_MODE_PREV"] = ""
        self._nv_pairs_default["PHANTOM_RP_LB_ID1"] = ""
        self._nv_pairs_default["PHANTOM_RP_LB_ID2"] = ""
        self._nv_pairs_default["PHANTOM_RP_LB_ID3"] = ""
        self._nv_pairs_default["PHANTOM_RP_LB_ID4"] = ""
        self._nv_pairs_default["PIM_HELLO_AUTH_ENABLE"] = False
        self._nv_pairs_default["PIM_HELLO_AUTH_KEY"] = ""
        self._nv_pairs_default["PM_ENABLE"] = False
        self._nv_pairs_default["PM_ENABLE_PREV"] = False
        self._nv_pairs_default["POWER_REDUNDANCY_MODE"] = "ps-redundant"
        self._nv_pairs_default["PREMSO_PARENT_FABRIC"] = ""
        self._nv_pairs_default["PTP_DOMAIN_ID"] = ""
        self._nv_pairs_default["PTP_LB_ID"] = ""
        self._nv_pairs_default["REPLICATION_MODE"] = "Multicast"
        self._nv_pairs_default["ROUTER_ID_RANGE"] = ""
        self._nv_pairs_default["ROUTE_MAP_SEQUENCE_NUMBER_RANGE"] = "1-65534"
        self._nv_pairs_default["RP_COUNT"] = "2"
        self._nv_pairs_default["RP_LB_ID"] = "254"
        self._nv_pairs_default["RP_MODE"] = "asm"
        self._nv_pairs_default["RR_COUNT"] = "2"
        self._nv_pairs_default["SEED_SWITCH_CORE_INTERFACES"] = ""
        self._nv_pairs_default["SERVICE_NETWORK_VLAN_RANGE"] = "3000-3199"
        self._nv_pairs_default["SITE_ID"] = ""
        self._nv_pairs_default["SNMP_SERVER_HOST_TRAP"] = True
        self._nv_pairs_default["SPINE_COUNT"] = "0"
        self._nv_pairs_default["SPINE_SWITCH_CORE_INTERFACES"] = ""
        self._nv_pairs_default["SSPINE_ADD_DEL_DEBUG_FLAG"] = "Disable"
        self._nv_pairs_default["SSPINE_COUNT"] = "0"
        self._nv_pairs_default["STATIC_UNDERLAY_IP_ALLOC"] = False
        self._nv_pairs_default["STP_BRIDGE_PRIORITY"] = ""
        self._nv_pairs_default["STP_ROOT_OPTION"] = "unmanaged"
        self._nv_pairs_default["STP_VLAN_RANGE"] = ""
        self._nv_pairs_default["STRICT_CC_MODE"] = False
        self._nv_pairs_default["SUBINTERFACE_RANGE"] = "2-511"
        self._nv_pairs_default["SUBNET_RANGE"] = "10.4.0.0/16"
        self._nv_pairs_default["SUBNET_TARGET_MASK"] = "30"
        self._nv_pairs_default["SYSLOG_SERVER_IP_LIST"] = ""
        self._nv_pairs_default["SYSLOG_SERVER_VRF"] = ""
        self._nv_pairs_default["SYSLOG_SEV"] = ""
        self._nv_pairs_default["TCAM_ALLOCATION"] = True
        self._nv_pairs_default["UNDERLAY_IS_V6"] = False
        self._nv_pairs_default["UNNUM_BOOTSTRAP_LB_ID"] = ""
        self._nv_pairs_default["UNNUM_DHCP_END"] = ""
        self._nv_pairs_default["UNNUM_DHCP_END_INTERNAL"] = ""
        self._nv_pairs_default["UNNUM_DHCP_START"] = ""
        self._nv_pairs_default["UNNUM_DHCP_START_INTERNAL"] = ""
        self._nv_pairs_default["USE_LINK_LOCAL"] = False
        self._nv_pairs_default["V6_SUBNET_RANGE"] = ""
        self._nv_pairs_default["V6_SUBNET_TARGET_MASK"] = ""
        self._nv_pairs_default["VPC_AUTO_RECOVERY_TIME"] = "360"
        self._nv_pairs_default["VPC_DELAY_RESTORE"] = "150"
        self._nv_pairs_default["VPC_DELAY_RESTORE_TIME"] = "60"
        self._nv_pairs_default["VPC_DOMAIN_ID_RANGE"] = "1-1000"
        self._nv_pairs_default["VPC_ENABLE_IPv6_ND_SYNC"] = True
        self._nv_pairs_default["VPC_PEER_KEEP_ALIVE_OPTION"] = "management"
        self._nv_pairs_default["VPC_PEER_LINK_PO"] = "500"
        self._nv_pairs_default["VPC_PEER_LINK_VLAN"] = "3600"
        self._nv_pairs_default["VRF_LITE_AUTOCONFIG"] = "Manual"
        self._nv_pairs_default["VRF_VLAN_RANGE"] = "2000-2299"
        self._nv_pairs_default["abstract_anycast_rp"] = "anycast_rp"
        self._nv_pairs_default["abstract_bgp"] = "base_bgp"
        value = "evpn_bgp_rr_neighbor"
        self._nv_pairs_default["abstract_bgp_neighbor"] = value
        self._nv_pairs_default["abstract_bgp_rr"] = "evpn_bgp_rr"
        self._nv_pairs_default["abstract_dhcp"] = "base_dhcp"
        self._nv_pairs_default[
            "abstract_extra_config_bootstrap"
        ] = "extra_config_bootstrap_11_1"
        value = "extra_config_leaf"
        self._nv_pairs_default["abstract_extra_config_leaf"] = value
        value = "extra_config_spine"
        self._nv_pairs_default["abstract_extra_config_spine"] = value
        value = "extra_config_tor"
        self._nv_pairs_default["abstract_extra_config_tor"] = value
        value = "base_feature_leaf_upg"
        self._nv_pairs_default["abstract_feature_leaf"] = value
        value = "base_feature_spine_upg"
        self._nv_pairs_default["abstract_feature_spine"] = value
        self._nv_pairs_default["abstract_isis"] = "base_isis_level2"
        self._nv_pairs_default["abstract_isis_interface"] = "isis_interface"
        self._nv_pairs_default[
            "abstract_loopback_interface"
        ] = "int_fabric_loopback_11_1"
        self._nv_pairs_default["abstract_multicast"] = "base_multicast_11_1"
        self._nv_pairs_default["abstract_ospf"] = "base_ospf"
        value = "ospf_interface_11_1"
        self._nv_pairs_default["abstract_ospf_interface"] = value
        self._nv_pairs_default["abstract_pim_interface"] = "pim_interface"
        self._nv_pairs_default["abstract_route_map"] = "route_map"
        self._nv_pairs_default["abstract_routed_host"] = "int_routed_host"
        self._nv_pairs_default["abstract_trunk_host"] = "int_trunk_host"
        value = "int_fabric_vlan_11_1"
        self._nv_pairs_default["abstract_vlan_interface"] = value
        self._nv_pairs_default["abstract_vpc_domain"] = "base_vpc_domain_11_1"
        value = "Default_Network_Universal"
        self._nv_pairs_default["default_network"] = value
        self._nv_pairs_default["default_pvlan_sec_network"] = ""
        self._nv_pairs_default["default_vrf"] = "Default_VRF_Universal"
        self._nv_pairs_default["enableRealTimeBackup"] = ""
        self._nv_pairs_default["enableScheduledBackup"] = ""
        self._nv_pairs_default[
            "network_extension_template"
        ] = "Default_Network_Extension_Universal"
        self._nv_pairs_default["scheduledTime"] = ""
        self._nv_pairs_default["temp_anycast_gateway"] = "anycast_gateway"
        self._nv_pairs_default["temp_vpc_domain_mgmt"] = "vpc_domain_mgmt"
        self._nv_pairs_default["temp_vpc_peer_link"] = "int_vpc_peer_link_po"
        self._nv_pairs_default[
            "vrf_extension_template"
        ] = "Default_VRF_Extension_Universal"

    def _init_nv_pairs_set(self):
        """
        Initialize a set containing all nvPairs
        These values are derived from the POST request NDFC makes when
        no user modifications (except FABRIC_NAME and BGP_AS) are made to
        the fields presented in the NDFC GUI.

        User-modified nvPairs (in this case FABRIC_NAME and BGP_AS) are
        included.
        """
        self._nv_pairs_set = set()
        self._nv_pairs_set.add("AAA_REMOTE_IP_ENABLED")
        self._nv_pairs_set.add("AAA_SERVER_CONF")
        self._nv_pairs_set.add("ACTIVE_MIGRATION")
        self._nv_pairs_set.add("ADVERTISE_PIP_BGP")
        self._nv_pairs_set.add("AGENT_INTF")
        self._nv_pairs_set.add("ANYCAST_BGW_ADVERTISE_PIP")
        self._nv_pairs_set.add("ANYCAST_GW_MAC")
        self._nv_pairs_set.add("ANYCAST_LB_ID")
        self._nv_pairs_set.add("ANYCAST_RP_IP_RANGE")
        self._nv_pairs_set.add("ANYCAST_RP_IP_RANGE_INTERNAL")
        self._nv_pairs_set.add("AUTO_SYMMETRIC_DEFAULT_VRF")
        self._nv_pairs_set.add("AUTO_SYMMETRIC_VRF_LITE")
        self._nv_pairs_set.add("AUTO_VRFLITE_IFC_DEFAULT_VRF")
        self._nv_pairs_set.add("BFD_AUTH_ENABLE")
        self._nv_pairs_set.add("BFD_AUTH_KEY")
        self._nv_pairs_set.add("BFD_AUTH_KEY_ID")
        self._nv_pairs_set.add("BFD_ENABLE")
        self._nv_pairs_set.add("BFD_IBGP_ENABLE")
        self._nv_pairs_set.add("BFD_ISIS_ENABLE")
        self._nv_pairs_set.add("BFD_OSPF_ENABLE")
        self._nv_pairs_set.add("BFD_PIM_ENABLE")
        self._nv_pairs_set.add("BGP_AS")
        self._nv_pairs_set.add("BGP_AS_PREV")
        self._nv_pairs_set.add("BGP_AUTH_ENABLE")
        self._nv_pairs_set.add("BGP_AUTH_KEY")
        self._nv_pairs_set.add("BGP_AUTH_KEY_TYPE")
        self._nv_pairs_set.add("BGP_LB_ID")
        self._nv_pairs_set.add("BOOTSTRAP_CONF")
        self._nv_pairs_set.add("BOOTSTRAP_ENABLE")
        self._nv_pairs_set.add("BOOTSTRAP_ENABLE_PREV")
        self._nv_pairs_set.add("BOOTSTRAP_MULTISUBNET")
        self._nv_pairs_set.add("BOOTSTRAP_MULTISUBNET_INTERNAL")
        self._nv_pairs_set.add("BRFIELD_DEBUG_FLAG")
        self._nv_pairs_set.add("BROWNFIELD_NETWORK_NAME_FORMAT")
        self._nv_pairs_set.add("BROWNFIELD_SKIP_OVERLAY_NETWORK_ATTACHMENTS")
        self._nv_pairs_set.add("CDP_ENABLE")
        self._nv_pairs_set.add("COPP_POLICY")
        self._nv_pairs_set.add("DCI_SUBNET_RANGE")
        self._nv_pairs_set.add("DCI_SUBNET_TARGET_MASK")
        self._nv_pairs_set.add("DEAFULT_QUEUING_POLICY_CLOUDSCALE")
        self._nv_pairs_set.add("DEAFULT_QUEUING_POLICY_OTHER")
        self._nv_pairs_set.add("DEAFULT_QUEUING_POLICY_R_SERIES")
        self._nv_pairs_set.add("DEFAULT_VRF_REDIS_BGP_RMAP")
        self._nv_pairs_set.add("DEPLOYMENT_FREEZE")
        self._nv_pairs_set.add("DHCP_ENABLE")
        self._nv_pairs_set.add("DHCP_END")
        self._nv_pairs_set.add("DHCP_END_INTERNAL")
        self._nv_pairs_set.add("DHCP_IPV6_ENABLE")
        self._nv_pairs_set.add("DHCP_IPV6_ENABLE_INTERNAL")
        self._nv_pairs_set.add("DHCP_START")
        self._nv_pairs_set.add("DHCP_START_INTERNAL")
        self._nv_pairs_set.add("DNS_SERVER_IP_LIST")
        self._nv_pairs_set.add("DNS_SERVER_VRF")
        self._nv_pairs_set.add("ENABLE_AAA")
        self._nv_pairs_set.add("ENABLE_AGENT")
        self._nv_pairs_set.add("ENABLE_DEFAULT_QUEUING_POLICY")
        self._nv_pairs_set.add("ENABLE_EVPN")
        self._nv_pairs_set.add("ENABLE_FABRIC_VPC_DOMAIN_ID")
        self._nv_pairs_set.add("ENABLE_FABRIC_VPC_DOMAIN_ID_PREV")
        self._nv_pairs_set.add("ENABLE_MACSEC")
        self._nv_pairs_set.add("ENABLE_NETFLOW")
        self._nv_pairs_set.add("ENABLE_NETFLOW_PREV")
        self._nv_pairs_set.add("ENABLE_NGOAM")
        self._nv_pairs_set.add("ENABLE_NXAPI")
        self._nv_pairs_set.add("ENABLE_NXAPI_HTTP")
        self._nv_pairs_set.add("ENABLE_PBR")
        self._nv_pairs_set.add("ENABLE_PVLAN")
        self._nv_pairs_set.add("ENABLE_PVLAN_PREV")
        self._nv_pairs_set.add("ENABLE_TENANT_DHCP")
        self._nv_pairs_set.add("ENABLE_TRM")
        self._nv_pairs_set.add("ENABLE_VPC_PEER_LINK_NATIVE_VLAN")
        self._nv_pairs_set.add("EXTRA_CONF_INTRA_LINKS")
        self._nv_pairs_set.add("EXTRA_CONF_LEAF")
        self._nv_pairs_set.add("EXTRA_CONF_SPINE")
        self._nv_pairs_set.add("EXTRA_CONF_TOR")
        self._nv_pairs_set.add("FABRIC_INTERFACE_TYPE")
        self._nv_pairs_set.add("FABRIC_MTU")
        self._nv_pairs_set.add("FABRIC_MTU_PREV")
        self._nv_pairs_set.add("FABRIC_NAME")
        self._nv_pairs_set.add("FABRIC_TYPE")
        self._nv_pairs_set.add("FABRIC_VPC_DOMAIN_ID")
        self._nv_pairs_set.add("FABRIC_VPC_DOMAIN_ID_PREV")
        self._nv_pairs_set.add("FABRIC_VPC_QOS")
        self._nv_pairs_set.add("FABRIC_VPC_QOS_POLICY_NAME")
        self._nv_pairs_set.add("FEATURE_PTP")
        self._nv_pairs_set.add("FEATURE_PTP_INTERNAL")
        self._nv_pairs_set.add("FF")
        self._nv_pairs_set.add("GRFIELD_DEBUG_FLAG")
        self._nv_pairs_set.add("HD_TIME")
        self._nv_pairs_set.add("HOST_INTF_ADMIN_STATE")
        self._nv_pairs_set.add("IBGP_PEER_TEMPLATE")
        self._nv_pairs_set.add("IBGP_PEER_TEMPLATE_LEAF")
        self._nv_pairs_set.add("INBAND_DHCP_SERVERS")
        self._nv_pairs_set.add("INBAND_MGMT")
        self._nv_pairs_set.add("INBAND_MGMT_PREV")
        self._nv_pairs_set.add("ISIS_AUTH_ENABLE")
        self._nv_pairs_set.add("ISIS_AUTH_KEY")
        self._nv_pairs_set.add("ISIS_AUTH_KEYCHAIN_KEY_ID")
        self._nv_pairs_set.add("ISIS_AUTH_KEYCHAIN_NAME")
        self._nv_pairs_set.add("ISIS_LEVEL")
        self._nv_pairs_set.add("ISIS_OVERLOAD_ELAPSE_TIME")
        self._nv_pairs_set.add("ISIS_OVERLOAD_ENABLE")
        self._nv_pairs_set.add("ISIS_P2P_ENABLE")
        self._nv_pairs_set.add("L2_HOST_INTF_MTU")
        self._nv_pairs_set.add("L2_HOST_INTF_MTU_PREV")
        self._nv_pairs_set.add("L2_SEGMENT_ID_RANGE")
        self._nv_pairs_set.add("L3VNI_MCAST_GROUP")
        self._nv_pairs_set.add("L3_PARTITION_ID_RANGE")
        self._nv_pairs_set.add("LINK_STATE_ROUTING")
        self._nv_pairs_set.add("LINK_STATE_ROUTING_TAG")
        self._nv_pairs_set.add("LINK_STATE_ROUTING_TAG_PREV")
        self._nv_pairs_set.add("LOOPBACK0_IPV6_RANGE")
        self._nv_pairs_set.add("LOOPBACK0_IP_RANGE")
        self._nv_pairs_set.add("LOOPBACK1_IPV6_RANGE")
        self._nv_pairs_set.add("LOOPBACK1_IP_RANGE")
        self._nv_pairs_set.add("MACSEC_ALGORITHM")
        self._nv_pairs_set.add("MACSEC_CIPHER_SUITE")
        self._nv_pairs_set.add("MACSEC_FALLBACK_ALGORITHM")
        self._nv_pairs_set.add("MACSEC_FALLBACK_KEY_STRING")
        self._nv_pairs_set.add("MACSEC_KEY_STRING")
        self._nv_pairs_set.add("MACSEC_REPORT_TIMER")
        self._nv_pairs_set.add("MGMT_GW")
        self._nv_pairs_set.add("MGMT_GW_INTERNAL")
        self._nv_pairs_set.add("MGMT_PREFIX")
        self._nv_pairs_set.add("MGMT_PREFIX_INTERNAL")
        self._nv_pairs_set.add("MGMT_V6PREFIX")
        self._nv_pairs_set.add("MGMT_V6PREFIX_INTERNAL")
        self._nv_pairs_set.add("MPLS_HANDOFF")
        self._nv_pairs_set.add("MPLS_LB_ID")
        self._nv_pairs_set.add("MPLS_LOOPBACK_IP_RANGE")
        self._nv_pairs_set.add("MSO_CONNECTIVITY_DEPLOYED")
        self._nv_pairs_set.add("MSO_CONTROLER_ID")
        self._nv_pairs_set.add("MSO_SITE_GROUP_NAME")
        self._nv_pairs_set.add("MSO_SITE_ID")
        self._nv_pairs_set.add("MST_INSTANCE_RANGE")
        self._nv_pairs_set.add("MULTICAST_GROUP_SUBNET")
        self._nv_pairs_set.add("NETFLOW_EXPORTER_LIST")
        self._nv_pairs_set.add("NETFLOW_MONITOR_LIST")
        self._nv_pairs_set.add("NETFLOW_RECORD_LIST")
        self._nv_pairs_set.add("NETWORK_VLAN_RANGE")
        self._nv_pairs_set.add("NTP_SERVER_IP_LIST")
        self._nv_pairs_set.add("NTP_SERVER_VRF")
        self._nv_pairs_set.add("NVE_LB_ID")
        self._nv_pairs_set.add("OSPF_AREA_ID")
        self._nv_pairs_set.add("OSPF_AUTH_ENABLE")
        self._nv_pairs_set.add("OSPF_AUTH_KEY")
        self._nv_pairs_set.add("OSPF_AUTH_KEY_ID")
        self._nv_pairs_set.add("OVERLAY_MODE")
        self._nv_pairs_set.add("OVERLAY_MODE_PREV")
        self._nv_pairs_set.add("PHANTOM_RP_LB_ID1")
        self._nv_pairs_set.add("PHANTOM_RP_LB_ID2")
        self._nv_pairs_set.add("PHANTOM_RP_LB_ID3")
        self._nv_pairs_set.add("PHANTOM_RP_LB_ID4")
        self._nv_pairs_set.add("PIM_HELLO_AUTH_ENABLE")
        self._nv_pairs_set.add("PIM_HELLO_AUTH_KEY")
        self._nv_pairs_set.add("PM_ENABLE")
        self._nv_pairs_set.add("PM_ENABLE_PREV")
        self._nv_pairs_set.add("POWER_REDUNDANCY_MODE")
        self._nv_pairs_set.add("PREMSO_PARENT_FABRIC")
        self._nv_pairs_set.add("PTP_DOMAIN_ID")
        self._nv_pairs_set.add("PTP_LB_ID")
        self._nv_pairs_set.add("REPLICATION_MODE")
        self._nv_pairs_set.add("ROUTER_ID_RANGE")
        self._nv_pairs_set.add("ROUTE_MAP_SEQUENCE_NUMBER_RANGE")
        self._nv_pairs_set.add("RP_COUNT")
        self._nv_pairs_set.add("RP_LB_ID")
        self._nv_pairs_set.add("RP_MODE")
        self._nv_pairs_set.add("RR_COUNT")
        self._nv_pairs_set.add("SEED_SWITCH_CORE_INTERFACES")
        self._nv_pairs_set.add("SERVICE_NETWORK_VLAN_RANGE")
        self._nv_pairs_set.add("SITE_ID")
        self._nv_pairs_set.add("SNMP_SERVER_HOST_TRAP")
        self._nv_pairs_set.add("SPINE_COUNT")
        self._nv_pairs_set.add("SPINE_SWITCH_CORE_INTERFACES")
        self._nv_pairs_set.add("SSPINE_ADD_DEL_DEBUG_FLAG")
        self._nv_pairs_set.add("SSPINE_COUNT")
        self._nv_pairs_set.add("STATIC_UNDERLAY_IP_ALLOC")
        self._nv_pairs_set.add("STP_BRIDGE_PRIORITY")
        self._nv_pairs_set.add("STP_ROOT_OPTION")
        self._nv_pairs_set.add("STP_VLAN_RANGE")
        self._nv_pairs_set.add("STRICT_CC_MODE")
        self._nv_pairs_set.add("SUBINTERFACE_RANGE")
        self._nv_pairs_set.add("SUBNET_RANGE")
        self._nv_pairs_set.add("SUBNET_TARGET_MASK")
        self._nv_pairs_set.add("SYSLOG_SERVER_IP_LIST")
        self._nv_pairs_set.add("SYSLOG_SERVER_VRF")
        self._nv_pairs_set.add("SYSLOG_SEV")
        self._nv_pairs_set.add("TCAM_ALLOCATION")
        self._nv_pairs_set.add("UNDERLAY_IS_V6")
        self._nv_pairs_set.add("UNNUM_BOOTSTRAP_LB_ID")
        self._nv_pairs_set.add("UNNUM_DHCP_END")
        self._nv_pairs_set.add("UNNUM_DHCP_END_INTERNAL")
        self._nv_pairs_set.add("UNNUM_DHCP_START")
        self._nv_pairs_set.add("UNNUM_DHCP_START_INTERNAL")
        self._nv_pairs_set.add("USE_LINK_LOCAL")
        self._nv_pairs_set.add("V6_SUBNET_RANGE")
        self._nv_pairs_set.add("V6_SUBNET_TARGET_MASK")
        self._nv_pairs_set.add("VPC_AUTO_RECOVERY_TIME")
        self._nv_pairs_set.add("VPC_DELAY_RESTORE")
        self._nv_pairs_set.add("VPC_DELAY_RESTORE_TIME")
        self._nv_pairs_set.add("VPC_DOMAIN_ID_RANGE")
        self._nv_pairs_set.add("VPC_ENABLE_IPv6_ND_SYNC")
        self._nv_pairs_set.add("VPC_PEER_KEEP_ALIVE_OPTION")
        self._nv_pairs_set.add("VPC_PEER_LINK_PO")
        self._nv_pairs_set.add("VPC_PEER_LINK_VLAN")
        self._nv_pairs_set.add("VRF_LITE_AUTOCONFIG")
        self._nv_pairs_set.add("VRF_VLAN_RANGE")
        self._nv_pairs_set.add("abstract_anycast_rp")
        self._nv_pairs_set.add("abstract_bgp")
        self._nv_pairs_set.add("abstract_bgp_neighbor")
        self._nv_pairs_set.add("abstract_bgp_rr")
        self._nv_pairs_set.add("abstract_dhcp")
        self._nv_pairs_set.add("abstract_extra_config_bootstrap")
        self._nv_pairs_set.add("abstract_extra_config_leaf")
        self._nv_pairs_set.add("abstract_extra_config_spine")
        self._nv_pairs_set.add("abstract_extra_config_tor")
        self._nv_pairs_set.add("abstract_feature_leaf")
        self._nv_pairs_set.add("abstract_feature_spine")
        self._nv_pairs_set.add("abstract_isis")
        self._nv_pairs_set.add("abstract_isis_interface")
        self._nv_pairs_set.add("abstract_loopback_interface")
        self._nv_pairs_set.add("abstract_multicast")
        self._nv_pairs_set.add("abstract_ospf")
        self._nv_pairs_set.add("abstract_ospf_interface")
        self._nv_pairs_set.add("abstract_pim_interface")
        self._nv_pairs_set.add("abstract_route_map")
        self._nv_pairs_set.add("abstract_routed_host")
        self._nv_pairs_set.add("abstract_trunk_host")
        self._nv_pairs_set.add("abstract_vlan_interface")
        self._nv_pairs_set.add("abstract_vpc_domain")
        self._nv_pairs_set.add("default_network")
        self._nv_pairs_set.add("default_pvlan_sec_network")
        self._nv_pairs_set.add("default_vrf")
        self._nv_pairs_set.add("enableRealTimeBackup")
        self._nv_pairs_set.add("enableScheduledBackup")
        self._nv_pairs_set.add("network_extension_template")
        self._nv_pairs_set.add("scheduledTime")
        self._nv_pairs_set.add("temp_anycast_gateway")
        self._nv_pairs_set.add("temp_vpc_domain_mgmt")
        self._nv_pairs_set.add("temp_vpc_peer_link")
        self._nv_pairs_set.add("vrf_extension_template")

    def _init_nv_pairs_mandatory_set(self):
        """
        Initialize a set containing mandatory nv pairs

        This is the difference between all nvPairs (_nv_pairs_set) and
        default nvPairs (_nv_pairs_default)
        """
        self._nv_pairs_mandatory_set = set()
        self._nv_pairs_mandatory_set = self._nv_pairs_set.difference(
            self._nv_pairs_default
        )

    def _init_properties(self):
        """
        Initialize all properties
        """
        self._properties = {}
        for param in self._properties_set:
            if param in self._properties_default:
                self._properties[param] = self._properties_default[param]
            else:
                self._properties[param] = ""

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

    def _validate_netflow_exporter_list(self, param):
        """
        Verify the following:
        1. param is a list of dict
        2. mandatory keys are present in every dict
        3. each key's value is appropriate
        """
        try:
            self.validations.verify_list_of_dict(param)
        except ValueError as err:
            msg = "_validate_netflow_exporter_list: exiting. "
            msg += f"expected list of dict. got {param}. "
            msg += f"error detail: {err}"
            self.logger.error(msg)
            sys.exit(1)
        keys = {"EXPORTER_NAME", "IP", "VRF", "SRC_IF_NAME", "UDP_PORT"}
        for item in param:
            args = {}
            args["keys"] = keys
            args["dict"] = item
            try:
                self.validations.verify_keys(args)
            except (KeyError, TypeError) as err:
                msg = f"_validate_netflow_exporter_list: {err}"
                self.logger.error(msg)
                sys.exit(1)

    def _validate_netflow_record_list(self, param):
        """
        Verify the following:
        1. param is a list of dict
        2. mandatory keys are present in every dict
        3. each key's value is appropriate
        """
        try:
            self.validations.verify_list_of_dict(param)
        except ValueError as err:
            msg = "_validate_netflow_record_list: exiting. "
            msg += f"expected list of dict. got {param}. "
            msg += f"error detail: {err}"
            self.logger.error(msg)
            sys.exit(1)
        keys = {"RECORD_NAME", "RECORD_TEMPLATE", "LAYER2_RECORD"}
        for item in param:
            args = {}
            args["keys"] = keys
            args["dict"] = item
            try:
                self.validations.verify_keys(args)
            except (KeyError, TypeError) as err:
                msg = f"_validate_netflow_record_list: {err}"
                self.logger.error(msg)
                sys.exit(1)

    def _translate_netflow_record_list(self, param):
        """
        Perform any conversions that are needed to satisfy NDFC

        Conversions:
        1. Convert LAYER2_RECORD from bool to lowercase str()

        NOTES:
        1.  param has already been validated so it's safe to forge ahead
        2.  LAYER2_RECORD MUST to be lowercase, not title-case, so
            a simple conversion like str(bool) won't work.
        """
        new_param = []
        for item in param:
            new_item = copy.deepcopy(item)
            new_item["LAYER2_RECORD"] = str(new_item["LAYER2_RECORD"]).lower()
            new_param.append(new_item)
        return new_param

    def _validate_netflow_monitor_list(self, param):
        """
        Verify the following:
        1. param is a list of dict
        2. mandatory keys are present in every dict
        3. each key's value is appropriate
        """
        try:
            self.validations.verify_list_of_dict(param)
        except ValueError as err:
            msg = "_validate_netflow_monitor_list: exiting. "
            msg += f"expected list of dict. got {param}. "
            msg += f"error detail: {err}"
            self.logger.error(msg)
            sys.exit(1)
        keys = {"MONITOR_NAME", "RECORD_NAME", "EXPORTER1"}
        for item in param:
            args = {}
            args["keys"] = keys
            args["dict"] = item
            try:
                self.validations.verify_keys(args)
            except (KeyError, TypeError) as err:
                msg = f"_validate_netflow_monitor_list: {err}"
                self.logger.error(msg)
                sys.exit(1)

    def _final_verification(self):
        self._ndfc_verification()

        for param in self._ndfc_params_mandatory_set:
            if self._ndfc_params[param] == "":
                msg = f"exiting. missing mandatory NDFC parameter {param}. "
                msg += "call instance."
                msg += f"{self._ndfc_param_to_property_map[param]} "
                msg += "before calling instance.create()"
                self.logger.error(msg)
                sys.exit(1)
        for param in self._nv_pairs_mandatory_set:
            if self._nv_pairs[param] == "":
                msg = f"exiting. missing mandatory nvPair {param}. "
                msg += f"Call instance.{param.lower()} "
                msg += "before calling instance.post()"
                self.logger.error(msg)
                sys.exit(1)

        # TODO: if isis_auth_enable == True, the following needs to be set
        #        link_state_routing == "is-is"
        # TODO: if link_state_routing == "is-is", the following are mandatory
        #       isis_level
        # TODO: if isis_auth_enable True, the following are mandatory
        #       isis_auth_keychain_name
        #       isis_auth_key
        #       isis_auth_keychain_key_id
        # TODO: if isis_overload_enable == True, the following are mandatory
        #       isis_overload_elapse_time

        # TODO: if is_underlay_v6 == True, the following are mandatory
        #       anycast_lb_id
        #       router_id_range
        #       loopback0_ipv6_range
        #       loopback1_ipv6_range
        #       v6_subnet_range
        #       v6_subnet_target_mask
        # TODO: if netflow_exporter_list is defined
        #       - verify that all other netflow lists are the same length
        # TODO: if netflow_monitor_list is defined
        #       - verify that all other netflow lists are the same length
        # TODO: if netflow_record_list is defined
        #       - verify that all other netflow lists are the same length
        if (
            self.fabric_vpc_domain_id != ""
            and self.enable_fabric_vpc_domain_id is False
        ):
            msg = "exiting. invalid combination. enable_fabric_vpc_domain_id "
            msg += "must be set to True if fabric_vpc_domain_id is set. "
            msg += "Got enable_fabric_vpc_domain_id "
            msg += f"{self.enable_fabric_vpc_domain_id}, fabric_vpc_domain_id "
            msg += f"{self.fabric_vpc_domain_id}"
            self.logger.error(msg)
            sys.exit(1)

        # We should never hit this case, since fabric_vpc_domain_id will throw
        # an error if the user calls it with a non-integer value.
        if (
            not isinstance(self.fabric_vpc_domain_id, int)
            and self.enable_fabric_vpc_domain_id is True
        ):
            msg = "exiting. invalid combination. enable_fabric_vpc_domain_id "
            msg += "must be set to False if fabric_vpc_domain_id is not set. "
            msg += "Got enable_fabric_vpc_domain_id "
            msg += f"{self.enable_fabric_vpc_domain_id}, fabric_vpc_domain_id "
            msg += f"{self.fabric_vpc_domain_id}"
            self.logger.error(msg)
            sys.exit(1)

    def create(self):
        """
        Create a fabric using Easy_Fabric template.
        """
        self._final_verification()
        self._preprocess_properties()

        if self.fabric_exists(self.fabric_name):
            msg = f"exiting. fabric {self.fabric_name} already exists "
            msg += f"on the NDFC at {self.ndfc.url_base}.  Existing "
            msg += f"fabrics: {', '.join(sorted(self.fabric_names))}"
            self.logger.error(msg)
            sys.exit(1)

        url = f"{self.ndfc.url_control_fabrics}"

        headers = {}
        headers["Authorization"] = self.ndfc.bearer_token
        headers["Content-Type"] = "application/json"

        _ndfc_payload = self._ndfc_params
        _ndfc_payload["nvPairs"] = self._nv_pairs

        try:
            self.ndfc.post(url, headers, _ndfc_payload)
        except NdfcRequestError as err:
            msg = f"error creating fabric {self.fabric_name}, "
            msg += f"error detail {err}"
            self.logger.error(msg)
            sys.exit(1)

    # ------------------------------------------------------------
    # properties that appear in both self._ndfc_params and
    # self._nv_pairs need to be updated in both places
    # ------------------------------------------------------------
    @property
    def bgp_as(self):
        """
        return the current nv_pairs value of fabric_name
        Since we set the NDFC top-level parameter AND the
        nvPair in the setter below, we're just returning
        the nv_pairs value here.
        """
        return self._nv_pairs["BGP_AS"]

    @bgp_as.setter
    def bgp_as(self, param):
        try:
            self.validations.verify_bgp_asn(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._ndfc_params["asn"] = param
        self._nv_pairs["BGP_AS"] = param

    @property
    def default_vrf(self):
        """
        Default Overlay VRF Template For Leafs

        Alias of vrf_template

        Valid values: "Default_VRF_Universal", "VRF_Classic"
        Default value: Default_VRF_Universal

        NDFC GUI label: VRF Template
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["default_vrf"]

    @default_vrf.setter
    def default_vrf(self, param):
        _valid = ["Default_VRF_Universal", "VRF_Classic"]
        if param in _valid:
            self._ndfc_params["vrfTemplate"] = param
            self._nv_pairs["default_vrf"] = param
            return
        msg = f"exiting. expected one of {_valid}, got {param}"
        self.logger.error(msg)

    @property
    def fabric_name(self):
        """
        return the current nv_pairs value of fabric_name
        Since we set the NDFC top-level parameter AND the
        nvPair in the setter below, we're just returning
        the nv_pairs value here.
        """
        return self._nv_pairs["FABRIC_NAME"]

    @fabric_name.setter
    def fabric_name(self, param):
        self._ndfc_params["fabricName"] = param
        self._nv_pairs["FABRIC_NAME"] = param

    @property
    def fabric_type(self):
        """
        return the current nv_pairs value of fabric_name
        Since we set the NDFC top-level parameter AND the
        nvPair in the setter below, we're just returning
        the nv_pairs value here.

        Default: "Switch_Fabric"
        Valid values*: "External", "Switch_Fabric"

        *Caution: The only valid value for Easy_Fabric is "Switch_Fabric"
        It's not recommended to change this value.
        """
        return self._nv_pairs["FABRIC_TYPE"]

    @fabric_type.setter
    def fabric_type(self, param):
        self._ndfc_params["fabricType"] = param
        self._nv_pairs["FABRIC_TYPE"] = param

    @property
    def network_extension_template(self):
        """
        return the current nv_pairs value of network_extension_template
        """
        return self._nv_pairs["network_extension_template"]

    @network_extension_template.setter
    def network_extension_template(self, param):
        self._ndfc_params["networkExtensionTemplate"] = param
        self._nv_pairs["network_extension_template"] = param

    @property
    def network_template(self):
        """
        return the current nv_pairs value of network_template
        """
        return self._nv_pairs["default_network"]

    @network_template.setter
    def network_template(self, param):
        self._ndfc_params["networkTemplate"] = param
        self._nv_pairs["default_network"] = param

    @property
    def replication_mode(self):
        """
        return the current nv_pairs value of replication_mode
        Since we set the NDFC top-level parameter AND the
        nvPair in the setter below, we're just returning
        the nv_pairs value here.

        NDFC GUI label: Replication Mode
        NDFC GUI tab: Replication
        """
        return self._nv_pairs["REPLICATION_MODE"]

    @replication_mode.setter
    def replication_mode(self, param):
        self._ndfc_params["replicationMode"] = param
        self._nv_pairs["REPLICATION_MODE"] = param

    @property
    def vrf_extension_template(self):
        """
        Default Overlay VRF Template For Borders

        Valid values: "Default_VRF_Extension_Universal", "VRF_Classic"
        Default value: Default_VRF_Extension_Universal

        NDFC GUI label: VRF Extension Template
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["vrf_extension_template"]

    @vrf_extension_template.setter
    def vrf_extension_template(self, param):
        _valid = ["Default_VRF_Extension_Universal", "VRF_Classic"]
        if param in _valid:
            self._ndfc_params["vrfExtensionTemplate"] = param
            self._nv_pairs["vrf_extension_template"] = param
            return
        msg = f"exiting. expected one of {_valid}, got {param}"
        self.logger.error(msg)
        sys.exit(1)

    @property
    def vrf_template(self):
        """
        Default Overlay VRF Template For Leafs

        Alias of default_vrf

        Valid values: "Default_VRF_Universal", "VRF_Classic"
        Default value: Default_VRF_Universal

        NDFC GUI label: VRF Template
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["default_vrf"]

    @vrf_template.setter
    def vrf_template(self, param):
        _valid = ["Default_VRF_Universal", "VRF_Classic"]
        if param in _valid:
            self._ndfc_params["vrfTemplate"] = param
            self._nv_pairs["default_vrf"] = param
            return
        msg = f"exiting. expected one of {_valid}, got {param}"
        self.logger.error(msg)

    # ------------------------------------------------------------
    # nvPairs
    # ------------------------------------------------------------
    @property
    def aaa_remote_ip_enabled(self):
        """
        Enable AAA IP Authorization

        Enable only when IP Authorization is enabled on the AAA Server

        NDFC GUI label: Enable AAA IP Authorization
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["AAA_REMOTE_IP_ENABLED"]

    @aaa_remote_ip_enabled.setter
    def aaa_remote_ip_enabled(self, param):
        self.verify_boolean(param, "aaa_remote_ip_enabled")
        self._nv_pairs["AAA_REMOTE_IP_ENABLED"] = param

    @property
    def aaa_server_conf(self):
        """
        AAA Configurations

        NDFC GUI label: AAA Freeform Config
        NDFC GUI tab: Manageability

        Input validation is not performed.
        """
        return self._nv_pairs["AAA_SERVER_CONF"]

    @aaa_server_conf.setter
    def aaa_server_conf(self, param):
        self._nv_pairs["AAA_SERVER_CONF"] = param

    @property
    def active_migration(self):
        """
        return the current nv_pairs value of active_migration
        """
        return self._nv_pairs["ACTIVE_MIGRATION"]

    @active_migration.setter
    def active_migration(self, param):
        self.verify_boolean(param, "active_migration")
        self._nv_pairs["ACTIVE_MIGRATION"] = param

    @property
    def advertise_pip_bgp(self):
        """
        For Primary VTEP IP Advertisement As Next-Hop Of Prefix Routes

        NDFC GUI label: vPC advertise-pip
        NDFC GUI tab: VPC

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ADVERTISE_PIP_BGP"]

    @advertise_pip_bgp.setter
    def advertise_pip_bgp(self, param):
        self.verify_boolean(param, "advertise_pip_bgp")
        self._nv_pairs["ADVERTISE_PIP_BGP"] = param

    @property
    def agent_intf(self):
        """
        return the current nv_pairs value of agent_intf
        """
        return self._nv_pairs["AGENT_INTF"]

    @agent_intf.setter
    def agent_intf(self, param):
        self.verify_boolean(param, "agent_intf")
        self._nv_pairs["AGENT_INTF"] = param

    @property
    def anycast_bgw_advertise_pip(self):
        """
        To advertise Anycast Border Gateway PIP as VTEP.
        Effective on MSD fabric 'Recalculate Config'

        NDFC GUI label: Anycast Border Gateway advertise-pip
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["ANYCAST_BGW_ADVERTISE_PIP"]

    @anycast_bgw_advertise_pip.setter
    def anycast_bgw_advertise_pip(self, param):
        self.verify_boolean(param, "anycast_bgw_advertise_pip")
        self._nv_pairs["ANYCAST_BGW_ADVERTISE_PIP"] = param

    @property
    def anycast_gw_mac(self):
        """
        return the current nv_pairs value of anycast_gw_mac

        NDFC GUI label: Anycast Gateway MAC
        NDFC GUI tab: General Parameters

        Valid values: a dotted notation mac address e.g. 000c.fa1c.04da
        Default value: 2020.0000.00aa
        """
        return self._nv_pairs["ANYCAST_GW_MAC"]

    @anycast_gw_mac.setter
    def anycast_gw_mac(self, param):
        if self.validations.is_mac_address_format_a(param):
            self._nv_pairs["ANYCAST_GW_MAC"] = param
        msg = f"exiting. {param}, anycast_bgw_advertise_pip, "
        msg += "unexpected value. "
        msg += "expected mac address with format xxxx.xxxx.xxxx"
        self.logger.error(msg)
        sys.exit(1)

    @property
    def anycast_lb_id(self):
        """
        Used for vPC Peering in VXLANv6 Fabrics

        Valid values: integer in range 0-1023
        Default value: ""

        NDFC GUI label: Underlay Anycast Loopback Id
        NDFC GUI tab: Protocols

        Mandatory when underlay_is_v6 is set to True
        """
        return self._nv_pairs["ANYCAST_LB_ID"]

    @anycast_lb_id.setter
    def anycast_lb_id(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 1023
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["ANYCAST_LB_ID"] = param

    @property
    def anycast_rp_ip_range(self):
        """
        Anycast or Phantom RP IP Address Range

        Valid value: An ipv4 network with prefix e.g. 10.1.0.0/16
        Default value: 10.254.254.0/24

        NDFC GUI label: Underlay RP Loopback IP Range
        NDFC GUI tab: Resources

        replication_mode must be set to "Multicast"
        """
        return self._nv_pairs["ANYCAST_RP_IP_RANGE"]

    @anycast_rp_ip_range.setter
    def anycast_rp_ip_range(self, param):
        try:
            self.validations.verify_ipv4_address_with_prefix(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["ANYCAST_RP_IP_RANGE"] = param

    @property
    def auto_symmetric_default_vrf(self):
        """
        Enable (True) or disable (False) auto generation of Default
        VRF interface and BGP peering configuration on VRF LITE IFC
        auto deployment. If set, auto created VRF Lite IFC links will
        have 'Auto Deploy Default VRF' enabled.

        NDFC GUI label: Auto Deploy Default VRF
        NDFC GUI tab: Resources

        vrf_lite_autoconfig must be set to Back2Back&ToExternal
        """
        return self._nv_pairs["AUTO_SYMMETRIC_DEFAULT_VRF"]

    @auto_symmetric_default_vrf.setter
    def auto_symmetric_default_vrf(self, param):
        self.verify_boolean(param, "auto_symmetric_default_vrf")
        self._nv_pairs["AUTO_SYMMETRIC_DEFAULT_VRF"] = param

    @property
    def auto_symmetric_vrf_lite(self):
        """
        NDFC GUI label: Auto Deploy for Peer
        NDFC GUI tab: Resources
        """
        return self._nv_pairs["AUTO_SYMMETRIC_VRF_LITE"]

    @auto_symmetric_vrf_lite.setter
    def auto_symmetric_vrf_lite(self, param):
        self.verify_boolean(param, "auto_symmetric_vrf_lite")
        self._nv_pairs["AUTO_SYMMETRIC_VRF_LITE"] = param

    @property
    def auto_vrflite_ifc_default_vrf(self):
        """
        return the current nv_pairs value of auto_vrflite_ifc_default_vrf
        """
        return self._nv_pairs["AUTO_VRFLITE_IFC_DEFAULT_VRF"]

    @auto_vrflite_ifc_default_vrf.setter
    def auto_vrflite_ifc_default_vrf(self, param):
        self.verify_boolean(param, "auto_vrflite_ifc_default_vrf")
        self._nv_pairs["AUTO_VRFLITE_IFC_DEFAULT_VRF"] = param

    @property
    def bfd_auth_enable(self):
        """
        return the current nv_pairs value of bfd_auth_enable
        """
        return self._nv_pairs["BFD_AUTH_ENABLE"]

    @bfd_auth_enable.setter
    def bfd_auth_enable(self, param):
        self.verify_boolean(param, "bfd_auth_enable")
        self._nv_pairs["BFD_AUTH_ENABLE"] = param

    @property
    def bfd_auth_key(self):
        """
        return the current nv_pairs value of bfd_auth_key
        No input validation is done when setting this value.
        """
        return self._nv_pairs["BFD_AUTH_KEY"]

    @bfd_auth_key.setter
    def bfd_auth_key(self, param):
        self._nv_pairs["BFD_AUTH_KEY"] = param

    @property
    def bfd_auth_key_id(self):
        """
        return the current nv_pairs value of bfd_auth_key_id
        No input validation is done when setting this value.
        """
        return self._nv_pairs["BFD_AUTH_KEY_ID"]

    @bfd_auth_key_id.setter
    def bfd_auth_key_id(self, param):
        self._nv_pairs["BFD_AUTH_KEY_ID"] = param

    @property
    def bfd_enable(self):
        """
        return the current nv_pairs value of bfd_enable
        """
        return self._nv_pairs["BFD_ENABLE"]

    @bfd_enable.setter
    def bfd_enable(self, param):
        self.verify_boolean(param, "bfd_enable")
        self._nv_pairs["BFD_ENABLE"] = param

    @property
    def bfd_ibgp_enable(self):
        """
        return the current nv_pairs value of bfd_ibgp_enable
        """
        return self._nv_pairs["BFD_IBGP_ENABLE"]

    @bfd_ibgp_enable.setter
    def bfd_ibgp_enable(self, param):
        self.verify_boolean(param, "bfd_ibgp_enable")
        self._nv_pairs["BFD_IBGP_ENABLE"] = param

    @property
    def bfd_isis_enable(self):
        """
        return the current nv_pairs value of bfd_isis_enable
        """
        return self._nv_pairs["BFD_ISIS_ENABLE"]

    @bfd_isis_enable.setter
    def bfd_isis_enable(self, param):
        self.verify_boolean(param, "bfd_ibgp_enable")
        self._nv_pairs["BFD_ISIS_ENABLE"] = param

    @property
    def bfd_ospf_enable(self):
        """
        return the current nv_pairs value of bfd_ospf_enable
        """
        return self._nv_pairs["BFD_OSPF_ENABLE"]

    @bfd_ospf_enable.setter
    def bfd_ospf_enable(self, param):
        self.verify_boolean(param, "bfd_ibgp_enable")
        self._nv_pairs["BFD_OSPF_ENABLE"] = param

    @property
    def bfd_pim_enable(self):
        """
        return the current nv_pairs value of bfd_pim_enable
        """
        return self._nv_pairs["BFD_PIM_ENABLE"]

    @bfd_pim_enable.setter
    def bfd_pim_enable(self, param):
        self.verify_boolean(param, "bfd_ibgp_enable")
        self._nv_pairs["BFD_PIM_ENABLE"] = param

    # bgp_as See above, under properties that need to populate both nvPairs
    # and NDFC top-level params

    @property
    def bgp_as_prev(self):
        """
        return the current nv_pairs value of bgp_as_prev
        """
        return self._nv_pairs["BGP_AS_PREV"]

    @bgp_as_prev.setter
    def bgp_as_prev(self, param):
        self._nv_pairs["BGP_AS_PREV"] = param

    @property
    def bgp_auth_enable(self):
        """
        return the current nv_pairs value of bgp_auth_enable
        """
        return self._nv_pairs["BGP_AUTH_ENABLE"]

    @bgp_auth_enable.setter
    def bgp_auth_enable(self, param):
        self.verify_boolean(param, "bgp_auth_enable")
        self._nv_pairs["BGP_AUTH_ENABLE"] = param

    @property
    def bgp_auth_key(self):
        """
        return the current nv_pairs value of bgp_auth_key
        Input validation is not performed.
        """
        return self._nv_pairs["BGP_AUTH_KEY"]

    @bgp_auth_key.setter
    def bgp_auth_key(self, param):
        self._nv_pairs["BGP_AUTH_KEY"] = param

    @property
    def bgp_auth_key_type(self):
        """
        return the current nv_pairs value of bgp_auth_key_type
        Valid values: 3, 7
        """
        return self._nv_pairs["BGP_AUTH_KEY_TYPE"]

    @bgp_auth_key_type.setter
    def bgp_auth_key_type(self, param):
        try:
            self.validations.verify_bgp_password_key_type(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["BGP_AUTH_KEY_TYPE"] = param

    @property
    def bgp_lb_id(self):
        """
        return the current nv_pairs value of bgp_lb_id
        Input validation is not performed.
        """
        return self._nv_pairs["BGP_LB_ID"]

    @bgp_lb_id.setter
    def bgp_lb_id(self, param):
        self._nv_pairs["BGP_LB_ID"] = param

    @property
    def bootstrap_conf(self):
        """
        return the current nv_pairs value of bootstrap_conf
        Input validation is not performed.
        """
        return self._nv_pairs["BOOTSTRAP_CONF"]

    @bootstrap_conf.setter
    def bootstrap_conf(self, param):
        self._nv_pairs["BOOTSTRAP_CONF"] = param

    @property
    def bootstrap_enable(self):
        """
        Automatic IP Assignment For POAP

        Valid values: boolean
        Default value: False

        NDFC GUI label: Enable Bootstrap
        NDFC GUI tab: Bootstrap
        """
        return self._nv_pairs["BOOTSTRAP_ENABLE"]

    @bootstrap_enable.setter
    def bootstrap_enable(self, param):
        self.verify_boolean(param, "bootstrap_enable")
        self._nv_pairs["BOOTSTRAP_ENABLE"] = param

    @property
    def bootstrap_enable_prev(self):
        """
        return the current nv_pairs value of bootstrap_enable_prev
        Input validation is not performed.
        """
        return self._nv_pairs["BOOTSTRAP_ENABLE_PREV"]

    @bootstrap_enable_prev.setter
    def bootstrap_enable_prev(self, param):
        self._nv_pairs["BOOTSTRAP_ENABLE_PREV"] = param

    @property
    def bootstrap_multisubnet(self):
        """
        return the current nv_pairs value of bootstrap_multisubnet
        Input validation is not performed.
        """
        return self._nv_pairs["BOOTSTRAP_MULTISUBNET"]

    @bootstrap_multisubnet.setter
    def bootstrap_multisubnet(self, param):
        self._nv_pairs["BOOTSTRAP_MULTISUBNET"] = param

    @property
    def bootstrap_multisubnet_internal(self):
        """
        return the current nv_pairs value of bootstrap_multisubnet_internal
        Input validation is not performed.
        """
        return self._nv_pairs["BOOTSTRAP_MULTISUBNET_INTERNAL"]

    @bootstrap_multisubnet_internal.setter
    def bootstrap_multisubnet_internal(self, param):
        self._nv_pairs["BOOTSTRAP_MULTISUBNET_INTERNAL"] = param

    @property
    def brfield_debug_flag(self):
        """
        return the current nv_pairs value of brfield_debug_flag
        Valid values: "Enable", "Disable"
        Default: "Disable"
        """
        return self._nv_pairs["BRFIELD_DEBUG_FLAG"]

    @brfield_debug_flag.setter
    def brfield_debug_flag(self, param):
        try:
            self.validations.verify_disable_enable(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["BRFIELD_DEBUG_FLAG"] = param

    @property
    def brownfield_network_name_format(self):
        """
        Brownfield Overlay Network Name Format
        Generated network name should be < 64 characters

        NDFC label: Brownfield Overlay Network Name Format
        NDFC tab: Advanced

        Default: Auto_Net_VNI$$VNI$$_VLAN$$VLAN_ID$$
        Input validation is not performed.
        """
        return self._nv_pairs["BROWNFIELD_NETWORK_NAME_FORMAT"]

    @brownfield_network_name_format.setter
    def brownfield_network_name_format(self, param):
        self._nv_pairs["BROWNFIELD_NETWORK_NAME_FORMAT"] = param

    @property
    def brownfield_skip_overlay_network_attachments(self):
        """
        Enable (True) or disable (False) skipping overlay network interface
        attachments for Brownfield and Host Port Resync cases

        NDFC label: Skip Overlay Network Interface Attachments
        NDFC tab: Advanced

        Valid values: Boolean
        Default: False
        """
        return self._nv_pairs["BROWNFIELD_SKIP_OVERLAY_NETWORK_ATTACHMENTS"]

    @brownfield_skip_overlay_network_attachments.setter
    def brownfield_skip_overlay_network_attachments(self, param):
        _name = "brownfield_skip_overlay_network_attachments"
        self.verify_boolean(param, _name)
        self._nv_pairs["BROWNFIELD_SKIP_OVERLAY_NETWORK_ATTACHMENTS"] = param

    @property
    def cdp_enable(self):
        """
        Enable (True) or disable (False) CDP on management interface

        NDFC label: Enable CDP for Bootstrapped Switch
        NDFC tab: Advanced

        Valid values: Boolean
        Default: False
        """
        return self._nv_pairs["CDP_ENABLE"]

    @cdp_enable.setter
    def cdp_enable(self, param):
        self.verify_boolean(param, "cdp_enable")
        self._nv_pairs["CDP_ENABLE"] = param

    @property
    def copp_policy(self):
        """
        Fabric Wide CoPP Policy.
        Customized CoPP policy should be provided when 'manual' is selected.
        Valid values: "dense", "manual", "moderate", "lenient", "strict"
        Default: "strict"
        """
        return self._nv_pairs["COPP_POLICY"]

    @copp_policy.setter
    def copp_policy(self, param):
        valid = ["dense", "manual", "moderate", "lenient", "strict"]
        if param in valid:
            self._nv_pairs["COPP_POLICY"] = param
            return
        msg = f"exiting. copp_policy, expected one of {valid} "
        msg += f"got {param}"
        self.logger.error(msg)
        sys.exit(1)

    @property
    def dci_subnet_range(self):
        """
        return the current nv_pairs value of dci_subnet_range
        """
        return self._nv_pairs["DCI_SUBNET_RANGE"]

    @dci_subnet_range.setter
    def dci_subnet_range(self, param):
        try:
            self.validations.verify_ipv4_address_with_prefix(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["DCI_SUBNET_RANGE"] = param

    @property
    def dci_subnet_target_mask(self):
        """
        return the current nv_pairs value of dci_subnet_target_mask
        Valid values: [30, 31]
        Default: 30
        """
        return self._nv_pairs["DCI_SUBNET_TARGET_MASK"]

    @dci_subnet_target_mask.setter
    def dci_subnet_target_mask(self, param):
        params = {}
        params["value"] = param
        params["min"] = 30
        params["max"] = 31
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["DCI_SUBNET_TARGET_MASK"] = param

    @property
    def default_network(self):
        """
        return the current nv_pairs value of default_network
        """
        return self._nv_pairs["default_network"]

    @default_network.setter
    def default_network(self, param):
        self._nv_pairs["default_network"] = param

    @property
    def default_pvlan_sec_network(self):
        """
        return the current nv_pairs value of default_pvlan_sec_network
        """
        return self._nv_pairs["default_pvlan_sec_network"]

    @default_pvlan_sec_network.setter
    def default_pvlan_sec_network(self, param):
        self._nv_pairs["default_pvlan_sec_network"] = param

    @property
    def default_queuing_policy_cloudscale(self):
        """
        return the current nv_pairs value of default_queuing_policy_cloudscale

        NOTE: The NDFC key for this is misspelled (DEAFULT instead of
        DEFAULT). We're using the proper spelling for the property name, and
        supplying NDFC with its preferred misspelling.

        Default value: ""

        Input validation is not performed.
        """
        return self._nv_pairs["DEAFULT_QUEUING_POLICY_CLOUDSCALE"]

    @default_queuing_policy_cloudscale.setter
    def default_queuing_policy_cloudscale(self, param):
        self._nv_pairs["DEAFULT_QUEUING_POLICY_CLOUDSCALE"] = param

    @property
    def default_queuing_policy_other(self):
        """
        return the current nv_pairs value of default_queuing_policy_other

        NOTE: The NDFC key for this is misspelled (DEAFULT instead of
        DEFAULT). We're using the proper spelling for the property name, and
        supplying NDFC with its preferred misspelling.

        Default value: ""

        Input validation is not performed.
        """
        return self._nv_pairs["DEAFULT_QUEUING_POLICY_OTHER"]

    @default_queuing_policy_other.setter
    def default_queuing_policy_other(self, param):
        self._nv_pairs["DEAFULT_QUEUING_POLICY_OTHER"] = param

    @property
    def default_queuing_policy_r_series(self):
        """
        return the current nv_pairs value of default_queuing_policy_r_series

        NOTE: The NDFC key for this is misspelled (DEAFULT instead of
        DEFAULT). We're using the proper spelling for the property name, and
        supplying NDFC with its preferred misspelling.

        Default value: ""

        Input validation is not performed.
        """
        return self._nv_pairs["DEAFULT_QUEUING_POLICY_R_SERIES"]

    @default_queuing_policy_r_series.setter
    def default_queuing_policy_r_series(self, param):
        self._nv_pairs["DEAFULT_QUEUING_POLICY_R_SERIES"] = param

    # default_vrf (see under TODO: add section name here)

    @property
    def default_vrf_redis_bgp_rmap(self):
        """
        return the current nv_pairs value of default_vrf_redis_bgp_rmap

        NDFC GUI label: Redistribute BGP Route-map Name
        NDFC GUI tab: Resources

        Default value: ""

        Input validation is not performed.
        """
        return self._nv_pairs["DEFAULT_VRF_REDIS_BGP_RMAP"]

    @default_vrf_redis_bgp_rmap.setter
    def default_vrf_redis_bgp_rmap(self, param):
        self._nv_pairs["DEFAULT_VRF_REDIS_BGP_RMAP"] = param

    @property
    def deployment_freeze(self):
        """
        return the current nv_pairs value of deployment_freeze

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["DEPLOYMENT_FREEZE"]

    @deployment_freeze.setter
    def deployment_freeze(self, param):
        self.verify_boolean(param, "deployment_freeze")
        self._nv_pairs["DEPLOYMENT_FREEZE"] = param

    @property
    def dhcp_enable(self):
        """
        Automatic IP Assignment For POAP From NDFC DHCP Server

        Valid values: boolean
        Default value: False

        NDFC GUI label: Enable Local DHCP Server
        NDFC GUI tab: Bootstrap
        """
        return self._nv_pairs["DHCP_ENABLE"]

    @dhcp_enable.setter
    def dhcp_enable(self, param):
        self.verify_boolean(param, "dhcp_enable")
        self._nv_pairs["DHCP_ENABLE"] = param

    @property
    def dhcp_end(self):
        """
        DHCP Scope End Address.
        Mandatory if dhcp_enable is set to True
        Valid values: IP address without prefix, e.g. 10.1.1.3
        Default value: ""
        """
        return self._nv_pairs["DHCP_END"]

    @dhcp_end.setter
    def dhcp_end(self, param):
        try:
            self.validations.verify_ipv4_address(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["DHCP_END"] = param

    @property
    def dhcp_end_internal(self):
        """
        return the current nv_pairs value of dhcp_end_internal

        Input validation is not performed.
        """
        return self._nv_pairs["DHCP_END_INTERNAL"]

    @dhcp_end_internal.setter
    def dhcp_end_internal(self, param):
        self._nv_pairs["DHCP_END_INTERNAL"] = param

    @property
    def dhcp_ipv6_enable(self):
        """
        Sets the DHCP version for IPv4 and IPv6 to DHCPv4

        NDFC GUI label: DHCP Version
        NDFC GUI tab: Bootstrap

        Valid values: "DHCPv4"
        Default value: ""

        bootstrap_enable must be set to True
        dhcp_enable must be set to True

        Other notes:
        1.  Unlike every other *_ENABLE parameter, this is not a boolean.
        2.  We'd have named this "DHCP_VERSION", with property name
            "dhcp_version", but we're sticking with our property name
            convention of using the actual nvPair key name.
        """
        return self._nv_pairs["DHCP_IPV6_ENABLE"]

    @dhcp_ipv6_enable.setter
    def dhcp_ipv6_enable(self, param):
        if param in self.valid["dhcp_ipv6_enable"]:
            self._nv_pairs["DHCP_IPV6_ENABLE"] = param
            return
        msg = "exiting. expected one of "
        msg += f"{self.valid['dhcp_ipv6_enable']}, got {param}"
        self.logger.error(msg)
        sys.exit(1)

    @property
    def dhcp_ipv6_enable_internal(self):
        """
        return the current nv_pairs value of dhcp_ipv6_enable_internal
        """
        return self._nv_pairs["DHCP_IPV6_ENABLE_INTERNAL"]

    @dhcp_ipv6_enable_internal.setter
    def dhcp_ipv6_enable_internal(self, param):
        self._nv_pairs["DHCP_IPV6_ENABLE_INTERNAL"] = param

    @property
    def dhcp_start(self):
        """
        return the current nv_pairs value of dhcp_start
        """
        return self._nv_pairs["DHCP_START"]

    @dhcp_start.setter
    def dhcp_start(self, param):
        try:
            self.validations.verify_ipv4_address(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["DHCP_START"] = param

    @property
    def dhcp_start_internal(self):
        """
        return the current nv_pairs value of dhcp_start_internal
        Input validation is not performed.
        """
        return self._nv_pairs["DHCP_START_INTERNAL"]

    @dhcp_start_internal.setter
    def dhcp_start_internal(self, param):
        self._nv_pairs["DHCP_START_INTERNAL"] = param

    @property
    def dns_server_ip_list(self):
        """
        return the current nv_pairs value of dns_server_ip_list
        Default: ""
        Valid values: Comma separated list of IP Addresses(v4/v6)
        Input validation is not currently performed.
        """
        return self._nv_pairs["DNS_SERVER_IP_LIST"]

    @dns_server_ip_list.setter
    def dns_server_ip_list(self, param):
        self._nv_pairs["DNS_SERVER_IP_LIST"] = param

    @property
    def dns_server_vrf(self):
        """
        return the current nv_pairs value of dns_server_vrf

        Valid values: One VRF for all DNS servers or a comma separated
        list of VRFs, one per DNS server in dns_server_ip_list.  If the
        latter, the number of elements in each list must match.

        Input validation is not currently performed.
        """
        return self._nv_pairs["DNS_SERVER_VRF"]

    @dns_server_vrf.setter
    def dns_server_vrf(self, param):
        self._nv_pairs["DNS_SERVER_VRF"] = param

    @property
    def enable_aaa(self):
        """
        return the current nv_pairs value of enable_aaa

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ENABLE_AAA"]

    @enable_aaa.setter
    def enable_aaa(self, param):
        self.verify_boolean(param, "enable_aaa")
        self._nv_pairs["ENABLE_AAA"] = param

    @property
    def enable_agent(self):
        """
        return the current nv_pairs value of enable_agent

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ENABLE_AGENT"]

    @enable_agent.setter
    def enable_agent(self, param):
        self.verify_boolean(param, "enable_agent")
        self._nv_pairs["ENABLE_AGENT"] = param

    @property
    def enable_default_queuing_policy(self):
        """
        return the current nv_pairs value of enable_default_queuing_policy

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ENABLE_DEFAULT_QUEUING_POLICY"]

    @enable_default_queuing_policy.setter
    def enable_default_queuing_policy(self, param):
        self.verify_boolean(param, "enable_default_queuing_policy")
        self._nv_pairs["ENABLE_DEFAULT_QUEUING_POLICY"] = param

    @property
    def enable_evpn(self):
        """
        return the current nv_pairs value of enable_evpn

        Valid values: boolean
        Default value: True
        """
        return self._nv_pairs["ENABLE_EVPN"]

    @enable_evpn.setter
    def enable_evpn(self, param):
        self.verify_boolean(param, "enable_evpn")
        self._nv_pairs["ENABLE_EVPN"] = param

    @property
    def enable_fabric_vpc_domain_id(self):
        """
        return the current nv_pairs value of enable_fabric_vpc_domain_id

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ENABLE_FABRIC_VPC_DOMAIN_ID"]

    @enable_fabric_vpc_domain_id.setter
    def enable_fabric_vpc_domain_id(self, param):
        self.verify_boolean(param, "enable_fabric_vpc_domain_id")
        self._nv_pairs["ENABLE_FABRIC_VPC_DOMAIN_ID"] = param

    @property
    def enable_fabric_vpc_domain_id_prev(self):
        """
        return the current nv_pairs value of enable_fabric_vpc_domain_id_prev

        Input validation is not currently performed.
        """
        return self._nv_pairs["ENABLE_FABRIC_VPC_DOMAIN_ID_PREV"]

    @enable_fabric_vpc_domain_id_prev.setter
    def enable_fabric_vpc_domain_id_prev(self, param):
        self._nv_pairs["ENABLE_FABRIC_VPC_DOMAIN_ID_PREV"] = param

    @property
    def enable_macsec(self):
        """
        return the current nv_pairs value of enable_macsec

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ENABLE_MACSEC"]

    @enable_macsec.setter
    def enable_macsec(self, param):
        self.verify_boolean(param, "enable_macsec")
        self._nv_pairs["ENABLE_MACSEC"] = param

    @property
    def enable_netflow(self):
        """
        Enable (True) or disable (False) Netflow on VTEPs

        NDFC GUI label: Enable Netflow
        NDFC gui tab: Flow Monitor

        Valid values: boolean
        Default value: False

        NOTES:
        - If True, the following are mandatory:
            - NETFLOW_EXPORTER_LIST
            - NETFLOW_RECORD_LIST
            - NETFLOW_MONITOR_LIST
        """
        return self._nv_pairs["ENABLE_NETFLOW"]

    @enable_netflow.setter
    def enable_netflow(self, param):
        self.verify_boolean(param, "enable_netflow")
        self._nv_pairs["ENABLE_NETFLOW"] = param

    @property
    def enable_netflow_prev(self):
        """
        return the current nv_pairs value of enable_netflow_prev

        Input validation is not currently performed.
        """
        return self._nv_pairs["ENABLE_NETFLOW_PREV"]

    @enable_netflow_prev.setter
    def enable_netflow_prev(self, param):
        self._nv_pairs["ENABLE_NETFLOW_PREV"] = param

    @property
    def enable_ngoam(self):
        """
        return the current nv_pairs value of enable_ngoam

        Valid values: boolean
        Default value: True
        """
        return self._nv_pairs["ENABLE_NGOAM"]

    @enable_ngoam.setter
    def enable_ngoam(self, param):
        self.verify_boolean(param, "enable_ngoam")
        self._nv_pairs["ENABLE_NGOAM"] = param

    @property
    def enable_nxapi(self):
        """
        return the current nv_pairs value of enable_nxapi

        Valid values: boolean
        Default value: True
        """
        return self._nv_pairs["ENABLE_NXAPI"]

    @enable_nxapi.setter
    def enable_nxapi(self, param):
        self.verify_boolean(param, "enable_nxapi")
        self._nv_pairs["ENABLE_NXAPI"] = param

    @property
    def enable_nxapi_http(self):
        """
        return the current nv_pairs value of enable_nxapi_http

        Valid values: boolean
        Default value: True
        """
        return self._nv_pairs["ENABLE_NXAPI_HTTP"]

    @enable_nxapi_http.setter
    def enable_nxapi_http(self, param):
        self.verify_boolean(param, "enable_nxapi_http")
        self._nv_pairs["ENABLE_NXAPI_HTTP"] = param

    @property
    def enable_pbr(self):
        """
        return the current nv_pairs value of enable_pbr

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ENABLE_PBR"]

    @enable_pbr.setter
    def enable_pbr(self, param):
        self.verify_boolean(param, "enable_pbr")
        self._nv_pairs["ENABLE_PBR"] = param

    @property
    def enable_pvlan(self):
        """
        return the current nv_pairs value of enable_pvlan

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ENABLE_PVLAN"]

    @enable_pvlan.setter
    def enable_pvlan(self, param):
        self.verify_boolean(param, "enable_pvlan")
        self._nv_pairs["ENABLE_PVLAN"] = param

    @property
    def enable_pvlan_prev(self):
        """
        return the current nv_pairs value of enable_pvlan_prev

        Input validation is not currently performed.
        """
        return self._nv_pairs["ENABLE_PVLAN_PREV"]

    @enable_pvlan_prev.setter
    def enable_pvlan_prev(self, param):
        self._nv_pairs["ENABLE_PVLAN_PREV"] = param

    @property
    def enable_tenant_dhcp(self):
        """
        return the current nv_pairs value of enable_tenant_dhcp

        Valid values: boolean
        Default value: True
        """
        return self._nv_pairs["ENABLE_TENANT_DHCP"]

    @enable_tenant_dhcp.setter
    def enable_tenant_dhcp(self, param):
        self.verify_boolean(param, "enable_tenant_dhcp")
        self._nv_pairs["ENABLE_TENANT_DHCP"] = param

    @property
    def enable_trm(self):
        """
        return the current nv_pairs value of enable_trm

        Valid values: boolean
        Default value: False

        NDFC GUI label: Enable Tenant Routed Multicast (TRM)
        NDFC GUI tab: Replication
        """
        return self._nv_pairs["ENABLE_TRM"]

    @enable_trm.setter
    def enable_trm(self, param):
        self.verify_boolean(param, "enable_trm")
        self._nv_pairs["ENABLE_TRM"] = param

    @property
    def enable_vpc_peer_link_native_vlan(self):
        """
        return the current nv_pairs value of enable_vpc_peer_link_native_vlan

        Valid values: boolean
        Default value: False
        """
        return self._nv_pairs["ENABLE_VPC_PEER_LINK_NATIVE_VLAN"]

    @enable_vpc_peer_link_native_vlan.setter
    def enable_vpc_peer_link_native_vlan(self, param):
        self.verify_boolean(param, "enable_vpc_peer_link_native_vlan")
        self._nv_pairs["ENABLE_VPC_PEER_LINK_NATIVE_VLAN"] = param

    @property
    def extra_conf_intra_links(self):
        """
        Additional CLIs For All Intra-Fabric Links

        NDFC GUI label: Intra-fabric Links Additional Config
        NDFC GUI tab: Advanced

        Input validation is not currently performed.
        """
        return self._nv_pairs["EXTRA_CONF_INTRA_LINKS"]

    @extra_conf_intra_links.setter
    def extra_conf_intra_links(self, param):
        self._nv_pairs["EXTRA_CONF_INTRA_LINKS"] = param

    @property
    def extra_conf_leaf(self):
        """
        Additional CLIs For All Leafs As Captured From Show Running
        Configuration

        NDFC GUI label: Leaf Freeform Config
        NDFC GUI tab: Advanced

        Input validation is not currently performed.
        """
        return self._nv_pairs["EXTRA_CONF_LEAF"]

    @extra_conf_leaf.setter
    def extra_conf_leaf(self, param):
        self._nv_pairs["EXTRA_CONF_LEAF"] = param

    @property
    def extra_conf_spine(self):
        """
        Additional CLIs For All Spines As Captured From Show Running
        Configuration

        NDFC GUI label: Spine Freeform Config
        NDFC GUI tab: Advanced

        Input validation is not currently performed.
        """
        return self._nv_pairs["EXTRA_CONF_SPINE"]

    @extra_conf_spine.setter
    def extra_conf_spine(self, param):
        self._nv_pairs["EXTRA_CONF_SPINE"] = param

    @property
    def extra_conf_tor(self):
        """
        Additional CLIs For All ToRs As Captured From Show Running
        Configuration

        NDFC GUI label: ToR Freeform Config
        NDFC GUI tab: Advanced

        Input validation is not currently performed.
        """
        return self._nv_pairs["EXTRA_CONF_TOR"]

    @extra_conf_tor.setter
    def extra_conf_tor(self, param):
        self._nv_pairs["EXTRA_CONF_TOR"] = param

    @property
    def fabric_interface_type(self):
        """
        The type of peering for intra-fabric links.
        Numbered(Point-to-Point) or Unnumbered

        NDFC GUI label: Fabric Interface Numbering
        NDFC GUI tab: General Parameters

        Valid values: "p2p", "unnumbered"
        Default: "p2p"
        """
        return self._nv_pairs["FABRIC_INTERFACE_TYPE"]

    @fabric_interface_type.setter
    def fabric_interface_type(self, param):
        if param in self.valid["fabric_interface_type"]:
            self._nv_pairs["FABRIC_INTERFACE_TYPE"] = param
            return
        msg = "exiting. expected one of "
        msg += f"{self.valid['fabric_interface_type']}, got {param}"
        self.logger.error(msg)
        sys.exit(1)

    @property
    def fabric_mtu(self):
        """
        Intra Fabric Interface MTU.

        Valid values: An even integer in range 576-9216
        Default: 9216

        NDFC GUI label: Intra Fabric Interface MTU
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["FABRIC_MTU"]

    @fabric_mtu.setter
    def fabric_mtu(self, param):
        params = {}
        params["value"] = param
        params["min"] = 576
        params["max"] = 9216
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        try:
            if self.validations.is_integer_even(param):
                self._nv_pairs["FABRIC_MTU"] = param
                return
        except TypeError as err:
            msg = f"exiting {err}"
            self.logger.error(msg)
            sys.exit(1)

    @property
    def fabric_mtu_prev(self):
        """
        return the current nv_pairs value of fabric_mtu_prev

        Input validation is not currently performed.
        """
        return self._nv_pairs["FABRIC_MTU_PREV"]

    @fabric_mtu_prev.setter
    def fabric_mtu_prev(self, param):
        self._nv_pairs["FABRIC_MTU_PREV"] = param

    @property
    def fabric_vpc_domain_id(self):
        """
        vPC Domain Id to be used on all vPC pairs

        This is not recommended.

        NDFC GUI label: Enable the same vPC Domain Id for all vPC Pairs
        NDFC GUI tab: VPC

        Valid values: Integer in range 1-1000
        Default value: ""

        enable_fabric_vpc_domain_id must be set to True if
        fabric_vpc_domain_id is set.
        """
        return self._nv_pairs["FABRIC_VPC_DOMAIN_ID"]

    @fabric_vpc_domain_id.setter
    def fabric_vpc_domain_id(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1
        params["max"] = 1000
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["FABRIC_VPC_DOMAIN_ID"] = param

    @property
    def fabric_vpc_domain_id_prev(self):
        """
        return the current nv_pairs value of fabric_vpc_domain_id_prev

        Input validation is not currently performed.
        """
        return self._nv_pairs["FABRIC_VPC_DOMAIN_ID_PREV"]

    @fabric_vpc_domain_id_prev.setter
    def fabric_vpc_domain_id_prev(self, param):
        self._nv_pairs["FABRIC_VPC_DOMAIN_ID_PREV"] = param

    @property
    def fabric_vpc_qos(self):
        """
        Enable Qos on spines for guaranteed delivery of vPC Fabric
        Peering communication

        Valid values: boolean
        Default value: False

        fabric_vpc_qos_policy_name must be set if fabric_vpc_qos is
        set to True

        NDFC GUI label: Enable the same vPC Domain Id for all vPC Pairs
        NDFC GUI tab: VPC
        """
        return self._nv_pairs["FABRIC_VPC_QOS"]

    @fabric_vpc_qos.setter
    def fabric_vpc_qos(self, param):
        self.verify_boolean(param, "fabric_vpc_qos")
        self._nv_pairs["FABRIC_VPC_QOS"] = param

    @property
    def fabric_vpc_qos_policy_name(self):
        """
        Qos Policy name to use on all spines

        fabric_vpc_qos should be set to True if this is set to
        anything other than ""

        NDFC's suggested name (if fabric_vpc_qos is set to True)
        is "spine_qos_for_fabric_vpc_peering"

        NDFC GUI label: Qos Policy Name
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["FABRIC_VPC_QOS_POLICY_NAME"]

    @fabric_vpc_qos_policy_name.setter
    def fabric_vpc_qos_policy_name(self, param):
        self._nv_pairs["FABRIC_VPC_QOS_POLICY_NAME"] = param

    @property
    def feature_ptp(self):
        """
        Enable Precision Time Protocol

        Valid values: boolean
        Default value: False

        NDFC GUI label: Enable Precision Time Protocol (PTP)
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["FEATURE_PTP"]

    @feature_ptp.setter
    def feature_ptp(self, param):
        self.verify_boolean(param, "fabric_vpc_qos")
        self._nv_pairs["FEATURE_PTP"] = param

    @property
    def feature_ptp_internal(self):
        """
        return the current nv_pairs value of feature_ptp_internal

        Input validation is not currently performed.
        """
        return self._nv_pairs["FEATURE_PTP_INTERNAL"]

    @feature_ptp_internal.setter
    def feature_ptp_internal(self, param):
        self._nv_pairs["FEATURE_PTP_INTERNAL"] = param

    @property
    def ff(self):
        """
        return the current nv_pairs value of ff

        Default value: "Easy_Fabric"

        Input validation is not currently performed.
        """
        return self._nv_pairs["FF"]

    @ff.setter
    def ff(self, param):
        self._nv_pairs["FF"] = param

    @property
    def grfield_debug_flag(self):
        """
        return the current nv_pairs value of grfield_debug_flag

        NDFC GUI label: Greenfield Cleanup Option
        NDFC GUI tab: Advanced
        Valid values: "Disable", "Enable"
        Default value: "Disable"
        """
        return self._nv_pairs["GRFIELD_DEBUG_FLAG"]

    @grfield_debug_flag.setter
    def grfield_debug_flag(self, param):
        try:
            self.validations.verify_disable_enable(param)
        except ValueError as err:
            self.logger(f"exiting. {err}")
        self._nv_pairs["GRFIELD_DEBUG_FLAG"] = param

    @property
    def hd_time(self):
        """
        NVE Source Inteface HoldDown Time, in seconds

        Valid values:  integer in range 1-1500
        Default: 180

        NDFC GUI label: VTEP HoldDown Time
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["HD_TIME"]

    @hd_time.setter
    def hd_time(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1
        params["max"] = 1500
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["HD_TIME"] = param

    @property
    def host_intf_admin_state(self):
        """
        Host interface administrative state

        Valid values: boolean
        Default value: True

        NDFC GUI label: Unshut Host Interfaces by Default
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["HOST_INTF_ADMIN_STATE"]

    @host_intf_admin_state.setter
    def host_intf_admin_state(self, param):
        self.verify_boolean(param, "host_intf_admin_state")
        self._nv_pairs["HOST_INTF_ADMIN_STATE"] = param

    @property
    def ibgp_peer_template(self):
        """
        Speficies the config used for RR and spines with border or
        border gateway role. This field should begin with ' template peer'
        or ' template peer-session'. This must have 2 leading spaces.

        Note! All configs should strictly match show run output, with
        respect to case and newlines. Any mismatches will yield unexpected
        diffs during deploy.

        NDFC GUI label: iBGP Peer-Template Config
        NDFC GUI tab: Protocols

        Input validation is not performed.
        """
        return self._nv_pairs["IBGP_PEER_TEMPLATE"]

    @ibgp_peer_template.setter
    def ibgp_peer_template(self, param):
        self._nv_pairs["IBGP_PEER_TEMPLATE"] = param

    @property
    def ibgp_peer_template_leaf(self):
        """
        return the current nv_pairs value of ibgp_peer_template_leaf

        Specifies the config used for leaf, border or border gateway. If this
        field is empty, the peer template defined in iBGP Peer-Template Config
        (ibgp_peer_template) is used on all BGP enabled devices (RRs, leafs,
        border or border gateway roles). This field should begin with
        ' template peer' or ' template peer-session'. This must have 2 leading
        spaces.

        Note! All configs should strictly match 'show run' output, with respect
        to case and newlines. Any mismatches will yield unexpected diffs during
        deploy.


        NDFC GUI label: Leaf/Border/Border Gateway iBGP Peer-Template Config
        NDFC GUI tab: Protocols

        Input validation is not performed.
        """
        return self._nv_pairs["IBGP_PEER_TEMPLATE_LEAF"]

    @ibgp_peer_template_leaf.setter
    def ibgp_peer_template_leaf(self, param):
        self._nv_pairs["IBGP_PEER_TEMPLATE_LEAF"] = param

    @property
    def inband_dhcp_servers(self):
        """
        Comma separated list of DHCP Server IPv4 Addresses

        Valid values: Python list of ipv4 addresses (max 3)
        Default value: ""

        NDFC GUI label: External DHCP Server IP Addresses
        NDFC GUI tab: Bootstrap

        NOTES:
        1.  bootstrap_enable must be set to True

        TODO: Revisit.  Currently these fields are not selectable in the GUI
        """
        return self._nv_pairs["INBAND_DHCP_SERVERS"]

    @inband_dhcp_servers.setter
    def inband_dhcp_servers(self, param):
        try:
            self.validations.verify_list(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        if len(param) > 3:
            msg = f"exiting. exceeded maximum of 3 addresses, got {param}"
            self.logger.error(msg)
            sys.exit(1)
        for item in param:
            try:
                self.validations.verify_ipv4_address(item)
            except AddressValueError as err:
                msg = "exiting. Expected python list of <= 3 ipv4 addresses "
                msg += f"got {param}. Detail: {err}"
                self.logger.error(msg)
                sys.exit(1)
        self._nv_pairs["INBAND_DHCP_SERVERS"] = ",".join(param)

    @property
    def inband_mgmt(self):
        """
        Manage switches with only Inband connectivity

        Valid values: boolean
        Default value: False

        NDFC GUI label: Inband Management
        NDFC GUI tab: Manageability

        """
        return self._nv_pairs["INBAND_MGMT"]

    @inband_mgmt.setter
    def inband_mgmt(self, param):
        self.verify_boolean(param, "inband_mgmt")
        self._nv_pairs["INBAND_MGMT"] = param

    @property
    def inband_mgmt_prev(self):
        """
        return the current nv_pairs value of inband_mgmt_prev

        Input validation is not performed.
        """
        return self._nv_pairs["INBAND_MGMT_PREV"]

    @inband_mgmt_prev.setter
    def inband_mgmt_prev(self, param):
        self._nv_pairs["INBAND_MGMT_PREV"] = param

    @property
    def isis_auth_enable(self):
        """
        Enable (True) or disable (False) IS-IS Authentication

        Valid values: boolean
        Default value: False

        NDFC GUI label: Enable IS-IS Authentication
        NDFC GUI tab: Protocols

        NOTES:
        1.  Underlay Routing Protocol (link_state_routing)
            must be set to "is-is" if isis_auth_enable is set
            to True.
        """
        return self._nv_pairs["ISIS_AUTH_ENABLE"]

    @isis_auth_enable.setter
    def isis_auth_enable(self, param):
        self.verify_boolean(param, "isis_auth_enable")
        self._nv_pairs["ISIS_AUTH_ENABLE"] = param

    @property
    def isis_auth_key(self):
        """
        Cisco Type 7 Encrypted authentication key

        Default value: ""

        NDFC GUI label: IS-IS Authentication Key
        NDFC GUI tab: Protocols

        Mandatory if isis_auth_enable is set to True

        Input validation is not performed.
        """
        return self._nv_pairs["ISIS_AUTH_KEY"]

    @isis_auth_key.setter
    def isis_auth_key(self, param):
        self._nv_pairs["ISIS_AUTH_KEY"] = param

    @property
    def isis_auth_keychain_key_id(self):
        """
        return the current nv_pairs value of isis_auth_keychain_key_id

        Valid values: integer in range 0-65535
        Default value: ""

        NDFC GUI label: IS-IS Authentication Key ID
        NDFC GUI tab: Protocols

        Mandatory if isis_auth_enable is set to True
        """
        return self._nv_pairs["ISIS_AUTH_KEYCHAIN_KEY_ID"]

    @isis_auth_keychain_key_id.setter
    def isis_auth_keychain_key_id(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 65535
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["ISIS_AUTH_KEYCHAIN_KEY_ID"] = param

    @property
    def isis_auth_keychain_name(self):
        """
        IS-IS Authentication Keychain Name

        NDFC GUI label: IS-IS Authentication Keychain Name
        NDFC GUI tab: Protocols

        Mandatory if isis_auth_enable is set to True
        """
        return self._nv_pairs["ISIS_AUTH_KEYCHAIN_NAME"]

    @isis_auth_keychain_name.setter
    def isis_auth_keychain_name(self, param):
        self._nv_pairs["ISIS_AUTH_KEYCHAIN_NAME"] = param

    @property
    def isis_level(self):
        """
        return the current nv_pairs value of isis_level

        Valid values: "level-1", "level-2"
        Default value: ""

        NDFC GUI label: IS-IS Level
        NDFC GUI tab: Protocols

        Mandatory if link_state_routing is set to "is-is"
        """
        return self._nv_pairs["ISIS_LEVEL"]

    @isis_level.setter
    def isis_level(self, param):
        self._nv_pairs["ISIS_LEVEL"] = param

    @property
    def isis_overload_elapse_time(self):
        """
        Clear the IS-IS overload bit after an elapsed time in seconds

        Valid values: integer in range 5-86400
        Default value when isis_overload_enable == False: ""
        Default value when isis_overload_enable == True: 60

        NDFC GUI label: IS-IS Overload Bit Elapsed Time
        NDFC GUI tab: Protocols

        Mandatory if isis_overload_enable is set to True
        """
        return self._nv_pairs["ISIS_OVERLOAD_ELAPSE_TIME"]

    @isis_overload_elapse_time.setter
    def isis_overload_elapse_time(self, param):
        params = {}
        params["value"] = param
        params["min"] = 5
        params["max"] = 86400
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["ISIS_OVERLOAD_ELAPSE_TIME"] = param

    @property
    def isis_overload_enable(self):
        """
        Enable (True) or disable (False) the IS-IS Overload Bit

        When enabled, set the overload bit for isis_overload_elapse_time
        after a reload

        NDFC GUI label: Set IS-IS Overload Bit
        NDFC GUI tab: Protocols

        """
        return self._nv_pairs["ISIS_OVERLOAD_ENABLE"]

    @isis_overload_enable.setter
    def isis_overload_enable(self, param):
        self.verify_boolean(param, "isis_overload_enable")
        self._nv_pairs["ISIS_OVERLOAD_ENABLE"] = param

    @property
    def isis_p2p_enable(self):
        """
        Enable (True) or disable (False) network point-to-point on
        fabric interfaces which are numbered

        Valid values: boolean
        Default value: False

        NDFC GUI label: Enable IS-IS Network Point-to-Point
        NDFC GUI tab: Protocols

        """
        return self._nv_pairs["ISIS_P2P_ENABLE"]

    @isis_p2p_enable.setter
    def isis_p2p_enable(self, param):
        self.verify_boolean(param, "isis_p2p_enable")
        self._nv_pairs["ISIS_P2P_ENABLE"] = param

    @property
    def l2_host_intf_mtu(self):
        """
        Maximum Transfer Unit for host-facing switchport interfaces

        Valid values: even integer in range 1500-9216
        Default value: 9216

        NDFC GUI label: Layer 2 Host Interface MTU
        NDFC GUI tab: Advanced

        """
        return self._nv_pairs["L2_HOST_INTF_MTU"]

    @l2_host_intf_mtu.setter
    def l2_host_intf_mtu(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1500
        params["max"] = 9216
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        try:
            if self.validations.is_integer_even(param):
                self._nv_pairs["L2_HOST_INTF_MTU"] = param
                return
        except TypeError as err:
            msg = f"exiting {err}"
            self.logger.error(msg)
            sys.exit(1)

    @property
    def l2_host_intf_mtu_prev(self):
        """
        return the current nv_pairs value of l2_host_intf_mtu_prev

        Input validation is not performed.
        """
        return self._nv_pairs["L2_HOST_INTF_MTU_PREV"]

    @l2_host_intf_mtu_prev.setter
    def l2_host_intf_mtu_prev(self, param):
        self._nv_pairs["L2_HOST_INTF_MTU_PREV"] = param

    @property
    def l2_segment_id_range(self):
        """
        Overlay Network Identifier Range

        Valid values: String with format "X-Y" where:
                      X <= Y
                      X >= 1
                      Y <= 16777214
        Default value: "30000-49000"

        NDFC GUI label: Layer 2 VXLAN VNI Range
        NDFC GUI tab: Resources

        Mandatory
        """
        return self._nv_pairs["L2_SEGMENT_ID_RANGE"]

    @l2_segment_id_range.setter
    def l2_segment_id_range(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1
        params["max"] = 16777214
        try:
            self.validations.verify_hypenated_range(params)
        except (ValueError, TypeError, KeyError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["L2_SEGMENT_ID_RANGE"] = param

    @property
    def l3vni_mcast_group(self):
        """
        return the current nv_pairs value of l3vni_mcast_group

        Valid values: unknown
        Default value: ""

        NDFC GUI label: TODO: this does not seem to correspond to any label
        NDFC GUI tab: unknown
        """
        return self._nv_pairs["L3VNI_MCAST_GROUP"]

    @l3vni_mcast_group.setter
    def l3vni_mcast_group(self, param):
        try:
            self.validations.verify_ipv4_multicast_address(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["L3VNI_MCAST_GROUP"] = param

    @property
    def l3_partition_id_range(self):
        """
        Overlay VRF Identifier Range

        Valid values: String with format "X-Y" where:
                      X <= Y
                      X >= 1
                      Y <= 16777214
        Default value: "50000-59000"

        NDFC GUI label: Layer 3 VXLAN VNI Range
        NDFC GUI tab: Resources

        Mandatory

        """
        return self._nv_pairs["L3_PARTITION_ID_RANGE"]

    @l3_partition_id_range.setter
    def l3_partition_id_range(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1
        params["max"] = 16777214
        try:
            self.validations.verify_hypenated_range(params)
        except (ValueError, TypeError, KeyError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["L3_PARTITION_ID_RANGE"] = param

    @property
    def link_state_routing(self):
        """
        Interior Gateway Protocol used for Spine-Leaf Connectivity

        Valid values: "is-is", "ospf"
        Default value: "ospf"

        NDFC GUI label: Underlay Routing Protocol
        NDFC GUI tab: General Parameters

        Mandatory
        """
        return self._nv_pairs["LINK_STATE_ROUTING"]

    @link_state_routing.setter
    def link_state_routing(self, param):
        # TODO: move link_state_routing validation to ndfc_fabric.py
        if param in self.valid["link_state_routing"]:
            self._nv_pairs["LINK_STATE_ROUTING"] = param
            return
        msg = f"exiting. expected one of {self.valid['link_state_routing']}, "
        msg += f"got {param}"
        self.logger.error(msg)
        sys.exit(1)

    @property
    def link_state_routing_tag(self):
        """
        return the current nv_pairs value of link_state_routing_tag

        Valid values: string. max length 20 characters.
        Default value: "UNDERLAY"

        NDFC GUI label: Underlay Routing Protocol Tag
        NDFC GUI tab: Protocols

        Mandatory
        """
        return self._nv_pairs["LINK_STATE_ROUTING_TAG"]

    @link_state_routing_tag.setter
    def link_state_routing_tag(self, param):
        try:
            params = {}
            params["string"] = param
            params["length"] = 20
            self.validations.verify_string_length(params)
        except (ValueError, TypeError, KeyError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["LINK_STATE_ROUTING_TAG"] = param

    @property
    def link_state_routing_tag_prev(self):
        """
        return the current nv_pairs value of link_state_routing_tag_prev

        Input validation is not performed.
        """
        return self._nv_pairs["LINK_STATE_ROUTING_TAG_PREV"]

    @link_state_routing_tag_prev.setter
    def link_state_routing_tag_prev(self, param):
        self._nv_pairs["LINK_STATE_ROUTING_TAG_PREV"] = param

    @property
    def loopback0_ipv6_range(self):
        """
        Loopback0 IPv6 Address Range

        NDFC GUI label: Underlay Routing Loopback IPv6 Range
        NDFC GUI tab: Resources

        underlay_is_v6 must be set to True
        """
        return self._nv_pairs["LOOPBACK0_IPV6_RANGE"]

    @loopback0_ipv6_range.setter
    def loopback0_ipv6_range(self, param):
        try:
            self.validations.verify_ipv6_network_range(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["LOOPBACK0_IPV6_RANGE"] = param

    @property
    def loopback0_ip_range(self):
        """
        Loopback0 IP Address Range

        NDFC GUI label: Underlay Routing Loopback IP Range
        NDFC GUI tab: Resources

        underlay_is_v6 must be set to False
        """
        return self._nv_pairs["LOOPBACK0_IP_RANGE"]

    @loopback0_ip_range.setter
    def loopback0_ip_range(self, param):
        try:
            self.validations.verify_ipv4_network_range(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["LOOPBACK0_IP_RANGE"] = param

    @property
    def loopback1_ipv6_range(self):
        """
        Loopback1 and Anycast Loopback IPv6 Address Range

        NDFC GUI label: Underlay VTEP Loopback IPv6 Range
        NDFC GUI tab: Resources

        underlay_is_v6 must be set to True
        """
        return self._nv_pairs["LOOPBACK1_IPV6_RANGE"]

    @loopback1_ipv6_range.setter
    def loopback1_ipv6_range(self, param):
        try:
            self.validations.verify_ipv6_network_range(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["LOOPBACK1_IPV6_RANGE"] = param

    @property
    def loopback1_ip_range(self):
        """
        Loopback1 IP Address Range

        NDFC GUI label: Underlay VTEP Loopback IP Range
        NDFC GUI tab: Resources

        underlay_is_v6 must be set to False
        """
        return self._nv_pairs["LOOPBACK1_IP_RANGE"]

    @loopback1_ip_range.setter
    def loopback1_ip_range(self, param):
        try:
            self.validations.verify_ipv4_network_range(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["LOOPBACK1_IP_RANGE"] = param

    @property
    def macsec_algorithm(self):
        """
        Primary MACsec Algorithm

        Valid values: "AES_128_CMAC", "AES_256_CMAC"
        Default value: ""

        NDFC GUI label: MACsec Primary Cryptographic Algorithm
        NDFC GUI tab: Advanced

        enable_macsec must be set to True
        """
        return self._nv_pairs["MACSEC_ALGORITHM"]

    @macsec_algorithm.setter
    def macsec_algorithm(self, param):
        try:
            self.validations.verify_macsec_algorithm(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["MACSEC_ALGORITHM"] = param

    @property
    def macsec_cipher_suite(self):
        """
        Primary MACsec Algorithm

        Valid values:
            - "GCM-AES-XPN-256"
            - "GCM-AES-128"
            - "GCM-AES-256"
            - "GCM-AES-XPN-128"
        Default value: ""

        NDFC GUI label: MACsec Cipher Suite
        NDFC GUI tab: Advanced

        enable_macsec must be set to True
        """
        return self._nv_pairs["MACSEC_CIPHER_SUITE"]

    @macsec_cipher_suite.setter
    def macsec_cipher_suite(self, param):
        # TODO: move macsec_cipher_suite validation to ndfc_fabric.py
        if param in self.valid["macsec_cipher_suite"]:
            self._nv_pairs["MACSEC_CIPHER_SUITE"] = param
        msg = f"exiting. expected one of {self.valid['macsec_cipher_suite']}, "
        msg += f"got {param}"
        self.logger.error(msg)
        sys.exit(1)

    @property
    def macsec_fallback_algorithm(self):
        """
        Falback MACsec Algorithm

        Valid values: "AES_128_CMAC", "AES_256_CMAC"
        Default value: ""

        NDFC GUI label: MACsec Fallback Cryptographic Algorithm
        NDFC GUI tab: Advanced

        enable_macsec must be set to True
        """
        return self._nv_pairs["MACSEC_FALLBACK_ALGORITHM"]

    @macsec_fallback_algorithm.setter
    def macsec_fallback_algorithm(self, param):
        # TODO: move macsec_fallback_algorithm validation to ndfc_fabric.py
        if param in self.valid["macsec_algorithm"]:
            self._nv_pairs["MACSEC_FALLBACK_ALGORITHM"] = param
        msg = f"exiting. expected one of {self.valid['macsec_algorithm']}, "
        msg += f"got {param}"
        self.logger.error(msg)
        sys.exit(1)

    @property
    def macsec_fallback_key_string(self):
        """
        MACsec Fallback Key String

        Valid values: Cisco Type 7 Encrypted Octet String
        Default value: ""

        NDFC GUI label: MACsec Fallback Key String
        NDFC GUI tab: Advanced

        enable_macsec must be set to True
        Mandatory if enable_macsec is set to True

        Input validation not performed
        """
        return self._nv_pairs["MACSEC_FALLBACK_KEY_STRING"]

    @macsec_fallback_key_string.setter
    def macsec_fallback_key_string(self, param):
        self._nv_pairs["MACSEC_FALLBACK_KEY_STRING"] = param

    @property
    def macsec_key_string(self):
        """
        MACsec Key String

        Valid values: Cisco Type 7 Encrypted Octet String
        Default value: ""

        NDFC GUI label: MACsec Primary Key String
        NDFC GUI tab: Advanced

        enable_macsec must be set to True
        Mandatory if enable_macsec is set to True

        Input validation not performed
        """
        return self._nv_pairs["MACSEC_KEY_STRING"]

    @macsec_key_string.setter
    def macsec_key_string(self, param):
        self._nv_pairs["MACSEC_KEY_STRING"] = param

    @property
    def macsec_report_timer(self):
        """
        MACsec Status Report Timer (in minutes)

        Valid values: integer in range 5-60
        Default value: 5 (if enable_macsec is True)
        Default value: "" (if enable_macset is False)

        NDFC GUI label: MACsec Status Report Timer
        NDFC GUI tab: Advanced

        enable_macsec must be set to True
        Mandatory if enable_macsec is set to True
        """
        return self._nv_pairs["MACSEC_REPORT_TIMER"]

    @macsec_report_timer.setter
    def macsec_report_timer(self, param):
        params = {}
        params["value"] = param
        params["min"] = 5
        params["max"] = 60
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["MACSEC_REPORT_TIMER"] = param

    @property
    def mgmt_gw(self):
        """
        Default Gateway For Management VRF On The Switch

        Valid values: IPv4 address
        Default value: ""

        NDFC GUI label: Switch Mgmt Default Gateway
        NDFC GUI tab: Bootstrap

        bootstrap_enable and dhcp_enable must be set to True
        """
        return self._nv_pairs["MGMT_GW"]

    @mgmt_gw.setter
    def mgmt_gw(self, param):
        self.validations.verify_ipv4_address(param)
        self._nv_pairs["MGMT_GW"] = param

    @property
    def mgmt_gw_internal(self):
        """
        return the current nv_pairs value of mgmt_gw_internal

        Input validation not performed.
        """
        return self._nv_pairs["MGMT_GW_INTERNAL"]

    @mgmt_gw_internal.setter
    def mgmt_gw_internal(self, param):
        self._nv_pairs["MGMT_GW_INTERNAL"] = param

    @property
    def mgmt_prefix(self):
        """
        IP prefix for the management subnet

        Valid values: integer in range 8-30
        Default value: ""

        NDFC GUI label: Switch Mgmt IP Subnet Prefix
        NDFC GUI tab: Bootstrap

        bootstrap_enable must be set to True
        dhcp_enable must be set to True
        """
        return self._nv_pairs["MGMT_PREFIX"]

    @mgmt_prefix.setter
    def mgmt_prefix(self, param):
        params = {}
        params["value"] = param
        params["min"] = 8
        params["max"] = 30
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["MGMT_PREFIX"] = param

    @property
    def mgmt_prefix_internal(self):
        """
        return the current nv_pairs value of mgmt_prefix_internal
        """
        return self._nv_pairs["MGMT_PREFIX_INTERNAL"]

    @mgmt_prefix_internal.setter
    def mgmt_prefix_internal(self, param):
        self._nv_pairs["MGMT_PREFIX_INTERNAL"] = param

    @property
    def mgmt_v6prefix(self):
        """
        return the current nv_pairs value of mgmt_v6prefix

        NDFC GUI label: None
        NDFC GUI tab: None

        Valid values: Unknown
        Default value: 64 (if underlay_is_v6 is set to True)

        This property is not currently represented in the NDFC GUI?
        """
        return self._nv_pairs["MGMT_V6PREFIX"]

    @mgmt_v6prefix.setter
    def mgmt_v6prefix(self, param):
        # TODO:4 Validation. mgmt_v6prefix
        self._nv_pairs["MGMT_V6PREFIX"] = param

    @property
    def mgmt_v6prefix_internal(self):
        """
        return the current nv_pairs value of mgmt_v6prefix_internal
        """
        return self._nv_pairs["MGMT_V6PREFIX_INTERNAL"]

    @mgmt_v6prefix_internal.setter
    def mgmt_v6prefix_internal(self, param):
        self._nv_pairs["MGMT_V6PREFIX_INTERNAL"] = param

    @property
    def mpls_handoff(self):
        """
        Enable (True) or disable (False) MPLS Handoff

        Valid value: boolean
        Default: False

        NDFC GUI label: Enable MPLS Handoff
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["MPLS_HANDOFF"]

    @mpls_handoff.setter
    def mpls_handoff(self, param):
        self.verify_boolean(param, "mpls_handoff")
        self._nv_pairs["MPLS_HANDOFF"] = param

    @property
    def mpls_lb_id(self):
        """
        Used for VXLAN to MPLS SR/LDP Handoff

        Valid value: integer in range 0-1023

        NDFC GUI label: Underlay MPLS Loopback Id
        NDFC GUI tab: Advanced

        NOTES:
        1. mpls_handoff must be set to True
        """
        return self._nv_pairs["MPLS_LB_ID"]

    @mpls_lb_id.setter
    def mpls_lb_id(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 1023
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["MPLS_LB_ID"] = param

    @property
    def mpls_loopback_ip_range(self):
        """
        Used for VXLAN to MPLS SR/LDP Handoff

        Valid value: An IPv4 network range e.g. 10.1.1.0/24

        NDFC GUI label: Underlay MPLS Loopback IP Range
        NDFC GUI tab: Resources

        NOTES:
        1. mpls_handoff must be set to True
        2. mpls_lb_id must be set
        """
        return self._nv_pairs["MPLS_LOOPBACK_IP_RANGE"]

    @mpls_loopback_ip_range.setter
    def mpls_loopback_ip_range(self, param):
        try:
            self.validations.verify_ipv4_network_range(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["MPLS_LOOPBACK_IP_RANGE"] = param

    @property
    def mso_connectivity_deployed(self):
        """
        return the current nv_pairs value of mso_connectivity_deployed

        Input not currently validated.
        """
        return self._nv_pairs["MSO_CONNECTIVITY_DEPLOYED"]

    @mso_connectivity_deployed.setter
    def mso_connectivity_deployed(self, param):
        # TODO:5 Validation. mso_connectivity_deployed
        self._nv_pairs["MSO_CONNECTIVITY_DEPLOYED"] = param

    @property
    def mso_controler_id(self):
        """
        return the current nv_pairs value of [sic] mso_controler_id

        Input not currently validated.
        """
        return self._nv_pairs["MSO_CONTROLER_ID"]

    @mso_controler_id.setter
    def mso_controler_id(self, param):
        # TODO:5 Validation. mso_controler_id
        self._nv_pairs["MSO_CONTROLER_ID"] = param

    @property
    def mso_site_group_name(self):
        """
        return the current nv_pairs value of mso_site_group_name

        Input not currently validated.
        """
        return self._nv_pairs["MSO_SITE_GROUP_NAME"]

    @mso_site_group_name.setter
    def mso_site_group_name(self, param):
        # TODO:4 Validation. mso_site_group_name
        self._nv_pairs["MSO_SITE_GROUP_NAME"] = param

    @property
    def mso_site_id(self):
        """
        return the current nv_pairs value of mso_site_id

        Input not currently validated.
        """
        return self._nv_pairs["MSO_SITE_ID"]

    @mso_site_id.setter
    def mso_site_id(self, param):
        # TODO:4 Validation. mso_site_id
        self._nv_pairs["MSO_SITE_ID"] = param

    @property
    def mst_instance_range(self):
        """
        MST instance range

        Valid value: Python list of integer ranges, within 0-4094

        Example: ["0-3", "5", "7-9", 4050-4094]
        Default: ["0"]

        NDFC GUI label: MST Instance Range
        NDFC GUI tab: Advanced

        NOTES:
        1. stp_root_option must be set to "mst"
        """
        return self._nv_pairs["MST_INSTANCE_RANGE"]

    @mst_instance_range.setter
    def mst_instance_range(self, param):
        if not isinstance(param, list):
            msg = f"exiting. expected python list. Got {param}"
            self.logger.error(msg)
            sys.exit(1)
        for mst_range in param:
            if not isinstance(mst_range, str):
                msg = f"exiting. expected python list of str(). Got {param}"
                self.logger.error(msg)
                sys.exit(1)
            if "-" in mst_range:
                mst_params = {}
                mst_params["value"] = mst_range
                mst_params["min"] = 0
                mst_params["max"] = 4094
                try:
                    self.validations.verify_hypenated_range(mst_params)
                except (ValueError, TypeError, KeyError) as err:
                    msg = f"exiting. {err}"
                    self.logger.error(msg)
                    sys.exit(1)
            else:
                try:
                    mst_range = int(mst_range)
                except (ValueError, TypeError):
                    msg = f"exiting. {mst_range} not convertible to int()"
                    self.logger.error(msg)
                    sys.exit(1)
                params = {}
                params["value"] = int(mst_range)
                params["min"] = 0
                params["max"] = 4094
                try:
                    self.validations.verify_integer_range(params)
                except (KeyError, TypeError, ValueError) as err:
                    msg = f"exiting. {err}"
                    self.logger.error(msg)
                    sys.exit(1)
        self._nv_pairs["MST_INSTANCE_RANGE"] = ",".join(param)

    @property
    def netflow_exporter_list(self):
        """
        One or Multiple Netflow Exporters

        A list of dict with the following keys:

        EXPORTER_NAME:
        - The name of the exporter
        - Example: exporter1
        IP:
        - The device/switch IP on which the exporter will be configured
        - IPv4 address without netmask
        - Example: 10.1.1.1
        VRF:
        - The VRF in which the exporter's SRC_IF_NAME lives
        - Example: myVrf
        SRC_IF_NAME:
        - The name of the exporter's source interface
        - Example: Loopback1
        UDP_PORT:
        - The source UDP port used by the exporter
        - Example: 6500

        NDFC GUI label: Netflow Exporter
        MDFC GUI tab: Flow Monitor

        NOTES:
        -   The length of the list must match both:
            - netflow_monitor_list
            - netflow_record_list
        """
        return self._nv_pairs["NETFLOW_EXPORTER_LIST"]

    @netflow_exporter_list.setter
    def netflow_exporter_list(self, param):
        self._validate_netflow_exporter_list(param)
        payload = {}
        payload["NETFLOW_EXPORTER_LIST"] = param
        self._nv_pairs["NETFLOW_EXPORTER_LIST"] = json.dumps(payload)

    @property
    def netflow_monitor_list(self):
        """
        One or Multiple Netflow Monitors

        A list of dict with the following keys:

        MONITOR_NAME:
        - The name of the monitor
        - Example: netflow-monitor
        RECORD_NAME:
        - The name of the record to be monitored
        - Example: ipv4-record
        EXPORTER1:
        - The name of the exporter
        - Must match an EXPORTER_NAME in netflow_exporter_list
        - Example: exporter1
        EXPORTER2:
        - Optional
        - Must match an EXPORTER_NAME in netflow_exporter_list
        - Example: exporter2

        NDFC GUI label: Netflow Monitor
        MDFC GUI tab: Flow Monitor

        NOTES:
        -   The length of the list must match both:
            - netflow_exporter_list
            - netflow_record_list
        """
        return self._nv_pairs["NETFLOW_MONITOR_LIST"]

    @netflow_monitor_list.setter
    def netflow_monitor_list(self, param):
        self._validate_netflow_monitor_list(param)
        payload = {}
        payload["NETFLOW_MONITOR_LIST"] = param
        self._nv_pairs["NETFLOW_MONITOR_LIST"] = json.dumps(payload)

    @property
    def netflow_record_list(self):
        """
        One or Multiple Netflow Records

        A list of dict with the following keys:

        RECORD_NAME:
        - The name of a record
        - Must match a RECORD_NAME in netflow_monitor_list
        - Example: ipv4-record
        RECORD_TEMPLATE:
        - The template for the netflow record
        - Must be one of the following:
            - netflow_ipv4_record
            - netflow_l2_record
        - Example: netflow_ipv4_record
        LAYER2_RECORD:
        - If True, RECORD_NAME is a L2 record
        - If False, RECORD_NAME is not a L2 record
        - Example: False

        NDFC GUI label: Netflow Monitor
        MDFC GUI tab: Flow Monitor

        NOTES:
        -   The length of the list must match both:
            - netflow_exporter_list
            - netflow_monitor_list
        """
        return self._nv_pairs["NETFLOW_RECORD_LIST"]

    @netflow_record_list.setter
    def netflow_record_list(self, param):
        self._validate_netflow_record_list(param)
        param = self._translate_netflow_record_list(param)
        payload = {}
        payload["NETFLOW_RECORD_LIST"] = param
        self._nv_pairs["NETFLOW_RECORD_LIST"] = json.dumps(payload)

    @property
    def phantom_rp_lb_id1(self):
        """
        Used for Bidir-PIM Phantom RP

        Valid value: integer in range 0-1023

        NDFC GUI label: Underlay Primary RP Loopback Id
        NDFC GUI tab: Replication

        NOTES:

        1. If rp_count is set to 2, phantom_rp_lb_id[1-2] must be set
        2. If rp_count is set to 4, phantom_rp_lb_id[1-4] must be set
        3. replication_mode must be set to "Multicast"
        4. rp_mode must be set to "bidir"
        """
        return self._nv_pairs["PHANTOM_RP_LB_ID1"]

    @phantom_rp_lb_id1.setter
    def phantom_rp_lb_id1(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 1023
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["PHANTOM_RP_LB_ID1"] = param

    @property
    def phantom_rp_lb_id2(self):
        """
        Used for Bidir-PIM Phantom RP

        Valid value: integer in range 0-1023

        NDFC GUI label: Underlay Primary RP Loopback Id
        NDFC GUI tab: Replication

        NOTES:

        1. If rp_count is set to 2, phantom_rp_lb_id[1-2] must be set
        2. If rp_count is set to 4, phantom_rp_lb_id[1-4] must be set
        3. replication_mode must be set to "Multicast"
        4. rp_mode must be set to "bidir"
        """
        return self._nv_pairs["PHANTOM_RP_LB_ID2"]

    @phantom_rp_lb_id2.setter
    def phantom_rp_lb_id2(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 1023
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["PHANTOM_RP_LB_ID2"] = param

    @property
    def phantom_rp_lb_id3(self):
        """
        Used for Bidir-PIM Phantom RP

        Valid value: integer in range 0-1023

        NDFC GUI label: Underlay Primary RP Loopback Id
        NDFC GUI tab: Replication

        NOTES:

        1. If rp_count is set to 2, phantom_rp_lb_id[1-2] must be set
        2. If rp_count is set to 4, phantom_rp_lb_id[1-4] must be set
        3. replication_mode must be set to "Multicast"
        4. rp_mode must be set to "bidir"
        """
        return self._nv_pairs["PHANTOM_RP_LB_ID3"]

    @phantom_rp_lb_id3.setter
    def phantom_rp_lb_id3(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 1023
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["PHANTOM_RP_LB_ID3"] = param

    @property
    def phantom_rp_lb_id4(self):
        """
        Used for Bidir-PIM Phantom RP

        Valid value: integer in range 0-1023

        NDFC GUI label: Underlay Primary RP Loopback Id
        NDFC GUI tab: Replication

        NOTES:

        1. If rp_count is set to 2, phantom_rp_lb_id[1-2] must be set
        2. If rp_count is set to 4, phantom_rp_lb_id[1-4] must be set
        3. replication_mode must be set to "Multicast"
        4. rp_mode must be set to "bidir"
        """
        return self._nv_pairs["PHANTOM_RP_LB_ID4"]

    @phantom_rp_lb_id4.setter
    def phantom_rp_lb_id4(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 1023
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["PHANTOM_RP_LB_ID4"] = param

    @property
    def router_id_range(self):
        """
        BGP Router ID for IPv6 Underlay

        NDFC GUI label: BGP Router ID Range for IPv6 Underlay
        NDFC GUI tab: Resources

        Mandatory when underlay_is_v6 is set to True
        """
        return self._nv_pairs["ROUTER_ID_RANGE"]

    @router_id_range.setter
    def router_id_range(self, param):
        try:
            self.validations.verify_ipv4_network_range(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["ROUTER_ID_RANGE"] = param

    @property
    def route_map_sequence_number_range(self):
        """
        Sequence number range for use with route-maps

        Valid values: String with format "X-Y" where:
        X min value: 1
        Y max value: 65534
        X < Y

        NDFC GUI label: Route Map Sequence Number Range
        MDFC GUI tab: Resources
        """
        return self._nv_pairs["ROUTE_MAP_SEQUENCE_NUMBER_RANGE"]

    @route_map_sequence_number_range.setter
    def route_map_sequence_number_range(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1
        params["max"] = 65534
        try:
            self.validations.verify_hypenated_range(params)
        except (ValueError, TypeError, KeyError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["ROUTE_MAP_SEQUENCE_NUMBER_RANGE"] = param

    @property
    def rp_count(self):
        """
        Number of spines acting as Rendezvous-Point (RP)

        Valid values: An integer.  Either 2 or 4.
        Default value: 2

        NDFC GUI label: Rendezvous-Points
        NDFC GUI tab: Replication

        NOTES:

        1. rp_count is not valid unless replication_mode is set to Multicast
        """
        return self._nv_pairs["RP_COUNT"]

    @rp_count.setter
    def rp_count(self, param):
        try:
            self.validations.verify_rp_count(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["RP_COUNT"] = param

    @property
    def rp_lb_id(self):
        """
        Used for vPC Peering in VXLANv6 Fabrics

        Valid value: integer in range 0-1023

        NDFC GUI label: Underlay Anycast Loopback Id
        NDFC GUI tab: Protocols
        """
        return self._nv_pairs["RP_LB_ID"]

    @rp_lb_id.setter
    def rp_lb_id(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 1023
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["RP_LB_ID"] = param

    @property
    def rp_mode(self):
        """
        return the current nv_pairs value of rp_mode

        Valid value: One of "asm" or "bidir"

        NDFC GUI label: RP Mode
        NDFC GUI tab: Replication

        NOTES:

        1. replication_mode must be "Multicast"
        """
        return self._nv_pairs["RP_MODE"]

    @rp_mode.setter
    def rp_mode(self, param):
        try:
            self.validations.verify_rp_mode(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["RP_MODE"] = param

    @property
    def rr_count(self):
        """
        The number of spines acting as route-reflectors

        Valid values: An integer.  Either 2 or 4.
        Default value: 2
        NDFC GUI label: Route-Reflectors
        NDFC GUI tab: General Parameters
        """
        return self._nv_pairs["RR_COUNT"]

    @rr_count.setter
    def rr_count(self, param):
        try:
            self.validations.verify_rr_count(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["RR_COUNT"] = param

    @property
    def seed_switch_core_interfaces(self):
        """
        Core-facing Interface list on Seed Switch

        Used for fabrics where bootstrap_enable and inband_mgmt are
        set to True (enabled).

        Valid values: a string. range of NX-OS style interface names
        Example: "Eth1/1-5,Eth1/7,Eth2/1-5,Eth2/7"

        NDFC GUI label: Seed Switch Fabric Interfaces
        NDFC GUI tab: Bootstrap

        See also:
        - spine_switch_core_interfaces

        NOTES:
        1. No input validation is done by this property
        """
        return self._nv_pairs["SEED_SWITCH_CORE_INTERFACES"]

    @seed_switch_core_interfaces.setter
    def seed_switch_core_interfaces(self, param):
        self._nv_pairs["SEED_SWITCH_CORE_INTERFACES"] = param

    # site_id
    # For EVPN Multi-Site Support (Min:1, Max: 281474976710655).
    # Defaults to Fabric ASN

    @property
    def spine_switch_core_interfaces(self):
        """
        Spine Switch Fabric Interfaces

        Used for fabrics where bootstrap_enable and inband_mgmt are
        set to True (enabled).

        Valid values: a string. range of NX-OS style interface names
        Example: "Eth1/1-5,Eth1/7,Eth2/1-5,Eth2/7"

        NDFC GUI label: Seed Switch Fabric Interfaces
        NDFC GUI tab: Bootstrap

        See also:
        - seed_switch_core_interfaces

        NOTES:
        1. No input validation is done by this property
        """
        return self._nv_pairs["SPINE_SWITCH_CORE_INTERFACES"]

    @spine_switch_core_interfaces.setter
    def spine_switch_core_interfaces(self, param):
        self._nv_pairs["SPINE_SWITCH_CORE_INTERFACES"] = param

    @property
    def stp_root_option(self):
        """
        Protocol to use for the Spanning Tree root bridge

        Valid value: string. One of "rpvst+", "mst", "unmanaged"

            rpvst+ : Rapid Per-VLAN Spanning Tree
               mst : Multi-Instance Spanning Tree
         unmanaged : STP Root not managed by NDFC

        Default value: "unmanaged"

        NDFC GUI label: Spanning Tree Root Bridge Protocol
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["STP_ROOT_OPTION"]

    @stp_root_option.setter
    def stp_root_option(self, param):
        try:
            self.validations.verify_stp_root_option(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["STP_ROOT_OPTION"] = param

    @property
    def stp_vlan_range(self):
        """
        Vlan range when stp_root_option is set to "rpvst+"

        Valid value: Python list of integer ranges, within 1-3967

        Examples:
            ["0-3", "5", "7-9", 3965-3967]
            ["10"]
        Default: ["1-3967"]

        NDFC GUI label: Spanning Tree VLAN Range
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["STP_VLAN_RANGE"]

    @stp_vlan_range.setter
    def stp_vlan_range(self, param):
        if not isinstance(param, list):
            msg = f"exiting. expected python list. Got {param}"
            self.logger.error(msg)
            sys.exit(1)
        for stp_range in param:
            if not isinstance(stp_range, str):
                msg = f"exiting. expected python list of str(). Got {param}"
                self.logger.error(msg)
                sys.exit(1)
            if "-" in stp_range:
                stp_params = {}
                stp_params["value"] = stp_range
                stp_params["min"] = 0
                stp_params["max"] = 3967
                try:
                    self.validations.verify_hypenated_range(stp_params)
                except (ValueError, TypeError, KeyError) as err:
                    msg = f"exiting. {err}"
                    self.logger.error(msg)
                    sys.exit(1)
            else:
                try:
                    stp_range = int(stp_range)
                except (ValueError, TypeError):
                    msg = f"exiting. {stp_range} not convertible to int()"
                    self.logger.error(msg)
                    sys.exit(1)
                params = {}
                params["value"] = int(stp_range)
                params["min"] = 0
                params["max"] = 3967
                try:
                    self.validations.verify_integer_range(params)
                except (KeyError, TypeError, ValueError) as err:
                    msg = f"exiting. {err}"
                    self.logger.error(msg)
                    sys.exit(1)
        self._nv_pairs["STP_VLAN_RANGE"] = ",".join(param)

    @property
    def strict_cc_mode(self):
        """
        Enable (True) or disable (False) bi-directional compliance checks to
        flag additional configs in the running config that are not in the
        intent/expected config

        Valid values: boolean
        Default value: False

        NDFC GUI label: Enable Strict Config Compliance
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["STRICT_CC_MODE"]

    @strict_cc_mode.setter
    def strict_cc_mode(self, param):
        self.verify_boolean(param, "strict_cc_mode")
        self._nv_pairs["STRICT_CC_MODE"] = param

    @property
    def subinterface_range(self):
        """
        Per Border Dot1q Range For VRF Lite Connectivity

        Valid value: hypenated string (X-Y) where:
        X >= 2
        Y <= 4093

        Default value: "2-511"
        Example: "2-4093"

        NDFC GUI label: Subinterface Dot1q Range
        NDFC GUI tab: Resources
        """
        return self._nv_pairs["SUBINTERFACE_RANGE"]

    @subinterface_range.setter
    def subinterface_range(self, param):
        params = {}
        params["value"] = param
        params["min"] = 2
        params["max"] = 4093
        try:
            self.validations.verify_hypenated_range(params)
        except (ValueError, TypeError, KeyError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["SUBINTERFACE_RANGE"] = param

    @property
    def subnet_range(self):
        """
        Address range from which to assign Numbered and Peer Link SVI IPs

        Valid value:    IPv4 network range, specified as X.X.X.X/Y
                        Where Y <= 31
        Default value: 10.33.0.0/16

        Example: 10.1.0.0/16

        NDFC GUI label: Underlay Subnet IP Range
        NDFC GUI tab: Resources
        """
        return self._nv_pairs["SUBNET_RANGE"]

    @subnet_range.setter
    def subnet_range(self, param):
        try:
            self.validations.verify_ipv4_network_range(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["SUBNET_RANGE"] = param

    @property
    def subnet_target_mask(self):
        """
        Mask for Underlay Subnet IP Range

        Valid value: integer in range 30-31
        Default value: 30

        NDFC GUI label: Underlay Subnet IP Mask
        NDFC GUI tab: General Parameters
        """
        return self._nv_pairs["SUBNET_TARGET_MASK"]

    @subnet_target_mask.setter
    def subnet_target_mask(self, param):
        params = {}
        params["value"] = param
        params["min"] = 30
        params["max"] = 31
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["SUBNET_TARGET_MASK"] = param

    @property
    def syslog_server_ip_list(self):
        """
        Python list of IP Unicast Addresses(v4/v6)

        Valid value: Python list containing IPv4/IPv6 addresses
        Default Value: ""

        Examples:
            ["10.1.1.1", "2001::1"]

        NDFC GUI label: Syslog Server IPs
        NDFC GUI tab: Manageability

        If syslog_server_ip_list is set, the following must also be set:
        - syslog_server_vrf
        - syslog_sev
        """
        return self._nv_pairs["SYSLOG_SERVER_IP_LIST"]

    @syslog_server_ip_list.setter
    def syslog_server_ip_list(self, param):
        try:
            self.validations.verify_list(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        for item in param:
            if self.validations.is_ipv4_unicast_address(item):
                continue
            if self.validations.is_ipv6_unicast_address(item):
                continue
            msg = "exiting. expected a python list of IPv4 and IPv6 unicast "
            msg += f"addresses. Got {param}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["SYSLOG_SERVER_IP_LIST"] = ",".join(param)

    @property
    def syslog_server_vrf(self):
        """
        Python list of VRF names

        Valid value: Python list containing vrf names
        Default Value: ""

        Examples:
            ["management", "foo"]

        NDFC GUI label: Syslog Server VRFs
        NDFC GUI tab: Manageability

        NOTES:
        1.  If the list contains a single VRF name, this VRF will apply to
            all syslog servers in syslog_server_ip_list.
        2.  If the list contains more than one VRF name, the length of the
            list must equal the length of syslog_server_ip_list.  Each VRF
            will apply to the corresponding entry in syslog_server_ip_list.
        """
        return self._nv_pairs["SYSLOG_SERVER_VRF"]

    @syslog_server_vrf.setter
    def syslog_server_vrf(self, param):
        try:
            self.validations.verify_list(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["SYSLOG_SERVER_VRF"] = ",".join(param)

    @property
    def syslog_sev(self):
        """
        Python list of Syslog severity values, one per Syslog server
        listed in syslog_server_ip_list.

        Valid value: Python list containing integers within range 0-7
        Default Value: ""

        Examples:
            [1,5]

        NDFC GUI label: Syslog Server Severity
        NDFC GUI tab: Manageability

        NOTES:
        1.  The list must contain the same number of elements as
            syslog_server_ip_list.  Each severity level will apply
            to the corresponding entry in syslog_server_ip_list.
        """
        return self._nv_pairs["SYSLOG_SEV"]

    @syslog_sev.setter
    def syslog_sev(self, param):
        try:
            self.validations.verify_list(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        for item in param:
            if not isinstance(item, int):
                msg = f"exiting. expected list of integers. got {param}"
                self.logger.error(msg)
                sys.exit(1)
        self._nv_pairs["SYSLOG_SEV"] = ",".join([str(x) for x in param])

    @property
    def tcam_allocation(self):
        """
        Enable (True) or disable (False) automatic generation of TCAM
        commands for VxLAN and vPC Fabric Peering

        Valid values: boolean
        Default value: True

        NDFC GUI label: Enable TCAM Allocation
        NDFC GUI tab: Advanced
        """
        return self._nv_pairs["TCAM_ALLOCATION"]

    @tcam_allocation.setter
    def tcam_allocation(self, param):
        self.verify_boolean(param, "tcam_allocation")
        self._nv_pairs["TCAM_ALLOCATION"] = param

    @property
    def underlay_is_v6(self):
        """
        return the current nv_pairs value of underlay_is_v6

        Valid values: boolean
        Default value: False

        NDFC GUI label: Enable IPv6 Underlay
        NDFC GUI tab: General Parameters

        If underlay_is_v6 is set to True, the following must also be set:
        -   anycast_lb_id
        -   loopback0_ipv6_range
        -   loopback1_ipv6_range
        -   router_id_range
        -   v6_subnet_range
        -   v6_subnet_target_mask
        """
        return self._nv_pairs["UNDERLAY_IS_V6"]

    @underlay_is_v6.setter
    def underlay_is_v6(self, param):
        self.verify_boolean(param, "underlay_is_v6")
        self._nv_pairs["UNDERLAY_IS_V6"] = param

    @property
    def unnum_bootstrap_lb_id(self):
        """
        return the current nv_pairs value of unnum_bootstrap_lb_id

        Valid values: integer in range 0-1023
        Default value: ""

        NDFC GUI label: Bootstrap Seed Switch Loopback Interface ID
        NDFC GUI tab: Bootstrap

        NOTES:
        1. bootstrap_enable must be set to True
        2. dhcp_enable must be set to True
        3. dhcp_end must be set
        4. dhcp_start must be set
        5. fabric_interface_type must be set to "unnumbered"
        6. unnum_dhcp_end must be set
        7. unnum_dhcp_start must be set
        """
        return self._nv_pairs["UNNUM_BOOTSTRAP_LB_ID"]

    @unnum_bootstrap_lb_id.setter
    def unnum_bootstrap_lb_id(self, param):
        params = {}
        params["value"] = param
        params["min"] = 0
        params["max"] = 1023
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["UNNUM_BOOTSTRAP_LB_ID"] = param

    @property
    def unnum_dhcp_end(self):
        """
        Must be a subset of IGP/BGP Loopback Prefix Pool

        NDFC GUI label: Switch Loopback DHCP Scope End Address
        NDFC GUI tab: Bootstrap
        """
        return self._nv_pairs["UNNUM_DHCP_END"]

    @unnum_dhcp_end.setter
    def unnum_dhcp_end(self, param):
        # TODO:2 Validation. unnum_dhcp_end
        self._nv_pairs["UNNUM_DHCP_END"] = param

    @property
    def unnum_dhcp_end_internal(self):
        """
        return the current nv_pairs value of unnum_dhcp_end_internal
        """
        return self._nv_pairs["UNNUM_DHCP_END_INTERNAL"]

    @unnum_dhcp_end_internal.setter
    def unnum_dhcp_end_internal(self, param):
        self._nv_pairs["UNNUM_DHCP_END_INTERNAL"] = param

    @property
    def unnum_dhcp_start(self):
        """
        Must be a subset of IGP/BGP Loopback Prefix Pool

        NDFC GUI label: Switch Loopback DHCP Scope Start Address
        NDFC GUI tab: Bootstrap
        """
        return self._nv_pairs["UNNUM_DHCP_START"]

    @unnum_dhcp_start.setter
    def unnum_dhcp_start(self, param):
        # TODO:2 Validation. unnum_dhcp_start
        self._nv_pairs["UNNUM_DHCP_START"] = param

    @property
    def unnum_dhcp_start_internal(self):
        """
        return the current nv_pairs value of unnum_dhcp_start_internal
        """
        return self._nv_pairs["UNNUM_DHCP_START_INTERNAL"]

    @unnum_dhcp_start_internal.setter
    def unnum_dhcp_start_internal(self, param):
        self._nv_pairs["UNNUM_DHCP_START_INTERNAL"] = param

    @property
    def use_link_local(self):
        """
        Enable (True) or disable (False) link-local IPv6 addresses
        for Spine-Leaf interfaces.  If set to False, Spine-Leaf
        interfaces will use IPv6 global addresses.

        Valid value: boolean
        Default value: False

        NDFC GUI label: Enable IPv6 Link-Local Address
        NDFC GUI tab: General Parameters

        """
        return self._nv_pairs["USE_LINK_LOCAL"]

    @use_link_local.setter
    def use_link_local(self, param):
        self.verify_boolean(param, "use_link_local")
        self._nv_pairs["USE_LINK_LOCAL"] = param

    @property
    def v6_subnet_range(self):
        """
        IPv6 Address range to assign Numbered and Peer Link SVI IPs

        Valid values: An IPv6 network range specified as ADDR/MASK

        Where: MASK <= 127

        Example: "fd00::a04:0/112"

        NDFC GUI label: Underlay Subnet IPv6 Range
        NDFC GUI tab: Resources
        """
        return self._nv_pairs["V6_SUBNET_RANGE"]

    @v6_subnet_range.setter
    def v6_subnet_range(self, param):
        try:
            self.validations.verify_ipv6_network_range(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
        self._nv_pairs["V6_SUBNET_RANGE"] = param

    @property
    def v6_subnet_target_mask(self):
        """
        Mask for Underlay Subnet IPv6 Range

        Valid values: integer in range 126-127
        Default value: 126

        NDFC GUI label: Underlay Subnet IPv6 Mask
        NDFC GUI tab: General Parameters

        NOTES:
        - underlay_is_v6 must be set to True
        """
        return self._nv_pairs["V6_SUBNET_TARGET_MASK"]

    @v6_subnet_target_mask.setter
    def v6_subnet_target_mask(self, param):
        params = {}
        params["value"] = param
        params["min"] = 126
        params["max"] = 127
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["V6_SUBNET_TARGET_MASK"] = param

    @property
    def vpc_auto_recovery_time(self):
        """
        vPC Auto Recovery Time (In Seconds)

        Valid values: integer in range 240-3600
        Default value: 360

        NDFC GUI label: vPC Auto Recovery Time (In Seconds)
        NDFC GUI tab: VPC
        """
        return self._nv_pairs["VPC_AUTO_RECOVERY_TIME"]

    @vpc_auto_recovery_time.setter
    def vpc_auto_recovery_time(self, param):
        params = {}
        params["value"] = param
        params["min"] = 240
        params["max"] = 3600
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["VPC_AUTO_RECOVERY_TIME"] = param

    @property
    def vpc_delay_restore(self):
        """
        return the current nv_pairs value of vpc_delay_restore
        """
        return self._nv_pairs["VPC_DELAY_RESTORE"]

    @vpc_delay_restore.setter
    def vpc_delay_restore(self, param):
        # TODO:1 Validation. vpc_delay_restore
        self._nv_pairs["VPC_DELAY_RESTORE"] = param

    @property
    def vpc_delay_restore_time(self):
        """
        vPC Delay Restore Time (In Seconds)

        Valid values: integer in range 1-3600
        Default value: 150

        NDFC GUI label: vPC Delay Restore Time (In Seconds)
        NDFC GUI tab: VPC
        """
        return self._nv_pairs["VPC_DELAY_RESTORE_TIME"]

    @vpc_delay_restore_time.setter
    def vpc_delay_restore_time(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1
        params["max"] = 3600
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["VPC_DELAY_RESTORE_TIME"] = param

    @property
    def vpc_domain_id_range(self):
        """
        vPC Domain id range to use for new pairings

        Valid values: hyphenated integer range X-Y, where X > 0 and Y <= 1000
        Default value: 1-1000

        NDFC GUI label: vPC Domain Id Range
        NDFC GUI tab: VPC
        """
        return self._nv_pairs["VPC_DOMAIN_ID_RANGE"]

    @vpc_domain_id_range.setter
    def vpc_domain_id_range(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1
        params["max"] = 1000
        try:
            self.validations.verify_hypenated_range(params)
        except (ValueError, TypeError, KeyError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["VPC_DOMAIN_ID_RANGE"] = param

    @property
    def vpc_enable_ipv6_nd_sync(self):
        """
        Enable (True) or disable (False) synchronization of IPv6 neighbor
        discovery across VPC peers

        Valid values: boolean
        Default value: True

        NDFC GUI label: vPC IPv6 ND Synchronize
        NDFC GUI tab: VPC
        """
        return self._nv_pairs["VPC_ENABLE_IPv6_ND_SYNC"]

    @vpc_enable_ipv6_nd_sync.setter
    def vpc_enable_ipv6_nd_sync(self, param):
        self.verify_boolean(param, "vpc_enable_ipv6_nd_sync")
        self._nv_pairs["VPC_ENABLE_IPv6_ND_SYNC"] = param

    @property
    def vpc_peer_keep_alive_option(self):
        """
        Port-channel ID for VPC Port-channel

        Valid values: One of "management" or "loopback"
        Default value: management

        NDFC GUI label: vPC Peer Keep Alive option
        NDFC GUI tab: VPC
        """
        return self._nv_pairs["VPC_PEER_KEEP_ALIVE_OPTION"]

    @vpc_peer_keep_alive_option.setter
    def vpc_peer_keep_alive_option(self, param):
        try:
            self.validations.verify_vpc_peer_keepalive_option(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["VPC_PEER_KEEP_ALIVE_OPTION"] = param

    @property
    def vpc_peer_link_po(self):
        """
        Port-channel ID for VPC Port-channel

        Valid values: integer in range 1-4096
        Default value: 500

        NDFC GUI label: vPC Peer Link Port Channel ID
        NDFC GUI tab: VPC
        """
        return self._nv_pairs["VPC_PEER_LINK_PO"]

    @vpc_peer_link_po.setter
    def vpc_peer_link_po(self, param):
        params = {}
        params["value"] = param
        params["min"] = 1
        params["max"] = 4096
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["VPC_PEER_LINK_PO"] = param

    @property
    def vpc_peer_link_vlan(self):
        """
        VLAN for vPC Peer Link SVI

        Valid values: integer in range 2-4094
        Default value: 3600

        NDFC GUI label: vPC Peer Link VLAN
        NDFC GUI tab: VPC
        """
        return self._nv_pairs["VPC_PEER_LINK_VLAN"]

    @vpc_peer_link_vlan.setter
    def vpc_peer_link_vlan(self, param):
        params = {}
        params["value"] = param
        params["min"] = 2
        params["max"] = 4094
        try:
            self.validations.verify_integer_range(params)
        except (KeyError, TypeError, ValueError) as err:
            self.logger(f"exiting. {err}")
            sys.exit(1)
        self._nv_pairs["VPC_PEER_LINK_VLAN"] = param

    @property
    def vrf_lite_autoconfig(self):
        """
        return the current nv_pairs value of vrf_lite_autoconfig
        """
        return self._nv_pairs["VRF_LITE_AUTOCONFIG"]

    @vrf_lite_autoconfig.setter
    def vrf_lite_autoconfig(self, param):
        # TODO:1 Validation. vrf_lite_autoconfig
        self._nv_pairs["VRF_LITE_AUTOCONFIG"] = param

    @property
    def vrf_vlan_range(self):
        """
        return the current nv_pairs value of vrf_vlan_range
        """
        return self._nv_pairs["VRF_VLAN_RANGE"]

    @vrf_vlan_range.setter
    def vrf_vlan_range(self, param):
        # TODO:1 Validation. vrf_vlan_range
        self._nv_pairs["VRF_VLAN_RANGE"] = param
