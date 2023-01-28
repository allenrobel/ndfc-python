"""
Create / delete networks  The JSON payload constructed by this class is shown below.

network = {'displayName': 'MyNetwork_30000',
 'fabric': 'My_VxLAN_Fabric',
 'networkExtensionTemplate': 'Default_Network_Extension_Universal',
 'networkId': '30000',
 'networkName': 'MyNetwork_30000',
 'networkTemplate': 'Default_Network_Universal',
 'networkTemplateConfig': {'dhcpServerAddr1': '',
                           'dhcpServerAddr2': '',
                           'dhcpServerAddr3': '',
                           'enableIR': False,
                           'enableL3OnBorder': True,
                           'gatewayIpAddress': '10.1.1.1/24',
                           'gatewayIpV6Address': '',
                           'intfDescription': '',
                           'isLayer2Only': False,
                           'loopbackId': '',
                           'mcastGroup': '',
                           'mtu': '9216',
                           'networkName': 'MyNetwork_30000',
                           'nveId': 1,
                           'rtBothAuto': True,
                           'secondaryGW1': '',
                           'secondaryGW2': '',
                           'secondaryGW3': '',
                           'secondaryGW4': '',
                           'segmentId': '30000',
                           'suppressArp': True,
                           'tag': '12345',
                           'trmEnabled': False,
                           'vlanId': '',
                           'vlanName': '',
                           'vrfDhcp': '',
                           'vrfDhcp2': '',
                           'vrfDhcp3': '',
                           'vrfName': 'Customer-001'},
 'serviceNetworkTemplate': None,
 'source': None,
 'vrf': 'Customer-001'}
"""
from inspect import stack
import json
import sys

OUR_VERSION = 101


