"""
Name:

ndfc_msd_fabric.py

Description:

Create fabric using the NDFC "VXLAN EVPN Multi-Site" (MSD_Fabric) template

NOTES:

1.  If valid_border_gwy_connections is set to Centralized_To_Route_Server
    The following are added to the mandatory nv_pairs set:
        - bgp_rp_asn
        - rp_server_ip
"""

import sys
from ipaddress import AddressValueError
from re import sub

from ndfc_python.ndfc_fabric import NdfcFabric, NdfcRequestError

OUR_VERSION = 102


class NdfcMsdFabric(NdfcFabric):
    """
    Create fabric using the Multisite Domain template.

    Example create operation:

    from ndfc_python.log import log
    from ndfc_python.ndfc import NDFC
    from ndfc_python.ndfc_credentials import NdfcCredentials
    from ndfc_python.ndfc_fabric import NdfcFabric

    logger = log('example_log', 'INFO', 'DEBUG')
    nc = NdfcCredentials()
    ndfc = NDFC()
    ndfc.log = logger
    ndfc.domain = nc.nd_domain
    ndfc.username = nc.username
    ndfc.password = nc.password
    ndfc.login()

    instance = NdfcMsdFabric()
    instance.logger = logger
    instance.ndfc = ndfc
    instance.fabric_name = 'MSD'
    instance.bgp_as = 65535
    instance.create()

    TODO: Need a delete() method
    """

    def __init__(self):
        super().__init__()
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self._nv_pairs = {}
        self._nv_pairs_default = {}
        self._nv_pairs_set = set()
        self._nv_pairs_mandatory_set = set()
        self._properties = {}
        self._properties_default = {}
        self._properties_set = set()
        self._properties_mandatory_set = set()

        self._init_property_map()

    def _init_properties_default(self):
        """
        Override NdfcFabric._init_properties_default()
        Initialize default top-level properties
        """
        self._properties_default = {}
        self._properties_default["templateName"] = "MSD_Fabric"

    def _init_properties_set(self):
        """
        Override NdfcFabric._init_properties_set()
        Initialize a set containing all properties
        """
        self._properties_set = set(self._properties_default.keys())
        self._properties_set.add("fabricName")

    def _init_properties_mandatory_set(self):
        """
        Override NdfcFabric._init_properties_mandatory_set()
        Initialize a set containing mandatory properties
        """
        self._properties_mandatory_set = self._properties_set

    def _init_properties(self):
        """
        Override NdfcFabric._init_properties()
        Initialize all top-level properties
        """
        self._properties = {}
        for param in self._properties_set:
            if param in self._properties_default:
                self._properties[param] = self._properties_default[param]
            else:
                self._properties[param] = ""

    def _init_nv_pairs_default(self):
        """
        Override NdfcFabric._init_nv_pairs_default()
        Initialize default values for nv pairs

        These are NDFC's default values. It's quite likely you'll want to
        modify some of these (properties are provided for this).  For example,
        by default NDFC does not auto-configure border gateway connections.
        You'd want to change BORDER_GWY_CONNECTIONS to either "Direct_To_BGWS"
        or "Centralized_To_Route_Server" if you want NDFC to automate these
        connections.
        """
        self._nv_pairs_default = {}
        self._nv_pairs_default["default_network"] = "Default_Network_Universal"
        self._nv_pairs_default["default_pvlan_sec_network"] = ""
        self._nv_pairs_default["default_vrf"] = "Default_VRF_Universal"
        self._nv_pairs_default["enableScheduledBackup"] = ""
        self._nv_pairs_default[
            "network_extension_template"
        ] = "Default_Network_Extension_Universal"
        self._nv_pairs_default["scheduledTime"] = ""
        self._nv_pairs_default[
            "vrf_extension_template"
        ] = "Default_VRF_Extension_Universal"
        self._nv_pairs_default["ANYCAST_GW_MAC"] = "2020.0000.00aa"
        self._nv_pairs_default["BGP_RP_ASN"] = ""
        self._nv_pairs_default["BGW_ROUTING_TAG"] = "54321"
        self._nv_pairs_default["BGW_ROUTING_TAG_PREV"] = "54321"
        self._nv_pairs_default["BORDER_GWY_CONNECTIONS"] = "Manual"
        self._nv_pairs_default["CLOUDSEC_ALGORITHM"] = ""
        self._nv_pairs_default["CLOUDSEC_AUTOCONFIG"] = False
        self._nv_pairs_default["CLOUDSEC_KEY_STRING"] = ""
        self._nv_pairs_default["CLOUDSEC_ENFORCEMENT"] = ""
        self._nv_pairs_default["CLOUDSEC_REPORT_TIMER"] = ""
        self._nv_pairs_default["DCI_SUBNET_RANGE"] = "10.10.1.0/24"
        self._nv_pairs_default["DCI_SUBNET_TARGET_MASK"] = "30"
        self._nv_pairs_default["DCNM_ID"] = ""
        self._nv_pairs_default["DELAY_RESTORE"] = "300"
        self._nv_pairs_default["ENABLE_BGP_BFD"] = False
        self._nv_pairs_default["ENABLE_BGP_LOG_NEIGHBOR_CHANGE"] = False
        self._nv_pairs_default["ENABLE_BGP_SEND_COMM"] = False
        self._nv_pairs_default["ENABLE_PVLAN"] = False
        self._nv_pairs_default["ENABLE_PVLAN_PREV"] = ""
        self._nv_pairs_default["ENABLE_RS_REDIST_DIRECT"] = False
        self._nv_pairs_default["FABRIC_TYPE"] = "MFD"
        self._nv_pairs_default["FF"] = "MSD"
        self._nv_pairs_default["L2_SEGMENT_ID_RANGE"] = "30000-49000"
        self._nv_pairs_default["L3_PARTITION_ID_RANGE"] = "50000-59000"
        self._nv_pairs_default["LOOPBACK100_IP_RANGE"] = "10.10.0.0/24"
        self._nv_pairs_default["MSO_CONTROLER_ID"] = ""
        self._nv_pairs_default["MSO_SITE_GROUP_NAME"] = ""
        self._nv_pairs_default["MS_LOOPBACK_ID"] = "100"
        self._nv_pairs_default["MS_IFC_BGP_AUTH_KEY_TYPE"] = ""
        self._nv_pairs_default["MS_IFC_BGP_AUTH_KEY_TYPE_PREV"] = ""
        self._nv_pairs_default["MS_IFC_BGP_PASSWORD"] = ""
        self._nv_pairs_default["MS_IFC_BGP_PASSWORD_PREV"] = ""
        self._nv_pairs_default["MS_IFC_BGP_PASSWORD_ENABLE"] = False
        self._nv_pairs_default["MS_IFC_BGP_PASSWORD_ENABLE_PREV"] = ""
        self._nv_pairs_default["MS_UNDERLAY_AUTOCONFIG"] = False
        self._nv_pairs_default["PREMSO_PARENT_FABRIC"] = ""
        self._nv_pairs_default["RP_SERVER_IP"] = ""
        self._nv_pairs_default["RS_ROUTING_TAG"] = ""
        self._nv_pairs_default["TOR_AUTO_DEPLOY"] = False

    def _init_nv_pairs_set(self):
        """
        Override NdfcFabric._init_nv_pairs_set()
        Initialize a set containing ALL nvPair key names
        """
        self._nv_pairs_set = set(self._nv_pairs_default.keys())
        self._nv_pairs_set.add("FABRIC_NAME")

    def _init_nv_pairs_mandatory_set(self):
        """
        Override NdfcFabric._init_nv_pairs_mandatory_set()
        Initialize a set containing mandatory nvPairs.
        This is the difference between all nvPairs and default nvPairs
        """
        self._nv_pairs_mandatory_set = set()
        self._nv_pairs_mandatory_set = self._nv_pairs_set.difference(
            self._nv_pairs_default
        )

    def _init_nv_pairs(self):
        """
        Initialize all nv_pairs
        Override NdfcFabric._init_nv_pairs()
        """
        self._nv_pairs = {}
        for param in self._nv_pairs_set:
            if param in self._nv_pairs_default:
                self._nv_pairs[param] = self._nv_pairs_default[param]
            else:
                self._nv_pairs[param] = ""

    def _init_property_map(self):
        """
        This class standardizes on lowercase dunder property names,
        while NDFC uses both camelCase and upper-case SNAKE_CASE names.
        For messages involving the original NDFC parameter names,
        self._property_map provides a way to map these into the property
        name conventions of this class.

        self._property_map is keyed on NDFC parameter names. The value is the
        name used in this class.
        """
        self._property_map = {}
        for param in self._properties_set.union(self._nv_pairs_set):
            # convert all dunder params to lowercase
            if "_" in param:
                self._property_map[param] = param.lower()
                continue
            # convert camel case to dunder
            pattern = r"(?<!^)(?=[A-Z])"
            self._property_map[param] = sub(pattern, "_", param).lower()
        # fix any corner-cases
        self._property_map["FF"] = "ff"

    def _preprocess_properties(self):
        """
        1. Align the properties to the expectations of NDFC
        """

    def _final_verification(self):
        self._ndfc_verification()
        for param in self._properties_mandatory_set:
            try:
                self.validations.verify_property_has_value(
                    param, self._properties[param]
                )
            except ValueError:
                msg = f"exiting. call instance.{self._property_map[param]} "
                msg += "before calling instance.post()"
                self.logger.error(msg)
                sys.exit(1)
        for param in self._nv_pairs_mandatory_set:
            if param not in self._nv_pairs:
                msg = f"exiting. call instance.{self._property_map[param]} "
                msg += "before calling instance.post()"
                self.logger.error(msg)
                sys.exit(1)
            try:
                value = self._nv_pairs[param]
                self.validations.verify_property_has_value(param, value)
            except ValueError:
                msg = f"exiting. call instance.{self._property_map[param]} "
                msg += "before calling instance.post()"
                self.logger.error(msg)
                sys.exit(1)

        # hack for black linter vs flake8 linter
        ctrs = "Centralized_To_Route_Server"
        if self._nv_pairs["BORDER_GWY_CONNECTIONS"] == ctrs:
            # If the user has selected Centralized_To_Route_Server connection
            # type, RP_SERVER_IP BGP_RP_ASN are both mandatory
            for param in ["RP_SERVER_IP", "BGP_RP_ASN"]:
                try:
                    nvp = self._nv_pairs[param]
                    self.validations.verify_property_has_value(param, nvp)
                except ValueError as err:
                    msg = "exiting, "
                    msg += "border_gwy_connections is set to "
                    msg += "Centralized_To_Route_Server which requires that "
                    msg += "both rp_server_ip and bgp_rp_asn be set, "
                    msg += f"exception detail: {err}"
                    self.logger.error(msg)
                    sys.exit(1)
            # RP_SERVER_IP and BGP_RP_ASN lists must be equal length
            try:
                nv_param = self._nv_pairs["BGP_RP_ASN"]
                self.validations.verify_list_lengths_are_equal(
                    self._nv_pairs["RP_SERVER_IP"], nv_param
                )
            except TypeError as err:
                msg = "rp_server_ip and bgp_rp_asn must be python lists. "
                msg += f"exception detail: {err}"
                self.logger.error(msg)
                sys.exit(1)
            except ValueError as err:
                msg = "rp_server_ip and bgp_rp_asn lists must be the "
                msg += f"same length, error detail {err}"
                self.logger.error(msg)
                sys.exit(1)
            # NDFC expects bgp_rp_asn and rp_server_ip to be comma-separated
            # string lists
            self._nv_pairs["BGP_RP_ASN"] = ",".join(
                [str(x) for x in self._nv_pairs["BGP_RP_ASN"]]
            )
            self._nv_pairs["RP_SERVER_IP"] = ",".join(
                [str(x) for x in self._nv_pairs["RP_SERVER_IP"]]
            )

    def create(self):
        """
        Create the MSD fabric
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

        payload = {}
        payload["fabricName"] = self.fabric_name
        payload["templateName"] = self.template_name
        payload["nvPairs"] = self._nv_pairs
        headers = {}
        headers["Authorization"] = self.ndfc.bearer_token
        headers["Content-Type"] = "application/json"

        try:
            self.ndfc.post(url, headers, payload)
        except NdfcRequestError as err:
            msg = f"error creating fabric {self.fabric_name}, "
            msg += f"error detail {err}"
            self.logger.error(msg)
            sys.exit(1)

    # Payload top-level properties
    @property
    def fabric_name(self):
        """
        return the current fabric name
        fabricName appears in the payload as both fabricName and
        nvPairs.FABRIC_NAME.  We return only the value for
        fabricName, but we keep both of these sync'ed in the
        setter below.
        """
        return self._properties["fabricName"]

    @fabric_name.setter
    def fabric_name(self, param):
        """
        fabricName appears in the payload as both fabricName and
        nvPairs.FABRIC_NAME.  We provide only one property, fabric_name,
        so need to ensure these are sync'ed.  We do this by setting
        the values for both below.
        """
        try:
            self.validations.verify_fabric_name(param)
        except (TypeError, ValueError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._properties["fabricName"] = param
        self._nv_pairs["FABRIC_NAME"] = param

    @property
    def template_name(self):
        """
        return the current fabric template name
        """
        return self._properties["templateName"]

    @template_name.setter
    def template_name(self, param):
        self._properties["templateName"] = param

    # nvPairs
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
    def default_vrf(self):
        """
        return the current nv_pairs value of default_vrf
        """
        return self._nv_pairs["default_vrf"]

    @default_vrf.setter
    def default_vrf(self, param):
        self._nv_pairs["default_vrf"] = param

    @property
    def enable_scheduled_backup(self):
        """
        return the current nv_pairs value of enableScheduledBackup
        """
        return self._nv_pairs["enableScheduledBackup"]

    @enable_scheduled_backup.setter
    def enable_scheduled_backup(self, param):
        self._nv_pairs["enableScheduledBackup"] = param

    @property
    def network_extension_template(self):
        """
        return the current nv_pairs value of network_extension_template
        """
        return self._nv_pairs["network_extension_template"]

    @network_extension_template.setter
    def network_extension_template(self, param):
        self._nv_pairs["network_extension_template"] = param

    @property
    def scheduled_time(self):
        """
        return the current nv_pairs value of scheduledTime
        """
        return self._nv_pairs["scheduledTime"]

    @scheduled_time.setter
    def scheduled_time(self, param):
        self._nv_pairs["scheduledTime"] = param

    @property
    def vrf_extension_template(self):
        """
        return the current nv_pairs value of vrf_extension_template
        """
        return self._nv_pairs["vrf_extension_template"]

    @vrf_extension_template.setter
    def vrf_extension_template(self, param):
        self._nv_pairs["vrf_extension_template"] = param

    @property
    def anycast_gw_mac(self):
        """
        return the current nv_pairs value of ANYCAST_GW_MAC
        """
        return self._nv_pairs["ANYCAST_GW_MAC"]

    @anycast_gw_mac.setter
    def anycast_gw_mac(self, param):
        self._nv_pairs["ANYCAST_GW_MAC"] = param

    @property
    def bgp_rp_asn(self):
        """
        return the current nv_pairs value of BGP_RP_ASN

        bgp_rp_asn must be a python list() of asn numbers conforming to:

            1-4294967295 | 1-65535[.0-65535]

        For example:

            [65001, "65001.54000", "65001.0", 4294967295]
        """
        return self._nv_pairs["BGP_RP_ASN"]

    @bgp_rp_asn.setter
    def bgp_rp_asn(self, param):
        try:
            self.validations.verify_bgp_rp_asn_list(param)
        except (ValueError, TypeError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["BGP_RP_ASN"] = param

    @property
    def bgw_routing_tag(self):
        """
        return the current nv_pairs value of BGW_ROUTING_TAG
        """
        return self._nv_pairs["BGW_ROUTING_TAG"]

    @bgw_routing_tag.setter
    def bgw_routing_tag(self, param):
        self._nv_pairs["BGW_ROUTING_TAG"] = param

    @property
    def bgw_routing_tag_prev(self):
        """
        return the current nv_pairs value of BGW_ROUTING_TAG_PREV
        """
        return self._nv_pairs["BGW_ROUTING_TAG_PREV"]

    @bgw_routing_tag_prev.setter
    def bgw_routing_tag_prev(self, param):
        self._nv_pairs["BGW_ROUTING_TAG_PREV"] = param

    @property
    def border_gwy_connections(self):
        """
        return the current nv_pairs value of BORDER_GWY_CONNECTIONS

        Valid values are:
        - Manual
        - Centralized_To_Route_Server
        - Back_To_Back_BGWS
        """
        return self._nv_pairs["BORDER_GWY_CONNECTIONS"]

    @border_gwy_connections.setter
    def border_gwy_connections(self, param):
        try:
            self.validations.verify_border_gwy_connections(param)
        except ValueError as err:
            msg = f"exiting {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["BORDER_GWY_CONNECTIONS"] = param

    @property
    def cloudsec_autoconfig(self):
        """
        return the current nv_pairs value of CLOUDSEC_AUTOCONFIG
        """
        return self._nv_pairs["CLOUDSEC_AUTOCONFIG"]

    @cloudsec_autoconfig.setter
    def cloudsec_autoconfig(self, param):
        self._nv_pairs["CLOUDSEC_AUTOCONFIG"] = param

    @property
    def cloudsec_key_string(self):
        """
        return the current nv_pairs value of CLOUDSEC_KEY_STRING
        """
        return self._nv_pairs["CLOUDSEC_KEY_STRING"]

    @cloudsec_key_string.setter
    def cloudsec_key_string(self, param):
        self._nv_pairs["CLOUDSEC_KEY_STRING"] = param

    @property
    def cloudsec_algorithm(self):
        """
        return the current nv_pairs value of CLOUDSEC_ALGORITHM
        """
        return self._nv_pairs["CLOUDSEC_ALGORITHM"]

    @cloudsec_algorithm.setter
    def cloudsec_algorithm(self, param):
        self._nv_pairs["CLOUDSEC_ALGORITHM"] = param

    @property
    def cloudsec_enforcement(self):
        """
        return the current nv_pairs value of CLOUDSEC_ENFORCEMENT
        """
        return self._nv_pairs["CLOUDSEC_ENFORCEMENT"]

    @cloudsec_enforcement.setter
    def cloudsec_enforcement(self, param):
        self._nv_pairs["CLOUDSEC_ENFORCEMENT"] = param

    @property
    def cloudsec_report_timer(self):
        """
        return the current nv_pairs value of CLOUDSEC_REPORT_TIMER
        """
        return self._nv_pairs["CLOUDSEC_REPORT_TIMER"]

    @cloudsec_report_timer.setter
    def cloudsec_report_timer(self, param):
        self._nv_pairs["CLOUDSEC_REPORT_TIMER"] = param

    @property
    def dci_subnet_range(self):
        """
        return the current nv_pairs value of DCI_SUBNET_RANGE
        """
        return self._nv_pairs["DCI_SUBNET_RANGE"]

    @dci_subnet_range.setter
    def dci_subnet_range(self, param):
        self._nv_pairs["DCI_SUBNET_RANGE"] = param

    @property
    def dci_subnet_target_mask(self):
        """
        return the current nv_pairs value of DCI_SUBNET_TARGET_MASK
        """
        return self._nv_pairs["DCI_SUBNET_TARGET_MASK"]

    @dci_subnet_target_mask.setter
    def dci_subnet_target_mask(self, param):
        self._nv_pairs["DCI_SUBNET_TARGET_MASK"] = param

    @property
    def dcnm_id(self):
        """
        return the current nv_pairs value of DCNM_ID
        """
        return self._nv_pairs["DCNM_ID"]

    @dcnm_id.setter
    def dcnm_id(self, param):
        self._nv_pairs["DCNM_ID"] = param

    @property
    def delay_restore(self):
        """
        return the current nv_pairs value of DELAY_RESTORE
        """
        return self._nv_pairs["DELAY_RESTORE"]

    @delay_restore.setter
    def delay_restore(self, param):
        self._nv_pairs["DELAY_RESTORE"] = param

    @property
    def enable_bgp_bfd(self):
        """
        return the current nv_pairs value of ENABLE_BGP_BFD
        """
        return self._nv_pairs["ENABLE_BGP_BFD"]

    @enable_bgp_bfd.setter
    def enable_bgp_bfd(self, param):
        self._nv_pairs["ENABLE_BGP_BFD"] = param

    @property
    def enable_bgp_log_neighbor_change(self):
        """
        return the current nv_pairs value of ENABLE_BGP_LOG_NEIGHBOR_CHANGE
        """
        return self._nv_pairs["ENABLE_BGP_LOG_NEIGHBOR_CHANGE"]

    @enable_bgp_log_neighbor_change.setter
    def enable_bgp_log_neighbor_change(self, param):
        self._nv_pairs["ENABLE_BGP_LOG_NEIGHBOR_CHANGE"] = param

    @property
    def enable_bgp_send_comm(self):
        """
        return the current nv_pairs value of ENABLE_BGP_SEND_COMM
        """
        return self._nv_pairs["ENABLE_BGP_SEND_COMM"]

    @enable_bgp_send_comm.setter
    def enable_bgp_send_comm(self, param):
        self._nv_pairs["ENABLE_BGP_SEND_COMM"] = param

    @property
    def enable_pvlan(self):
        """
        return the current nv_pairs value of ENABLE_PVLAN
        """
        return self._nv_pairs["ENABLE_PVLAN"]

    @enable_pvlan.setter
    def enable_pvlan(self, param):
        self._nv_pairs["ENABLE_PVLAN"] = param

    @property
    def enable_pvlan_prev(self):
        """
        return the current nv_pairs value of ENABLE_PVLAN_PREV
        """
        return self._nv_pairs["ENABLE_PVLAN_PREV"]

    @enable_pvlan_prev.setter
    def enable_pvlan_prev(self, param):
        self._nv_pairs["ENABLE_PVLAN_PREV"] = param

    @property
    def enable_rs_redist_direct(self):
        """
        return the current nv_pairs value of ENABLE_RS_REDIST_DIRECT
        """
        return self._nv_pairs["ENABLE_RS_REDIST_DIRECT"]

    @enable_rs_redist_direct.setter
    def enable_rs_redist_direct(self, param):
        self._nv_pairs["ENABLE_RS_REDIST_DIRECT"] = param

    # fabric_name (see top-level properties for fabric_name property)

    @property
    def fabric_type(self):
        """
        return the current nv_pairs value of FABRIC_TYPE
        """
        return self._nv_pairs["FABRIC_TYPE"]

    @fabric_type.setter
    def fabric_type(self, param):
        self._nv_pairs["FABRIC_TYPE"] = param

    @property
    def ff(self):  # pylint: disable=invalid-name
        """
        return the current nv_pairs value of FF
        """
        return self._nv_pairs["FF"]

    @ff.setter
    def ff(self, param):  # pylint: disable=invalid-name
        self._nv_pairs["FF"] = param

    @property
    def l2_segment_id_range(self):
        """
        return the current nv_pairs value of L2_SEGMENT_ID_RANGE
        """
        return self._nv_pairs["L2_SEGMENT_ID_RANGE"]

    @l2_segment_id_range.setter
    def l2_segment_id_range(self, param):
        self._nv_pairs["L2_SEGMENT_ID_RANGE"] = param

    @property
    def l3_partition_id_range(self):
        """
        return the current nv_pairs value of L3_PARTITION_ID_RANGE
        """
        return self._nv_pairs["L3_PARTITION_ID_RANGE"]

    @l3_partition_id_range.setter
    def l3_partition_id_range(self, param):
        self._nv_pairs["L3_PARTITION_ID_RANGE"] = param

    @property
    def loopback100_ip_range(self):
        """
        return the current nv_pairs value of LOOPBACK100_IP_RANGE
        """
        return self._nv_pairs["LOOPBACK100_IP_RANGE"]

    @loopback100_ip_range.setter
    def loopback100_ip_range(self, param):
        self._nv_pairs["LOOPBACK100_IP_RANGE"] = param

    @property
    def mso_controller_id(self):
        """
        return the current nv_pairs value of MSO_CONTROLER_ID
        NOTE: "CONTROLER" is misspelled internally within NDFC.
        We corrected the user-facing property spelling because
        we are OCD in that way.
        """
        return self._nv_pairs["MSO_CONTROLER_ID"]

    @mso_controller_id.setter
    def mso_controller_id(self, param):
        self._nv_pairs["MSO_CONTROLER_ID"] = param

    @property
    def mso_site_group_name(self):
        """
        return the current nv_pairs value of MSO_SITE_GROUP_NAME
        """
        return self._nv_pairs["MSO_SITE_GROUP_NAME"]

    @mso_site_group_name.setter
    def mso_site_group_name(self, param):
        self._nv_pairs["MSO_SITE_GROUP_NAME"] = param

    @property
    def ms_loopback_id(self):
        """
        return the current nv_pairs value of MS_LOOPBACK_ID
        """
        return self._nv_pairs["MS_LOOPBACK_ID"]

    @ms_loopback_id.setter
    def ms_loopback_id(self, param):
        self._nv_pairs["MS_LOOPBACK_ID"] = param

    @property
    def ms_ifc_bgp_auth_key_type(self):
        """
        return the current nv_pairs value of MS_IFC_BGP_AUTH_KEY_TYPE
        """
        return self._nv_pairs["MS_IFC_BGP_AUTH_KEY_TYPE"]

    @ms_ifc_bgp_auth_key_type.setter
    def ms_ifc_bgp_auth_key_type(self, param):
        self._nv_pairs["MS_IFC_BGP_AUTH_KEY_TYPE"] = param

    @property
    def ms_ifc_bgp_auth_key_type_prev(self):
        """
        return the current nv_pairs value of MS_IFC_BGP_AUTH_KEY_TYPE_PREV
        """
        return self._nv_pairs["MS_IFC_BGP_AUTH_KEY_TYPE_PREV"]

    @ms_ifc_bgp_auth_key_type_prev.setter
    def ms_ifc_bgp_auth_key_type_prev(self, param):
        self._nv_pairs["MS_IFC_BGP_AUTH_KEY_TYPE_PREV"] = param

    @property
    def ms_ifc_bgp_password(self):
        """
        return the current nv_pairs value of MS_IFC_BGP_PASSWORD
        """
        return self._nv_pairs["MS_IFC_BGP_PASSWORD"]

    @ms_ifc_bgp_password.setter
    def ms_ifc_bgp_password(self, param):
        self._nv_pairs["MS_IFC_BGP_PASSWORD"] = param

    @property
    def ms_ifc_bgp_password_prev(self):
        """
        return the current nv_pairs value of MS_IFC_BGP_PASSWORD_PREV
        """
        return self._nv_pairs["MS_IFC_BGP_PASSWORD_PREV"]

    @ms_ifc_bgp_password_prev.setter
    def ms_ifc_bgp_password_prev(self, param):
        self._nv_pairs["MS_IFC_BGP_PASSWORD_PREV"] = param

    @property
    def ms_ifc_bgp_password_enable(self):
        """
        return the current nv_pairs value of MS_IFC_BGP_PASSWORD_ENABLE
        """
        return self._nv_pairs["MS_IFC_BGP_PASSWORD_ENABLE"]

    @ms_ifc_bgp_password_enable.setter
    def ms_ifc_bgp_password_enable(self, param):
        self._nv_pairs["MS_IFC_BGP_PASSWORD_ENABLE"] = param

    @property
    def ms_ifc_bgp_password_enable_prev(self):
        """
        return the current nv_pairs value of MS_IFC_BGP_PASSWORD_ENABLE_PREV
        """
        return self._nv_pairs["MS_IFC_BGP_PASSWORD_ENABLE_PREV"]

    @ms_ifc_bgp_password_enable_prev.setter
    def ms_ifc_bgp_password_enable_prev(self, param):
        self._nv_pairs["MS_IFC_BGP_PASSWORD_ENABLE_PREV"] = param

    @property
    def ms_underlay_autoconfig(self):
        """
        return the current nv_pairs value of MS_UNDERLAY_AUTOCONFIG
        """
        return self._nv_pairs["MS_UNDERLAY_AUTOCONFIG"]

    @ms_underlay_autoconfig.setter
    def ms_underlay_autoconfig(self, param):
        self._nv_pairs["MS_UNDERLAY_AUTOCONFIG"] = param

    @property
    def premso_parent_fabric(self):
        """
        return the current nv_pairs value of PREMSO_PARENT_FABRIC
        """
        return self._nv_pairs["PREMSO_PARENT_FABRIC"]

    @premso_parent_fabric.setter
    def premso_parent_fabric(self, param):
        self._nv_pairs["PREMSO_PARENT_FABRIC"] = param

    @property
    def rp_server_ip(self):
        """
        return the current nv_pairs value of RP_SERVER_IP

        rp_server_ip must be a python list() of ip addresses e.g.
        ["1.1.1.1", "192.168.1.3"]
        """
        return self._nv_pairs["RP_SERVER_IP"]

    @rp_server_ip.setter
    def rp_server_ip(self, param):
        try:
            self.validations.verify_rp_server_ip_list(param)
        except (AddressValueError, TypeError) as err:
            msg = f"exiting {err}"
            self.logger.error(msg)
            sys.exit(1)
        self._nv_pairs["RP_SERVER_IP"] = param

    @property
    def rs_routing_tag(self):
        """
        return the current nv_pairs value of RS_ROUTING_TAG
        """
        return self._nv_pairs["RS_ROUTING_TAG"]

    @rs_routing_tag.setter
    def rs_routing_tag(self, param):
        self._nv_pairs["RS_ROUTING_TAG"] = param

    @property
    def tor_auto_deploy(self):
        """
        return the current nv_pairs value of TOR_AUTO_DEPLOY
        """
        return self._nv_pairs["TOR_AUTO_DEPLOY"]

    @tor_auto_deploy.setter
    def tor_auto_deploy(self, param):
        self._nv_pairs["TOR_AUTO_DEPLOY"] = param
