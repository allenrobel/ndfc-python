"""
Name: ndfc_vrf.py
Description: Create VRFs
"""

import inspect
import json
import logging
from ipaddress import AddressValueError

from ndfc_python.ndfc import NdfcRequestError
from ndfc_python.validations import Validations


class NdfcVrf:
    """
    Create VRFs
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.validations = Validations()

        # properties not passed to NDFC
        # order is important for these three
        self._internal_properties = {}
        self._init_internal_properties()

        # post/get base headers
        self._headers = {}
        self._headers["Content-Type"] = "application/json"

        self._payload_set = set()
        self._payload_set.add("display_name")
        self._payload_set.add("fabric")
        self._payload_set.add("serviceVrfTemplate")
        self._payload_set.add("source")
        self._payload_set.add("vrfExtensionTemplate")
        self._payload_set.add("vrfId")
        self._payload_set.add("vrfName")
        self._payload_set.add("vrfTemplate")

        self.mandatory_payload_set = set()
        self.mandatory_payload_set.add("fabric")
        self.mandatory_payload_set.add("vrfId")
        self.mandatory_payload_set.add("vrfName")

        self.mandatory_template_config_set = set()
        self.mandatory_template_config_set.add("vrfVlanId")

        self.payload_default = {}
        value = "Default_VRF_Extension_Universal"
        self.payload_default["vrfExtensionTemplate"] = value
        self.payload_default["vrfTemplate"] = "Default_VRF_Universal"

        self.template_config_set = set()
        self.template_config_set.add("advertiseHostRouteFlag")
        self.template_config_set.add("advertiseDefaultRouteFlag")
        self.template_config_set.add("bgpPassword")
        self.template_config_set.add("bgpPasswordKeyType")
        self.template_config_set.add("configureStaticDefaultRouteFlag")
        self.template_config_set.add("ENABLE_NETFLOW")
        self.template_config_set.add("ipv6LinkLocalFlag")
        self.template_config_set.add("isRPExternal")
        self.template_config_set.add("loopbackNumber")
        self.template_config_set.add("L3VniMcastGroup")
        self.template_config_set.add("maxBgpPaths")
        self.template_config_set.add("maxIbgpPaths")
        self.template_config_set.add("multicastGroup")
        self.template_config_set.add("mtu")
        self.template_config_set.add("NETFLOW_MONITOR")
        self.template_config_set.add("nveId")
        self.template_config_set.add("rpAddress")
        self.template_config_set.add("tag")
        self.template_config_set.add("trmEnabled")
        self.template_config_set.add("trmBGWMSiteEnabled")
        self.template_config_set.add("vrfName")
        self.template_config_set.add("vrfDescription")
        self.template_config_set.add("vrfIntfDescription")
        self.template_config_set.add("vrfRouteMap")
        self.template_config_set.add("vrfSegmentId")
        self.template_config_set.add("vrfVlanId")
        self.template_config_set.add("vrfVlanName")

        self.template_config_default = {}
        self.template_config_default["advertiseDefaultRouteFlag"] = True
        self.template_config_default["advertiseHostRouteFlag"] = False
        self.template_config_default["bgpPasswordKeyType"] = 3
        self.template_config_default["configureStaticDefaultRouteFlag"] = True
        self.template_config_default["ENABLE_NETFLOW"] = False
        self.template_config_default["ipv6LinkLocalFlag"] = True
        self.template_config_default["isRPExternal"] = False
        self.template_config_default["mtu"] = 9216
        self.template_config_default["nveId"] = 1
        self.template_config_default["tag"] = "12345"
        value = "FABRIC-RMAP-REDIST-SUBNET"
        self.template_config_default["vrfRouteMap"] = value
        self.template_config_default["maxBgpPaths"] = "1"
        self.template_config_default["maxIbgpPaths"] = "2"
        self.template_config_default["trmEnabled"] = False
        self.template_config_default["trmBGWMSiteEnabled"] = False

        self._init_payload()
        self._init_vrf_template_config()

    def _init_internal_properties(self):
        self._internal_properties["ndfc"] = None

    def _init_payload(self):
        """
        initialize the REST payload
        """
        self.payload = {}
        for param in self._payload_set:
            if param in self.payload_default:
                self.payload[param] = self.payload_default[param]
            else:
                self.payload[param] = ""

    def _init_vrf_template_config(self):
        """
        initialize the vrf template_config
        """
        self.template_config = {}
        for param in self.template_config_set:
            if param in self.template_config_default:
                value = self.template_config_default[param]
                self.template_config[param] = value
            else:
                self.template_config[param] = ""

    def _preprocess_payload(self):
        """
        NOT USED CURRENTLY
        1. Set a default value for any properties that the caller has not set
        and that NDFC provides a default for.

        2. Copy top-level property values (that need it) into their respective
        template_config properties.
        """
        if self.payload["display_name"] == "":
            self.payload["display_name"] = self.vrf_name

        self.template_config["vrfName"] = self.vrf_name
        self.template_config["vrfSegmentId"] = self.vrf_id

    def _final_verification(self):
        """
        verify the following:

        - ndfc is set and is an NDFC instance
        - all mandatory parameters are set
        - self.vrf does not already exist in self.fabric
        """
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ndfc(self.ndfc)
        except (AttributeError, TypeError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        for param in self.mandatory_payload_set:
            if self.payload[param] == "":
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Call {self.class_name}.{param} before calling "
                msg += f"{self.class_name}.post()"
                raise ValueError(msg)
        for param in self.mandatory_template_config_set:
            if self.template_config[param] == "":
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Call {self.class_name}.{param} before calling "
                msg += f"{self.class_name}.post()"
                raise ValueError(msg)
        if self.vrf_exists_in_fabric():
            msg = f"{self.class_name}.{method_name}: "
            msg += f"VRF {self.vrf_name} already exists in "
            msg += f"fabric {self.fabric}"
            raise ValueError(msg)

    def post(self):
        """
        post the resquest
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        url = f"{self.ndfc.url_top_down_fabrics}/{self.fabric}/vrfs"

        headers = {}
        headers["Authorization"] = self.ndfc.bearer_token
        headers["Content-Type"] = "application/json"

        self.payload["vrfTemplateConfig"] = json.dumps(self.template_config)

        try:
            self.ndfc.post(url, headers, self.payload)
        except NdfcRequestError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error sending POST request to the controller. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

    def vrf_exists_in_fabric(self):
        """
        Return True if self.vrf exists in self.fabric.
        Else, return False
        """
        url = f"{self.ndfc.url_top_down_fabrics}/{self.fabric}/vrfs"

        self._headers["Authorization"] = self.ndfc.bearer_token

        response = self.ndfc.get(url, self._headers)
        for item_d in response:
            if "fabric" not in item_d:
                continue
            if "vrfName" not in item_d:
                continue
            if item_d["fabric"] != self.fabric:
                continue
            if item_d["vrfName"] != self.vrf_name:
                continue
            return True
        return False

    # properties that are not passed to NDFC
    @property
    def ndfc(self):
        """
        return/set the current ndfc instance
        """
        return self._internal_properties["ndfc"]

    @ndfc.setter
    def ndfc(self, param):
        self._internal_properties["ndfc"] = param

    # top_level properties
    @property
    def display_name(self):
        """
        return the current payload value of VRF display name
        """
        return self.payload["displayName"]

    @display_name.setter
    def display_name(self, param):
        self.payload["displayName"] = param

    @property
    def fabric(self):
        """
        return the current payload value of VRF fabric
        """
        return self.payload["fabric"]

    @fabric.setter
    def fabric(self, param):
        self.payload["fabric"] = param

    @property
    def vrf_extension_template(self):
        """
        return the current payload value of vrf_extension_template
        """
        return self.payload["vrfExtensionTemplate"]

    @vrf_extension_template.setter
    def vrf_extension_template(self, param):
        self.payload["vrfExtensionTemplate"] = param

    @property
    def vrf_id(self):
        """
        return the current payload value of vrf_id
        """
        return self.payload["vrfId"]

    @vrf_id.setter
    def vrf_id(self, param):
        self.payload["vrfId"] = param

    @property
    def vrf_name(self):
        """
        return the current payload value of vrf_name
        """
        return self.payload["vrfName"]

    @vrf_name.setter
    def vrf_name(self, param):
        self.payload["vrfName"] = param

    @property
    def vrf_template(self):
        """
        return the current payload value of vrf_template
        """
        return self.payload["vrfTemplate"]

    @vrf_template.setter
    def vrf_template(self, param):
        self.payload["vrfTemplate"] = param

    @property
    def service_vrf_template(self):
        """
        return the current payload value of service_vrf_template
        """
        return self.payload["serviceVrfTemplate"]

    @service_vrf_template.setter
    def service_vrf_template(self, param):
        self.payload["serviceVrfTemplate"] = param

    @property
    def source(self):
        """
        return the current payload value of source
        """
        return self.payload["source"]

    @source.setter
    def source(self, param):
        self.payload["source"] = param

    # vrf_template_config properties

    @property
    def advertise_host_route_flag(self):
        """
        return the current template_config value of advertise_host_route_flag
        """
        return self.template_config["advertiseHostRouteFlag"]

    @advertise_host_route_flag.setter
    def advertise_host_route_flag(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(param)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["advertiseHostRouteFlag"] = param

    @property
    def advertise_default_route_flag(self):
        """
        return the current template_config value of
        advertise_default_route_flag
        """
        return self.template_config["advertiseDefaultRouteFlag"]

    @advertise_default_route_flag.setter
    def advertise_default_route_flag(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(param)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["advertiseDefaultRouteFlag"] = param

    @property
    def bgp_password(self):
        """
        return the current template_config value of bgp_password
        """
        return self.template_config["bgpPassword"]

    @bgp_password.setter
    def bgp_password(self, param):
        self.template_config["bgpPassword"] = param

    @property
    def bgp_password_key_type(self):
        """
        return the current template_config value of bgp_password_key_type
        """
        return self.template_config["bgpPasswordKeyType"]

    @bgp_password_key_type.setter
    def bgp_password_key_type(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_bgp_password_key_type(param)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["bgpPasswordKeyType"] = param

    @property
    def configure_static_default_route_flag(self):
        """
        return the current template_config value of
        configure_static_default_route_flag
        """
        return self.template_config["configureStaticDefaultRouteFlag"]

    @configure_static_default_route_flag.setter
    def configure_static_default_route_flag(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(param)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["configureStaticDefaultRouteFlag"] = param

    @property
    def enable_netflow(self):
        """
        return the current template_config value of enable_netflow
        """
        return self.template_config["ENABLE_NETFLOW"]

    @enable_netflow.setter
    def enable_netflow(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(param)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["ENABLE_NETFLOW"] = param

    @property
    def ipv6_link_local_flag(self):
        """
        return the current template_config value of ipv6_link_local_flag
        """
        return self.template_config["ipv6LinkLocalFlag"]

    @ipv6_link_local_flag.setter
    def ipv6_link_local_flag(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(param)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["ipv6LinkLocalFlag"] = param

    @property
    def is_rp_external(self):
        """
        return the current template_config value of is_rp_external
        """
        return self.template_config["isRPExternal"]

    @is_rp_external.setter
    def is_rp_external(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(param)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["isRPExternal"] = param

    @property
    def l3_vni_mcast_group(self):
        """
        return the current template_config value of l3_vni_mcast_group
        """
        return self.template_config["L3VniMcastGroup"]

    @l3_vni_mcast_group.setter
    def l3_vni_mcast_group(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_multicast_address(param)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["L3VniMcastGroup"] = param

    @property
    def loopback_number(self):
        """
        return the current template_config value of loopback_number
        """
        return self.template_config["loopbackNumber"]

    @loopback_number.setter
    def loopback_number(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_loopback_id(param)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["loopbackNumber"] = param

    @property
    def max_bgp_paths(self):
        """
        return the current template_config value of max_bgp_paths
        """
        return self.template_config["maxBgpPaths"]

    @max_bgp_paths.setter
    def max_bgp_paths(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_max_bgp_paths(param)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["maxBgpPaths"] = param

    @property
    def max_ibgp_paths(self):
        """
        return the current template_config value of max_ibgp_paths
        """
        return self.template_config["maxIbgpPaths"]

    @max_ibgp_paths.setter
    def max_ibgp_paths(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_max_bgp_paths(param)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["maxIbgpPaths"] = param

    @property
    def multicast_group(self):
        """
        return the current template_config value of multicast_group
        """
        return self.template_config["multicastGroup"]

    @multicast_group.setter
    def multicast_group(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_multicast_address(param)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["multicastGroup"] = param

    @property
    def mtu(self):
        """
        return the current template_config value of mtu
        """
        return self.template_config["mtu"]

    @mtu.setter
    def mtu(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_mtu(param)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["mtu"] = param

    @property
    def netflow_monitor(self):
        """
        return the current template_config value of netflow_monitor
        """
        return self.template_config["NETFLOW_MONITOR"]

    @netflow_monitor.setter
    def netflow_monitor(self, param):
        self.template_config["NETFLOW_MONITOR"] = param

    @property
    def nve_id(self):
        """
        return the current template_config value of nve_id
        """
        return self.template_config["nveId"]

    @nve_id.setter
    def nve_id(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_nve_id(param)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["nveId"] = param

    @property
    def rp_address(self):
        """
        return the current template_config value of rp_address
        """
        return self.template_config["rpAddress"]

    @rp_address.setter
    def rp_address(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_address(param)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["rpAddress"] = param

    @property
    def tag(self):
        """
        return the current template_config value of tag
        """
        return self.template_config["tag"]

    @tag.setter
    def tag(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_routing_tag(param)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["tag"] = param

    @property
    def trm_bgw_msite_enabled(self):
        """
        return the current template_config value of trm_bgw_msite_enabled
        """
        return self.template_config["trmBGWMSiteEnabled"]

    @trm_bgw_msite_enabled.setter
    def trm_bgw_msite_enabled(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(param)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["trmBGWMSiteEnabled"] = param

    @property
    def trm_enabled(self):
        """
        return the current template_config value of trm_enabled
        """
        return self.template_config["trmEnabled"]

    @trm_enabled.setter
    def trm_enabled(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(param)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["trmEnabled"] = param

    @property
    def vrf_description(self):
        """
        return the current template_config value of vrf_description
        """
        return self.template_config["vrfDescription"]

    @vrf_description.setter
    def vrf_description(self, param):
        self.template_config["vrfDescription"] = param

    @property
    def vrf_intf_description(self):
        """
        return the current template_config value of vrf_intf_description
        """
        return self.template_config["vrfIntfDescription"]

    @vrf_intf_description.setter
    def vrf_intf_description(self, param):
        self.template_config["vrfIntfDescription"] = param

    @property
    def vrf_route_map(self):
        """
        return the current template_config value of vrf_route_map
        """
        return self.template_config["vrfRouteMap"]

    @vrf_route_map.setter
    def vrf_route_map(self, param):
        self.template_config["vrfRouteMap"] = param

    @property
    def vrf_vlan_id(self):
        """
        return the current template_config value of vrf_vlan_id
        """
        return self.template_config["vrfVlanId"]

    @vrf_vlan_id.setter
    def vrf_vlan_id(self, param):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_vrf_vlan_id(param)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["vrfVlanId"] = param

    @property
    def vrf_vlan_name(self):
        """
        return the current template_config value of vrf_vlan_name
        """
        return self.template_config["vrfVlanName"]

    @vrf_vlan_name.setter
    def vrf_vlan_name(self, param):
        self.template_config["vrfVlanName"] = param