class NdfcNetwork:
    """
    create / delete networks

    Example create operation:

    instance = NdfcNetwork(ndfc)
    instance.fabric = 'foo'
    instance.network_id = 30000
    instance.vlan_id = 3000
    instance.vrf = 'foo_vrf'
    instance.create()

    Example delete operation:

    instance = NdfcNetwork(ndfc)
    instance.fabric = 'foo'
    instance.network_name = 'MyNetwork_30000'
    instance.delete()

    """

    def __init__(self, ndfc):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        # post/get base headers
        self._headers = {}
        self._headers["Content-Type"] = "application/json"

        self._init_payload_set()
        self._init_payload_set_mandatory()
        self._init_payload_default()
        self._init_template_config_set()
        self._init_template_config_default()
        self._init_template_config_set_mandatory()
        self._init_payload()
        self._init_template_config()
        self._init_payload_mapping_dict()
        self._init_template_config_mapping_dict()

    def log(self, *args):
        """
        simple logger
        """
        print(
            f"{self.class_name}(v{self.lib_version}).{stack()[1].function}: {' '.join(args)}"
        )

    def _init_payload_set(self):
        self._payload_set = set()
        self._payload_set.add("displayName")
        self._payload_set.add("fabric")
        self._payload_set.add("networkExtensionTemplate")
        self._payload_set.add("networkId")
        self._payload_set.add("networkName")
        self._payload_set.add("networkTemplate")
        self._payload_set.add("serviceNetworkTemplate")
        self._payload_set.add("source")
        self._payload_set.add("vrf")

    def _init_payload_set_mandatory(self):
        self._payload_set_mandatory = set()
        self._payload_set_mandatory.add("fabric")
        self._payload_set_mandatory.add("networkId")
        self._payload_set_mandatory.add("vrf")

    def _init_payload_default(self):
        self._payload_default = {}
        self._payload_default[
            "networkExtensionTemplate"
        ] = "Default_Network_Extension_Universal"
        self._payload_default["networkTemplate"] = "Default_Network_Universal"

    def _init_template_config_set(self):
        self._template_config_set = set()
        self._template_config_set.add("dhcpServerAddr1")
        self._template_config_set.add("dhcpServerAddr2")
        self._template_config_set.add("dhcpServerAddr3")
        self._template_config_set.add("enableIR")
        self._template_config_set.add("enableL3OnBorder")
        self._template_config_set.add("gatewayIpAddress")
        self._template_config_set.add("gatewayIpV6Address")
        self._template_config_set.add("intfDescription")
        self._template_config_set.add("isLayer2Only")
        self._template_config_set.add("loopbackId")
        self._template_config_set.add("mcastGroup")
        self._template_config_set.add("mtu")
        self._template_config_set.add("networkName")
        self._template_config_set.add("nveId")
        self._template_config_set.add("rtBothAuto")
        self._template_config_set.add("secondaryGW1")
        self._template_config_set.add("secondaryGW2")
        self._template_config_set.add("secondaryGW3")
        self._template_config_set.add("secondaryGW4")
        self._template_config_set.add("segmentId")
        self._template_config_set.add("suppressArp")
        self._template_config_set.add("tag")
        self._template_config_set.add("trmEnabled")
        self._template_config_set.add("vlanId")
        self._template_config_set.add("vlanName")
        self._template_config_set.add("vrfDhcp")
        self._template_config_set.add("vrfDhcp2")
        self._template_config_set.add("vrfDhcp3")
        self._template_config_set.add("vrfName")

    def _init_template_config_default(self):
        self._template_config_default = {}
        self._template_config_default["enableIR"] = True
        self._template_config_default["enableL3OnBorder"] = False
        self._template_config_default["isLayer2Only"] = False
        self._template_config_default["mtu"] = 9216
        self._template_config_default["nveId"] = 1
        self._template_config_default["rtBothAuto"] = False
        self._template_config_default["suppressArp"] = True
        self._template_config_default["tag"] = "12345"
        self._template_config_default["trmEnabled"] = False

    def _init_template_config_set_mandatory(self):
        self._template_config_set_mandatory = set()
        self._template_config_set_mandatory.add("vlanId")

    def _init_payload(self):
        self.payload = {}
        for param in self._payload_set:
            if param in self._payload_default:
                self.payload[param] = self._payload_default[param]
            else:
                self.payload[param] = ""

    def _init_template_config(self):
        self.template_config = {}
        for param in self._template_config_set:
            if param in self._template_config_default:
                self.template_config[param] = self._template_config_default[param]
            else:
                self.template_config[param] = ""

    def _preprocess_payload(self):
        """
        1. Set a default value for any properties that the caller
        has not set and that NDFC provides a default for.

        2. Copy top-level property values (that need it) into their
        respective template_config properties.

        3. Any other fixup that may be required
        """
        # if source is null, NDFC complains if it's present
        if self.source == "":
            self.payload.pop("source", None)
            self.ndfc.log.debug(
                "deleted null source key from payload to avoid ndfc complaints"
            )
        if self.network_name == "":
            self.network_name = f"MyNetwork_{self.network_id}"
            self.template_config["networkName"] = self.network_name
        if self.display_name == "":
            self.display_name = self.network_name
        self.template_config["vrfName"] = self.vrf
        if self.segment_id == "":
            self.segment_id = self.network_id

    def _init_payload_mapping_dict(self):
        """
        see _map_payload_param()
        """
        self._payload_mapping_dict = {}
        self._payload_mapping_dict["displayName"] = "display_name"
        self._payload_mapping_dict["fabric"] = "fabric"
        self._payload_mapping_dict[
            "networkExtensionTemplate"
        ] = "network_extension_template"
        self._payload_mapping_dict["networkId"] = "network_id"
        self._payload_mapping_dict["networkName"] = "network_name"
        self._payload_mapping_dict["networkTemplate"] = "network_template"
        self._payload_mapping_dict[
            "serviceNetworkTemplate"
        ] = "service_network_template"
        self._payload_mapping_dict["source"] = "source"
        self._payload_mapping_dict["vrf"] = "vrf"

    def _init_template_config_mapping_dict(self):
        """
        see _map_template_config_param()
        """
        self._template_config_mapping_dict = {}
        self._template_config_mapping_dict["dhcpServerAddr1"] = "dhcp_server_addr_1"
        self._template_config_mapping_dict["dhcpServerAddr2"] = "dhcp_server_addr_2"
        self._template_config_mapping_dict["dhcpServerAddr3"] = "dhcp_server_addr_3"
        self._template_config_mapping_dict["enableIR"] = "enable_ir"
        self._template_config_mapping_dict["enableL3OnBorder"] = "enable_l3_on_border"
        self._template_config_mapping_dict["gatewayIpAddress"] = "gateway_ip_address"
        self._template_config_mapping_dict[
            "gatewayIpV6Address"
        ] = "gateway_ipv6_address"
        self._template_config_mapping_dict["intfDescription"] = "intf_description"
        self._template_config_mapping_dict["isLayer2Only"] = "is_layer2_only"
        self._template_config_mapping_dict["loopbackId"] = "loopback_id"
        self._template_config_mapping_dict["mcastGroup"] = "mcast_group"
        self._template_config_mapping_dict["mtu"] = "mtu"
        self._template_config_mapping_dict["nveId"] = "nve_id"
        self._template_config_mapping_dict["rtBothAuto"] = "rt_both_auto"
        self._template_config_mapping_dict["secondaryGW1"] = "secondary_gw_1"
        self._template_config_mapping_dict["secondaryGW2"] = "secondary_gw_2"
        self._template_config_mapping_dict["secondaryGW3"] = "secondary_gw_3"
        self._template_config_mapping_dict["secondaryGW4"] = "secondary_gw_4"
        self._template_config_mapping_dict["segmentId"] = "segment_id"
        self._template_config_mapping_dict["suppressArp"] = "suppress_arp"
        self._template_config_mapping_dict["tag"] = "tag"
        self._template_config_mapping_dict["trmEnabled"] = "trm_enabled"
        self._template_config_mapping_dict["vlanId"] = "vlan_id"
        self._template_config_mapping_dict["vrfDhcp"] = "vrf_dhcp"
        self._template_config_mapping_dict["vrfDhcp2"] = "vrf_dhcp_2"
        self._template_config_mapping_dict["vrfDhcp3"] = "vrf_dhcp_3"

    def _map_payload_param(self, param):
        """
        Because payload keys are camel case, and pylint does
        not like camel case, we modified the corresponding
        properties to be snake case.  This method maps the
        camel case keys to their corresponding properties. It
        is used in _final_verification to provide the user with
        the correct property to call if there's a missing mandatory
        payload property.
        """
        if param not in self._payload_mapping_dict:
            self.log("WARNING: param {} not in _payload_mapping_dict")
            return param
        return self._payload_mapping_dict[param]

    def _map_template_config_param(self, param):
        """
        Because template_config keys are camel case, and pylint does
        not like camel case, we modified the corresponding
        properties to be snake case.  This method maps the
        camel case keys to their corresponding properties. It
        is used in _final_verification to provide the user with
        the correct property to call if there's a missing mandatory
        template_config property.
        """
        if param not in self._template_config_mapping_dict:
            self.log("WARNING: param {} not in _template_config_mapping_dict")
            return param
        return self._template_config_mapping_dict[param]

    def _final_verification(self):
        """
        final verification of all parameters
        """
        for param in self._payload_set_mandatory:
            if self.payload[param] == "":
                self.log(
                    f"Exiting. call instance.{self._map_payload_param(param)}",
                    "before calling instance.create()",
                )
                sys.exit(1)
        for param in self._template_config_set_mandatory:
            if self.template_config[param] == "":
                self.log(
                    f"Exiting. call instance.{self._map_template_config_param(param)}",
                    "before calling instance.create()",
                )
                sys.exit(1)

    def vrf_exists_in_fabric(self):
        """
        Return True if vrfName is present in the fabric
        Else, return False
        """
        url = f"{self.ndfc.url_top_down_fabrics}/{self.fabric}/vrfs"
        headers = self._headers
        headers["Authorization"] = self.ndfc.bearer_token

        response = self.ndfc.get(url, headers)
        for item_d in response:
            if "fabric" not in item_d:
                continue
            if "vrfName" not in item_d:
                continue
            if item_d["fabric"] != self.fabric:
                continue
            if item_d["vrfName"] != self.vrf:
                continue
            return True
        return False

    def network_id_exists_in_fabric(self):
        """
        Return True if networkId is present in the fabric
        Else, return False
        """
        url = f"{self.ndfc.url_top_down_fabrics}/{self.fabric}/networks"
        headers = self._headers
        headers["Authorization"] = self.ndfc.bearer_token

        response = self.ndfc.get(url, headers)
        for item_d in response:
            if "networkId" not in item_d:
                continue
            if item_d["networkId"] == self.network_id:
                return True
        return False

    def network_name_exists_in_fabric(self):
        """
        Return True if networkName exists in the fabric.
        Else return False
        """
        url = f"{self.ndfc.url_top_down_fabrics}/{self.fabric}/networks"

        headers = self._headers
        headers["Authorization"] = self.ndfc.bearer_token

        response = self.ndfc.get(url, headers)
        for item_d in response:
            if "networkName" not in item_d:
                continue
            if item_d["networkName"] == self.network_name:
                return True
        return False

    def create(self):
        """
        Create a network
        """
        self._preprocess_payload()
        self._final_verification()

        if self.vrf_exists_in_fabric() is False:
            self.log(
                f"Exiting. vrf {self.vrf} does not exist in fabric {self.fabric}.",
                "Create it before calling NdfcNetwork()",
            )
            sys.exit(1)

        if self.network_id_exists_in_fabric() is True:
            self.log(
                f"Exiting. networkId {self.network_id} already exists in fabric {self.fabric}.",
                "Delete it before calling NdfcNetwork.create()",
            )
            sys.exit(1)

        url = f"{self.ndfc.url_top_down_fabrics}/{self.fabric}/networks"
        headers = self._headers
        headers["Authorization"] = self.ndfc.bearer_token

        self.payload["networkTemplateConfig"] = json.dumps(self.template_config)

        self.ndfc.post(url, headers, self.payload)

    def delete(self):
        """
        Delete a network
        """
        if self.network_name == "":
            self.log(
                "Exiting. Call instance.networkName before calling NdfcNetworks.delete()"
            )
            sys.exit(1)
        if self.fabric == "":
            self.log(
                "Exiting. Call instance.fabric before calling NdfcNetworks.delete()"
            )
            sys.exit(1)

        headers = self._headers
        headers["Authorization"] = self.ndfc.bearer_token

        if self.network_name_exists_in_fabric() is False:
            self.log(
                f"Exiting. networkName {self.network_name} does not exist in fabric {self.fabric}."
            )
            sys.exit(1)

        url = f"{self.ndfc.url_top_down_fabrics}/{self.fabric}/networks/{self.network_name}"
        self.ndfc.delete(url, headers)

    # top_level properties
    @property
    def display_name(self):
        """
        return the current payload value of display_name
        """
        return self.payload["displayName"]

    @display_name.setter
    def display_name(self, param):
        self.payload["displayName"] = param

    @property
    def fabric(self):
        """
        return the current payload value of fabric
        """
        return self.payload["fabric"]

    @fabric.setter
    def fabric(self, param):
        self.payload["fabric"] = param

    @property
    def network_extension_template(self):
        """
        return the current payload value of network_extension_template
        """
        return self.payload["networkExtensionTemplate"]

    @network_extension_template.setter
    def network_extension_template(self, param):
        self.payload["networkExtensionTemplate"] = param

    @property
    def network_id(self):
        """
        return the current payload value of network_id
        """
        return self.payload["networkId"]

    @network_id.setter
    def network_id(self, param):
        self.payload["networkId"] = param

    @property
    def network_name(self):
        """
        return the current payload value of network_name
        """
        return self.payload["networkName"]

    @network_name.setter
    def network_name(self, param):
        self.payload["networkName"] = param

    @property
    def network_template(self):
        """
        return the current payload value of network_template
        """
        return self.payload["networkTemplate"]

    @network_template.setter
    def network_template(self, param):
        self.payload["networkTemplate"] = param

    @property
    def service_network_template(self):
        """
        return the current payload value of service_network_template
        """
        return self.payload["serviceNetworkTemplate"]

    @service_network_template.setter
    def service_network_template(self, param):
        self.payload["serviceNetworkTemplate"] = param

    @property
    def source(self):
        """
        return the current payload value of source
        """
        return self.payload["source"]

    @source.setter
    def source(self, param):
        self.payload["source"] = param

    @property
    def vrf(self):
        """
        return the current payload value of vrf
        """
        return self.payload["vrf"]

    @vrf.setter
    def vrf(self, param):
        self.payload["vrf"] = param

    # template_config properties
    @property
    def dhcp_server_addr_1(self):
        """
        return the current template_config value of dhcp_server_addr_1
        """
        return self.template_config["dhcpServerAddr1"]

    @dhcp_server_addr_1.setter
    def dhcp_server_addr_1(self, param):
        self.template_config["dhcpServerAddr1"] = param

    @property
    def dhcp_server_addr_2(self):
        """
        return the current template_config value of dhcp_server_addr_2
        """
        return self.template_config["dhcpServerAddr2"]

    @dhcp_server_addr_2.setter
    def dhcp_server_addr_2(self, param):
        self.template_config["dhcpServerAddr2"] = param

    @property
    def dhcp_server_addr_3(self):
        """
        return the current template_config value of dhcp_server_addr_3
        """
        return self.template_config["dhcpServerAddr3"]

    @dhcp_server_addr_3.setter
    def dhcp_server_addr_3(self, param):
        self.template_config["dhcpServerAddr3"] = param

    @property
    def enable_ir(self):
        """
        return the current template_config value of enable_ir
        """
        return self.template_config["enableIR"]

    @enable_ir.setter
    def enable_ir(self, param):
        self.ndfc.verify_boolean(param)
        self.template_config["enableIR"] = param

    @property
    def enable_l3_on_border(self):
        """
        return the current template_config value of enable_l3_on_border
        """
        return self.template_config["enableL3OnBorder"]

    @enable_l3_on_border.setter
    def enable_l3_on_border(self, param):
        self.ndfc.verify_boolean(param)
        self.template_config["enableL3OnBorder"] = param

    @property
    def gateway_ip_address(self):
        """
        return the current template_config value of gateway_ip_address
        """
        return self.template_config["gatewayIpAddress"]

    @gateway_ip_address.setter
    def gateway_ip_address(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self.template_config["gatewayIpAddress"] = param

    @property
    def gateway_ipv6_address(self):
        """
        return the current template_config value of gateway_ipv6_address
        """
        return self.template_config["gatewayIpV6Address"]

    @gateway_ipv6_address.setter
    def gateway_ipv6_address(self, param):
        self.ndfc.verify_ipv6_address_with_prefix(param)
        self.template_config["gatewayIpV6Address"] = param

    @property
    def intf_description(self):
        """
        return the current template_config value of intf_description
        """
        return self.template_config["intfDescription"]

    @intf_description.setter
    def intf_description(self, param):
        self.template_config["intfDescription"] = param

    @property
    def is_layer2_only(self):
        """
        return the current template_config value of is_layer2_only
        """
        return self.template_config["isLayer2Only"]

    @is_layer2_only.setter
    def is_layer2_only(self, param):
        self.ndfc.verify_boolean(param)
        self.template_config["isLayer2Only"] = param

    @property
    def loopback_id(self):
        """
        return the current template_config value of loopback_id
        """
        return self.template_config["loopbackId"]

    @loopback_id.setter
    def loopback_id(self, param):
        self.ndfc.verify_loopback_id(param)
        self.template_config["loopbackId"] = param

    @property
    def mcast_group(self):
        """
        return the current template_config value of mcast_group
        """
        return self.template_config["mcastGroup"]

    @mcast_group.setter
    def mcast_group(self, param):
        self.ndfc.verify_ipv4_multicast_address(
            param, f"{self.class_name}.mcast_group.setter"
        )
        self.template_config["mcastGroup"] = param

    @property
    def mtu(self):
        """
        return the current template_config value of mtu
        """
        return self.template_config["mtu"]

    @mtu.setter
    def mtu(self, param):
        self.ndfc.verify_mtu(param, f"{self.class_name}.mtu.setter")
        self.template_config["mtu"] = param

    # networkName (see property for self.payload['networkName])
    # We populate self.template_config['networkName'] from the value
    # in self.payload['networkName']

    @property
    def nve_id(self):
        """
        return the current template_config value of nve_id
        """
        return self.template_config["nveId"]

    @nve_id.setter
    def nve_id(self, param):
        self.ndfc.verify_nve_id(param, f"{self.class_name}.nve_id.setter")
        self.template_config["nveId"] = param

    @property
    def rt_both_auto(self):
        """
        return the current template_config value of rt_both_auto
        """
        return self.template_config["rtBothAuto"]

    @rt_both_auto.setter
    def rt_both_auto(self, param):
        self.ndfc.verify_boolean(param)
        self.template_config["rtBothAuto"] = param

    @property
    def secondary_gw_1(self):
        """
        return the current template_config value of secondary_gw_1
        """
        return self.template_config["secondaryGW1"]

    @secondary_gw_1.setter
    def secondary_gw_1(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self.template_config["secondaryGW1"] = param

    @property
    def secondary_gw_2(self):
        """
        return the current template_config value of secondary_gw_2
        """
        return self.template_config["secondaryGW2"]

    @secondary_gw_2.setter
    def secondary_gw_2(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self.template_config["secondaryGW2"] = param

    @property
    def secondary_gw_3(self):
        """
        return the current template_config value of secondary_gw_3
        """
        return self.template_config["secondaryGW3"]

    @secondary_gw_3.setter
    def secondary_gw_3(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self.template_config["secondaryGW3"] = param

    @property
    def secondary_gw_4(self):
        """
        return the current template_config value of secondary_gw_4
        """
        return self.template_config["secondaryGW4"]

    @secondary_gw_4.setter
    def secondary_gw_4(self, param):
        self.ndfc.verify_ipv4_address_with_prefix(param)
        self.template_config["secondaryGW4"] = param

    @property
    def segment_id(self):
        """
        return the current template_config value of segment_id
        """
        return self.template_config["segmentId"]

    @segment_id.setter
    def segment_id(self, param):
        self.ndfc.verify_vni(param)
        self.template_config["segmentId"] = param

    @property
    def suppress_arp(self):
        """
        return the current template_config value of suppress_arp
        """
        return self.template_config["suppressArp"]

    @suppress_arp.setter
    def suppress_arp(self, param):
        self.ndfc.verify_boolean(param)
        self.template_config["suppressArp"] = param

    @property
    def tag(self):
        """
        return the current template_config value of tag
        """
        return self.template_config["tag"]

    @tag.setter
    def tag(self, param):
        self.ndfc.verify_routing_tag(param)
        self.template_config["tag"] = param

    @property
    def trm_enabled(self):
        """
        return the current template_config value of trm_enabled
        """
        return self.template_config["trmEnabled"]

    @trm_enabled.setter
    def trm_enabled(self, param):
        self.ndfc.verify_boolean(param)
        self.template_config["trmEnabled"] = param

    @property
    def vlan_id(self):
        """
        return the current template_config value of vlan_id
        """
        return self.template_config["vlanId"]

    @vlan_id.setter
    def vlan_id(self, param):
        self.ndfc.verify_vlan(param)
        self.template_config["vlanId"] = param

    @property
    def vrf_dhcp(self):
        """
        return the current template_config value of vrf_dhcp
        """
        return self.template_config["vrfDhcp"]

    @vrf_dhcp.setter
    def vrf_dhcp(self, param):
        self.template_config["vrfDhcp"] = param

    @property
    def vrf_dhcp_2(self):
        """
        return the current template_config value of vrf_dhcp_2
        """
        return self.template_config["vrfDhcp2"]

    @vrf_dhcp_2.setter
    def vrf_dhcp_2(self, param):
        self.template_config["vrfDhcp2"] = param

    @property
    def vrf_dhcp_3(self):
        """
        return the current template_config value of vrf_dhcp_3
        """
        return self.template_config["vrfDhcp3"]

    @vrf_dhcp_3.setter
    def vrf_dhcp_3(self, param):
        self.template_config["vrfDhcp3"] = param
