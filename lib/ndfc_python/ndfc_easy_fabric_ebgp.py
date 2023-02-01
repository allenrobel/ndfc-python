#!/usr/bin/env python
"""
Name: ndfc_fabric_site_easy_fabric_ebgp.py
Description: Create NDFC site fabrics using Easy_Fabric_eBGP template
"""
import sys
from ndfc_python.ndfc_fabric import NdfcFabric

OUR_VERSION = 100


class NdfcEasyFabricEbgp(NdfcFabric):
    """
    Create site/child fabric using Easy_Fabric_eBGP template

    Example create operation:

    instance = NdfcEasyFabricEbgp(ndfc)
    instance.fabric_name = 'easy_fabric_ebgp_1'
    instance.bgp_as = 65011
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
        self.properties_set.add("fabricName")
        self.properties_set.add("templateName")

    def _init_properties_mandatory_set(self):
        """
        Initialize a set containing mandatory properties
        """
        self.properties_mandatory_set = set()
        self.properties_mandatory_set.add("fabricName")

    def _init_nv_pairs_default(self):
        """
        Initialize default values for nv pairs
        """
        self._nv_pairs_default = {}
        self._nv_pairs_default["AAA_REMOTE_IP_ENABLED"] = "false"
        self._nv_pairs_default["AAA_SERVER_CONF"] = ""
        self._nv_pairs_default["ACTIVE_MIGRATION"] = "false"
        self._nv_pairs_default["ADVERTISE_PIP_BGP"] = "false"
        self._nv_pairs_default["ANYCAST_GW_MAC"] = ""
        self._nv_pairs_default["ANYCAST_RP_IP_RANGE"] = ""
        self._nv_pairs_default["ANYCAST_RP_IP_RANGE_INTERNAL"] = ""
        self._nv_pairs_default["BFD_AUTH_ENABLE"] = "false"
        self._nv_pairs_default["BFD_AUTH_KEY"] = ""
        self._nv_pairs_default["BFD_AUTH_KEY_ID"] = ""
        self._nv_pairs_default["BFD_ENABLE"] = "false"
        self._nv_pairs_default["BFD_IBGP_ENABLE"] = "false"
        # mandatory
        #self._nv_pairs_default["BGP_AS"] = "65200"
        self._nv_pairs_default["BGP_AS_MODE"] = "Multi-AS" # "Same-Tier-AS"
        self._nv_pairs_default["BGP_AUTH_ENABLE"] = "false"
        self._nv_pairs_default["BGP_AUTH_KEY"] = ""
        self._nv_pairs_default["BGP_AUTH_KEY_TYPE"] = "" # "3"
        self._nv_pairs_default["BGP_LB_ID"] = "0" # "0"
        self._nv_pairs_default["BGP_MAX_PATH"] = "4"
        self._nv_pairs_default["BOOTSTRAP_CONF"] = ""
        self._nv_pairs_default["BOOTSTRAP_ENABLE"] = "false"
        self._nv_pairs_default["BOOTSTRAP_MULTISUBNET"] = ""
        self._nv_pairs_default["BOOTSTRAP_MULTISUBNET_INTERNAL"] = ""
        self._nv_pairs_default["BRFIELD_DEBUG_FLAG"] = "Disable"
        self._nv_pairs_default["CDP_ENABLE"] = "false"
        self._nv_pairs_default["COPP_POLICY"] = "strict" # dense, lenient, moderate
        self._nv_pairs_default["DCI_SUBNET_RANGE"] = "10.33.0.0/16"
        self._nv_pairs_default["DCI_SUBNET_TARGET_MASK"] = "30"
        # self._nv_pairs_default["DEAFULT_QUEUING_POLICY_CLOUDSCALE"] = "queuing_policy_default_8q_cloudscale"
        # self._nv_pairs_default["DEAFULT_QUEUING_POLICY_OTHER"] = "queuing_policy_default_other"
        # self._nv_pairs_default["DEAFULT_QUEUING_POLICY_R_SERIES"] = "queuing_policy_default_r_series"
        self._nv_pairs_default["DEAFULT_QUEUING_POLICY_CLOUDSCALE"] = ""
        self._nv_pairs_default["DEAFULT_QUEUING_POLICY_OTHER"] = ""
        self._nv_pairs_default["DEAFULT_QUEUING_POLICY_R_SERIES"] = ""
        self._nv_pairs_default["DEPLOYMENT_FREEZE"] = "false"
        self._nv_pairs_default["DHCP_ENABLE"] = "false"
        self._nv_pairs_default["DHCP_END"] = ""
        self._nv_pairs_default["DHCP_END_INTERNAL"] = ""
        self._nv_pairs_default["DHCP_IPV6_ENABLE"] = "DHCPv4"
        self._nv_pairs_default["DHCP_IPV6_ENABLE_INTERNAL"] = ""
        self._nv_pairs_default["DHCP_START"] = ""
        self._nv_pairs_default["DHCP_START_INTERNAL"] = ""
        self._nv_pairs_default["DNS_SERVER_IP_LIST"] = ""
        self._nv_pairs_default["DNS_SERVER_VRF"] = ""
        self._nv_pairs_default["ENABLE_AAA"] = "false"
        self._nv_pairs_default["ENABLE_DEFAULT_QUEUING_POLICY"] = "false"
        self._nv_pairs_default["ENABLE_EVPN"] = "false"
        self._nv_pairs_default["ENABLE_FABRIC_VPC_DOMAIN_ID"] = "false"
        self._nv_pairs_default["ENABLE_FABRIC_VPC_DOMAIN_ID_PREV"] = "false"
        self._nv_pairs_default["ENABLE_MACSEC"] = "false"
        self._nv_pairs_default["ENABLE_NETFLOW"] = "false"
        self._nv_pairs_default["ENABLE_NETFLOW_PREV"] = "false"
        self._nv_pairs_default["ENABLE_NGOAM"] = "true"
        self._nv_pairs_default["ENABLE_NXAPI"] = "true"
        self._nv_pairs_default["ENABLE_NXAPI_HTTP"] = "true"
        self._nv_pairs_default["ENABLE_TENANT_DHCP"] = "false"
        self._nv_pairs_default["ENABLE_TRM"] = "false"
        self._nv_pairs_default["ENABLE_VPC_PEER_LINK_NATIVE_VLAN"] = "false"
        self._nv_pairs_default["EXTRA_CONF_INTRA_LINKS"] = ""
        self._nv_pairs_default["EXTRA_CONF_LEAF"] = ""
        self._nv_pairs_default["EXTRA_CONF_SPINE"] = ""
        self._nv_pairs_default["FABRIC_INTERFACE_TYPE"] = "p2p"
        self._nv_pairs_default["FABRIC_MTU"] = "9216"
        self._nv_pairs_default["FABRIC_MTU_PREV"] = "9216"
        # mandatory
        #self._nv_pairs_default["FABRIC_NAME"] = "Easy_Fabric_EBGP_1"
        self._nv_pairs_default["FABRIC_TECHNOLOGY"] = "EBGPVXLANFabric"
        self._nv_pairs_default["FABRIC_TYPE"] = "Switch_Fabric"
        self._nv_pairs_default["FABRIC_VPC_DOMAIN_ID"] = ""
        self._nv_pairs_default["FABRIC_VPC_DOMAIN_ID_PREV"] = ""
        self._nv_pairs_default["FABRIC_VPC_QOS"] = "false"
        self._nv_pairs_default["FABRIC_VPC_QOS_POLICY_NAME"] = "spine_qos_for_fabric_vpc_peering"
        self._nv_pairs_default["FF"] = "Easy_Fabric_eBGP"
        self._nv_pairs_default["FHRP_PROTOCOL"] = "hsrp"
        self._nv_pairs_default["GRFIELD_DEBUG_FLAG"] = "Disable"
        self._nv_pairs_default["HD_TIME"] = "" # "180"
        self._nv_pairs_default["L2_HOST_INTF_MTU"] = "9216"
        self._nv_pairs_default["L2_HOST_INTF_MTU_PREV"] = "9216"
        self._nv_pairs_default["L2_SEGMENT_ID_RANGE"] = ""
        self._nv_pairs_default["L3VNI_MCAST_GROUP"] = ""
        self._nv_pairs_default["L3_PARTITION_ID_RANGE"] = ""
        self._nv_pairs_default["LINK_STATE_ROUTING"] = "ebgp"
        self._nv_pairs_default["LINK_STATE_ROUTING_TAG"] = "UNDERLAY"
        self._nv_pairs_default["LOOPBACK0_IPV6_RANGE"] = ""
        self._nv_pairs_default["LOOPBACK0_IP_RANGE"] = "10.2.0.0/22"
        self._nv_pairs_default["LOOPBACK1_IP_RANGE"] = ""
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
        self._nv_pairs_default["MGMT_V6PREFIX_INTERNAL"] = "64"
        #self._nv_pairs_default["MULTICAST_GROUP_SUBNET"] = "239.1.1.0/25"
        self._nv_pairs_default["MULTICAST_GROUP_SUBNET"] = ""
        self._nv_pairs_default["NETFLOW_EXPORTER_LIST"] = ""
        self._nv_pairs_default["NETFLOW_MONITOR_LIST"] = ""
        self._nv_pairs_default["NETFLOW_RECORD_LIST"] = ""
        self._nv_pairs_default["NETWORK_VLAN_RANGE"] = "2300-2999"
        self._nv_pairs_default["NTP_SERVER_IP_LIST"] = ""
        self._nv_pairs_default["NTP_SERVER_VRF"] = ""
        self._nv_pairs_default["NVE_LB_ID"] = "" # "1"
        self._nv_pairs_default["OSPF_AREA_ID"] = "0.0.0.0"
        #self._nv_pairs_default["OVERLAY_MODE"] = "cli"
        self._nv_pairs_default["OVERLAY_MODE"] = "" # cli
        self._nv_pairs_default["OVERLAY_MODE_PREV"] = ""
        self._nv_pairs_default["PHANTOM_RP_LB_ID1"] = ""
        self._nv_pairs_default["PHANTOM_RP_LB_ID2"] = ""
        self._nv_pairs_default["PHANTOM_RP_LB_ID3"] = ""
        self._nv_pairs_default["PHANTOM_RP_LB_ID4"] = ""
        self._nv_pairs_default["PIM_HELLO_AUTH_ENABLE"] = "false"
        self._nv_pairs_default["PIM_HELLO_AUTH_KEY"] = ""
        self._nv_pairs_default["PM_ENABLE"] = "false"
        self._nv_pairs_default["PM_ENABLE_PREV"] = "false"
        self._nv_pairs_default["POWER_REDUNDANCY_MODE"] = "ps-redundant" # combined, insrc-redundant
        self._nv_pairs_default["PREV_EVPN_FLAG"] = "" # "false"
        self._nv_pairs_default["PREV_FHRP_PROTOCOL"] = "hsrp"
        #self._nv_pairs_default["REPLICATION_MODE"] = "Multicast" # Ingress
        self._nv_pairs_default["REPLICATION_MODE"] = "" # Ingress, Multicast
        self._nv_pairs_default["ROUTE_MAP_TAG"] = "12345"
        self._nv_pairs_default["RP_COUNT"] = "" # "2"
        self._nv_pairs_default["RP_LB_ID"] = ""
        self._nv_pairs_default["RP_MODE"] = "" # "asm"
        self._nv_pairs_default["RR_COUNT"] = "2"
        self._nv_pairs_default["SNMP_SERVER_HOST_TRAP"] = "true"
        self._nv_pairs_default["STATIC_UNDERLAY_IP_ALLOC"] = "false"
        self._nv_pairs_default["STRICT_CC_MODE"] = "false"
        self._nv_pairs_default["SUBINTERFACE_RANGE"] = "2-511"
        self._nv_pairs_default["SUBNET_RANGE"] = "10.4.0.0/16"
        self._nv_pairs_default["SUBNET_TARGET_MASK"] = "30"
        self._nv_pairs_default["SUPER_SPINE_BGP_AS"] = ""
        self._nv_pairs_default["SYSLOG_SERVER_IP_LIST"] = ""
        self._nv_pairs_default["SYSLOG_SERVER_VRF"] = ""
        self._nv_pairs_default["SYSLOG_SEV"] = ""
        self._nv_pairs_default["TCAM_ALLOCATION"] = "true"
        self._nv_pairs_default["UNDERLAY_IS_V6"] = "false"
        self._nv_pairs_default["UNDERLAY_IS_V6_PREV"] = "false"
        self._nv_pairs_default["USE_LINK_LOCAL"] = "true"
        self._nv_pairs_default["VPC_AUTO_RECOVERY_TIME"] = "360"
        self._nv_pairs_default["VPC_DELAY_RESTORE"] = "150"
        self._nv_pairs_default["VPC_DOMAIN_ID_RANGE"] = "1-1000"
        self._nv_pairs_default["VPC_ENABLE_IPv6_ND_SYNC"] = "true"
        self._nv_pairs_default["VPC_PEER_KEEP_ALIVE_OPTION"] = "management" # loopback
        self._nv_pairs_default["VPC_PEER_LINK_PO"] = "500"
        self._nv_pairs_default["VPC_PEER_LINK_VLAN"] = "3600"
        self._nv_pairs_default["VRF_LITE_AUTOCONFIG"] = "" # "Manual"
        self._nv_pairs_default["VRF_VLAN_RANGE"] = ""
        self._nv_pairs_default["abstract_anycast_rp"] = "anycast_rp"
        self._nv_pairs_default["abstract_bgp"] = "base_bgp"
        self._nv_pairs_default["abstract_dhcp"] = "base_dhcp"
        self._nv_pairs_default["abstract_extra_config_bootstrap"] = "extra_config_bootstrap_11_1"
        self._nv_pairs_default["abstract_extra_config_leaf"] = "extra_config_leaf"
        self._nv_pairs_default["abstract_extra_config_spine"] = "extra_config_spine"
        self._nv_pairs_default["abstract_feature_leaf"] = "base_feature_leaf_upg"
        self._nv_pairs_default["abstract_feature_spine"] = "base_feature_spine_upg"
        self._nv_pairs_default["abstract_loopback_interface"] = "int_fabric_loopback_11_1"
        self._nv_pairs_default["abstract_multicast"] = "base_multicast_11_1"
        self._nv_pairs_default["abstract_pim_interface"] = "pim_interface"
        self._nv_pairs_default["abstract_route_map"] = "route_map"
        self._nv_pairs_default["abstract_routed_host"] = "int_routed_host"
        self._nv_pairs_default["abstract_trunk_host"] = "int_trunk_host"
        self._nv_pairs_default["abstract_vlan_interface"] = "int_fabric_vlan_11_1"
        self._nv_pairs_default["abstract_vpc_domain"] = "base_vpc_domain_11_1"
        self._nv_pairs_default["dcnmUser"] = "admin"
        self._nv_pairs_default["default_asn_template"] = "bgp_asn"
        #self._nv_pairs_default["default_network"] = "Routed_Network_Universal"
        self._nv_pairs_default["default_network"] = ""
        #self._nv_pairs_default["default_vrf"] = "Default_VRF_Universal"
        self._nv_pairs_default["default_vrf"] = ""
        self._nv_pairs_default["enableRealTimeBackup"] = ""
        self._nv_pairs_default["enableScheduledBackup"] = ""
        #self._nv_pairs_default["network_extension_template"] = "Routed_Network_Universal"
        self._nv_pairs_default["network_extension_template"] = ""
        self._nv_pairs_default["scheduledTime"] = ""
        self._nv_pairs_default["temp_anycast_gateway"] = "anycast_gateway"
        self._nv_pairs_default["temp_vpc_domain_mgmt"] = "vpc_domain_mgmt"
        self._nv_pairs_default["temp_vpc_peer_link"] = "int_vpc_peer_link_po"
        #self._nv_pairs_default["vrf_extension_template"] = "Default_VRF_Extension_Universal"
        self._nv_pairs_default["vrf_extension_template"] = ""

    def _init_nv_pairs_set(self):
        """
        Initialize a set containing all nv pairs
        """
        self._nv_pairs_set = set()
        self._nv_pairs_set.add("AAA_REMOTE_IP_ENABLED")
        self._nv_pairs_set.add("AAA_SERVER_CONF")
        self._nv_pairs_set.add("ACTIVE_MIGRATION")
        self._nv_pairs_set.add("ADVERTISE_PIP_BGP")
        self._nv_pairs_set.add("ANYCAST_GW_MAC")
        self._nv_pairs_set.add("ANYCAST_RP_IP_RANGE")
        self._nv_pairs_set.add("ANYCAST_RP_IP_RANGE_INTERNAL")
        self._nv_pairs_set.add("BFD_AUTH_ENABLE")
        self._nv_pairs_set.add("BFD_AUTH_KEY")
        self._nv_pairs_set.add("BFD_AUTH_KEY_ID")
        self._nv_pairs_set.add("BFD_ENABLE")
        self._nv_pairs_set.add("BFD_IBGP_ENABLE")
        self._nv_pairs_set.add("BGP_AS")
        self._nv_pairs_set.add("BGP_AS_MODE")
        self._nv_pairs_set.add("BGP_AUTH_ENABLE")
        self._nv_pairs_set.add("BGP_AUTH_KEY")
        self._nv_pairs_set.add("BGP_AUTH_KEY_TYPE")
        self._nv_pairs_set.add("BGP_LB_ID")
        self._nv_pairs_set.add("BGP_MAX_PATH")
        self._nv_pairs_set.add("BOOTSTRAP_CONF")
        self._nv_pairs_set.add("BOOTSTRAP_ENABLE")
        self._nv_pairs_set.add("BOOTSTRAP_MULTISUBNET")
        self._nv_pairs_set.add("BOOTSTRAP_MULTISUBNET_INTERNAL")
        self._nv_pairs_set.add("BRFIELD_DEBUG_FLAG")
        self._nv_pairs_set.add("CDP_ENABLE")
        self._nv_pairs_set.add("COPP_POLICY")
        self._nv_pairs_set.add("DCI_SUBNET_RANGE")
        self._nv_pairs_set.add("DCI_SUBNET_TARGET_MASK")
        self._nv_pairs_set.add("DEAFULT_QUEUING_POLICY_CLOUDSCALE")
        self._nv_pairs_set.add("DEAFULT_QUEUING_POLICY_OTHER")
        self._nv_pairs_set.add("DEAFULT_QUEUING_POLICY_R_SERIES")
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
        self._nv_pairs_set.add("ENABLE_TENANT_DHCP")
        self._nv_pairs_set.add("ENABLE_TRM")
        self._nv_pairs_set.add("ENABLE_VPC_PEER_LINK_NATIVE_VLAN")
        self._nv_pairs_set.add("EXTRA_CONF_INTRA_LINKS")
        self._nv_pairs_set.add("EXTRA_CONF_LEAF")
        self._nv_pairs_set.add("EXTRA_CONF_SPINE")
        self._nv_pairs_set.add("FABRIC_INTERFACE_TYPE")
        self._nv_pairs_set.add("FABRIC_MTU")
        self._nv_pairs_set.add("FABRIC_MTU_PREV")
        self._nv_pairs_set.add("FABRIC_NAME")
        self._nv_pairs_set.add("FABRIC_TECHNOLOGY")
        self._nv_pairs_set.add("FABRIC_TYPE")
        self._nv_pairs_set.add("FABRIC_VPC_DOMAIN_ID")
        self._nv_pairs_set.add("FABRIC_VPC_DOMAIN_ID_PREV")
        self._nv_pairs_set.add("FABRIC_VPC_QOS")
        self._nv_pairs_set.add("FABRIC_VPC_QOS_POLICY_NAME")
        self._nv_pairs_set.add("FF")
        self._nv_pairs_set.add("FHRP_PROTOCOL")
        self._nv_pairs_set.add("GRFIELD_DEBUG_FLAG")
        self._nv_pairs_set.add("HD_TIME")
        self._nv_pairs_set.add("L2_HOST_INTF_MTU")
        self._nv_pairs_set.add("L2_HOST_INTF_MTU_PREV")
        self._nv_pairs_set.add("L2_SEGMENT_ID_RANGE")
        self._nv_pairs_set.add("L3VNI_MCAST_GROUP")
        self._nv_pairs_set.add("L3_PARTITION_ID_RANGE")
        self._nv_pairs_set.add("LINK_STATE_ROUTING")
        self._nv_pairs_set.add("LINK_STATE_ROUTING_TAG")
        self._nv_pairs_set.add("LOOPBACK0_IPV6_RANGE")
        self._nv_pairs_set.add("LOOPBACK0_IP_RANGE")
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
        self._nv_pairs_set.add("MULTICAST_GROUP_SUBNET")
        self._nv_pairs_set.add("NETFLOW_EXPORTER_LIST")
        self._nv_pairs_set.add("NETFLOW_MONITOR_LIST")
        self._nv_pairs_set.add("NETFLOW_RECORD_LIST")
        self._nv_pairs_set.add("NETWORK_VLAN_RANGE")
        self._nv_pairs_set.add("NTP_SERVER_IP_LIST")
        self._nv_pairs_set.add("NTP_SERVER_VRF")
        self._nv_pairs_set.add("NVE_LB_ID")
        self._nv_pairs_set.add("OSPF_AREA_ID")
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
        self._nv_pairs_set.add("PREV_EVPN_FLAG")
        self._nv_pairs_set.add("PREV_FHRP_PROTOCOL")
        self._nv_pairs_set.add("REPLICATION_MODE")
        self._nv_pairs_set.add("ROUTE_MAP_TAG")
        self._nv_pairs_set.add("RP_COUNT")
        self._nv_pairs_set.add("RP_LB_ID")
        self._nv_pairs_set.add("RP_MODE")
        self._nv_pairs_set.add("RR_COUNT")
        self._nv_pairs_set.add("SNMP_SERVER_HOST_TRAP")
        self._nv_pairs_set.add("STATIC_UNDERLAY_IP_ALLOC")
        self._nv_pairs_set.add("STRICT_CC_MODE")
        self._nv_pairs_set.add("SUBINTERFACE_RANGE")
        self._nv_pairs_set.add("SUBNET_RANGE")
        self._nv_pairs_set.add("SUBNET_TARGET_MASK")
        self._nv_pairs_set.add("SUPER_SPINE_BGP_AS")
        self._nv_pairs_set.add("SYSLOG_SERVER_IP_LIST")
        self._nv_pairs_set.add("SYSLOG_SERVER_VRF")
        self._nv_pairs_set.add("SYSLOG_SEV")
        self._nv_pairs_set.add("TCAM_ALLOCATION")
        self._nv_pairs_set.add("UNDERLAY_IS_V6")
        self._nv_pairs_set.add("UNDERLAY_IS_V6_PREV")
        self._nv_pairs_set.add("USE_LINK_LOCAL")
        self._nv_pairs_set.add("VPC_AUTO_RECOVERY_TIME")
        self._nv_pairs_set.add("VPC_DELAY_RESTORE")
        self._nv_pairs_set.add("VPC_DOMAIN_ID_RANGE")
        self._nv_pairs_set.add("VPC_ENABLE_IPv6_ND_SYNC")
        self._nv_pairs_set.add("VPC_PEER_KEEP_ALIVE_OPTION")
        self._nv_pairs_set.add("VPC_PEER_LINK_PO")
        self._nv_pairs_set.add("VPC_PEER_LINK_VLAN")
        self._nv_pairs_set.add("VRF_LITE_AUTOCONFIG")
        self._nv_pairs_set.add("VRF_VLAN_RANGE")
        self._nv_pairs_set.add("abstract_anycast_rp")
        self._nv_pairs_set.add("abstract_bgp")
        self._nv_pairs_set.add("abstract_dhcp")
        self._nv_pairs_set.add("abstract_extra_config_bootstrap")
        self._nv_pairs_set.add("abstract_extra_config_leaf")
        self._nv_pairs_set.add("abstract_extra_config_spine")
        self._nv_pairs_set.add("abstract_feature_leaf")
        self._nv_pairs_set.add("abstract_feature_spine")
        self._nv_pairs_set.add("abstract_loopback_interface")
        self._nv_pairs_set.add("abstract_multicast")
        self._nv_pairs_set.add("abstract_pim_interface")
        self._nv_pairs_set.add("abstract_route_map")
        self._nv_pairs_set.add("abstract_routed_host")
        self._nv_pairs_set.add("abstract_trunk_host")
        self._nv_pairs_set.add("abstract_vlan_interface")
        self._nv_pairs_set.add("abstract_vpc_domain")
        self._nv_pairs_set.add("dcnmUser")
        self._nv_pairs_set.add("default_asn_template")
        self._nv_pairs_set.add("default_network")
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
        """
        self._nv_pairs_mandatory_set = set()
        self._nv_pairs_mandatory_set = self._nv_pairs_set.difference(
            self._nv_pairs_default
        )

    def _init_properties_default(self):
        """
        Initialize default properties (currently there are no default properties)
        """
        self.properties_default = {}
        self.properties_default["templateName"] = "Easy_Fabric_eBGP"

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
        Set all nv_pairs params to default initially.
        User can override these through the exposed properties.
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
        if self._nv_pairs["FABRIC_NAME"] != "":
            self.properties["fabricName"] = self._nv_pairs["FABRIC_NAME"]

    def _final_verification(self):
        """
        Any final verifications go here
        """
        for param in self.properties_mandatory_set:
            if self.properties[param] == "":
                msg = f"exiting. call instance.{param.lower()} before calling instance.post()"
                self.ndfc.log.error(msg)
                sys.exit(1)
        for param in self._nv_pairs_mandatory_set:
            if self._nv_pairs[param] == "":
                msg = f"exiting. call instance.{param.lower()} before calling instance.post()"
                self.ndfc.log.error(msg)
                sys.exit(1)


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
        self._nv_pairs["BGP_AS"] = str(param)


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
    def fabric_mtu(self):
        """
        return the current nv_pairs value of fabric_mtu
        """
        return self._nv_pairs["FABRIC_MTU"]

    @fabric_mtu.setter
    def fabric_mtu(self, param):
        self._nv_pairs["FABRIC_MTU"] = param


    @property
    def fabric_name(self):
        """
        return the current nv_pairs value of fabric_name
        """
        return self._nv_pairs["FABRIC_NAME"]

    @fabric_name.setter
    def fabric_name(self, param):
        self._nv_pairs["FABRIC_NAME"] = param


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
