"""
# Name

network_create.py

# Description

Send network create POST requests to the controller

# Payload Example

```json
{
    'displayName': 'MyNetwork_30000',
    'fabric': 'My_VxLAN_Fabric',
    'networkExtensionTemplate': 'Default_Network_Extension_Universal',
    'networkId': '30000',
    'networkName': 'MyNetwork_30000',
    'networkTemplate': 'Default_Network_Universal',
    'networkTemplateConfig': {
        'dhcpServerAddr1': '',
        'dhcpServerAddr2': '',
        'dhcpServerAddr3': '',
        'enableL3OnBorder': True,
        'enableL3OnBorderVpcBgw': False,
        'gatewayIpAddress': '10.1.1.1/24',
        'gatewayIpV6Address': '',
        'igmpVersion': '2',
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
        'trmV6Enabled': False,
        'vlanId': '',
        'vlanName': '',
        'VLAN_NETFLOW_MONITOR': '',
        'vrfDhcp': '',
        'vrfDhcp2': '',
        'vrfDhcp3': '',
        'vrfName': 'Customer-001'
    },
    'serviceNetworkTemplate': None,
    'source': None,
    'vrf': 'Customer-001'
}
```
"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import json
import logging
from ipaddress import AddressValueError

from ndfc_python.validations import Validations
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.fabric.fabric_details_v2 import FabricDetailsByName


@Properties.add_rest_send
@Properties.add_results
class NetworkCreate:
    """
    # Summary

    Create networks

    ## Example network create request

    ### See

    ./examples/network_create.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.validations = Validations()

        self._rest_send = None
        self._results = None

        self._payload_set = set()
        self._payload_set_mandatory = set()
        self._payload_default = {}
        self._template_config_set = set()
        self._template_config_default = {}
        self._template_config_set_mandatory = set()
        self.template_config = {}
        self.payload = {}
        self._payload_mapping_dict = {}
        self._template_config_mapping_dict = {}

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

    def _init_payload_set(self):
        """
        set of all payload keys
        """
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
        """
        set of all mandatory payload keys
        """
        self._payload_set_mandatory.add("fabric")
        self._payload_set_mandatory.add("networkName")
        self._payload_set_mandatory.add("networkId")
        self._payload_set_mandatory.add("vrf")

    def _init_payload_default(self):
        """
        set of all default payload keys

        These are keys for which the caller does not have to provide a value
        unless they specifically want to change them.
        """
        # fmt: off
        self._payload_default["networkExtensionTemplate"] = "Default_Network_Extension_Universal"
        self._payload_default["networkTemplate"] = "Default_Network_Universal"
        # fmt: on

    def _init_template_config_set(self):
        """
        set of all keys in the template Default_Network_Universal
        """
        # fmt: off
        self._template_config_set.add("dhcpServerAddr1")
        self._template_config_set.add("dhcpServerAddr2")
        self._template_config_set.add("dhcpServerAddr3")
        self._template_config_set.add("enableL3OnBorder")
        self._template_config_set.add("enableL3OnBorderVpcBgw")
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
        self._template_config_set.add("SVI_NETFLOW_MONITOR")
        self._template_config_set.add("tag")
        self._template_config_set.add("trmEnabled")
        self._template_config_set.add("trmV6Enabled")
        self._template_config_set.add("vlanId")
        self._template_config_set.add("vlanName")
        self._template_config_set.add("VLAN_NETFLOW_MONITOR")
        self._template_config_set.add("vrfDhcp")
        self._template_config_set.add("vrfDhcp2")
        self._template_config_set.add("vrfDhcp3")
        self._template_config_set.add("vrfName")
        # fmt: on

    def _init_template_config_default(self):
        """
        set of keys in the template Default_Network_Universal
        for which the caller does not need to provide a value
        unless they want to change them.
        """
        # fmt: off
        self._template_config_default["enableL3OnBorder"] = False
        self._template_config_default["enableL3OnBorderVpcBgw"] = False
        self._template_config_default["isLayer2Only"] = False
        self._template_config_default["mtu"] = 9216
        self._template_config_default["nveId"] = 1
        self._template_config_default["rtBothAuto"] = False
        self._template_config_default["suppressArp"] = True
        self._template_config_default["tag"] = "12345"
        self._template_config_default["trmEnabled"] = False
        self._template_config_default["trmV6Enabled"] = False
        # fmt: on

    def _init_template_config_set_mandatory(self):
        """
        set of mandatory keys in the template Default_Network_Universal
        """
        self._template_config_set_mandatory.add("vlanId")

    def _init_payload(self):
        self.payload = {}
        for param in self._payload_set:
            if param in self._payload_default:
                self.payload[param] = self._payload_default[param]
            else:
                self.payload[param] = ""

    def _init_template_config(self):
        for param in self._template_config_set:
            if param in self._template_config_default:
                self.template_config[param] = self._template_config_default[param]
            else:
                self.template_config[param] = ""

    def _preprocess_payload(self):
        """
        1. Set a default value for any properties that the caller
        has not set and that the controller provides a default for.

        2. Copy top-level property values (that need it) into their
        respective template_config properties.

        3. Any other fixup that may be required
        """
        method_name = inspect.stack()[0][3]
        # if source is null, NDFC complains if it's present
        if self.source == "":
            self.payload.pop("source", None)
            msg = f"{self.class_name}.{method_name}: "
            msg += "deleted null source key from payload to avoid controller complaints"
            self.log.debug(msg)
        if self.network_name == "":
            self.network_name = f"MyNetwork_{self.network_id}"
            self.template_config["networkName"] = self.network_name
        if self.display_name == "":
            self.display_name = self.network_name
        self.template_config["vrfName"] = self.vrf_name
        if self.segment_id == "":
            self.segment_id = self.network_id

    def _init_payload_mapping_dict(self):
        """
        see _map_payload_param()
        """
        # fmt: off
        self._payload_mapping_dict = {}
        self._payload_mapping_dict["displayName"] = "display_name"
        self._payload_mapping_dict["fabric"] = "fabric_name"
        self._payload_mapping_dict["networkExtensionTemplate"] = "network_extension_template"
        self._payload_mapping_dict["networkId"] = "network_id"
        self._payload_mapping_dict["networkName"] = "network_name"
        self._payload_mapping_dict["networkTemplate"] = "network_template"
        self._payload_mapping_dict["serviceNetworkTemplate"] = "service_network_template"
        self._payload_mapping_dict["source"] = "source"
        self._payload_mapping_dict["vrf"] = "vrf_name"
        # fmt: on

    def _init_template_config_mapping_dict(self):
        """
        see _map_template_config_param()
        """
        # fmt: off
        self._template_config_mapping_dict = {}
        self._template_config_mapping_dict["dhcpServerAddr1"] = "dhcp_server_addr_1"
        self._template_config_mapping_dict["dhcpServerAddr2"] = "dhcp_server_addr_2"
        self._template_config_mapping_dict["dhcpServerAddr3"] = "dhcp_server_addr_3"
        self._template_config_mapping_dict["enableL3OnBorder"] = "enable_l3_on_border"
        self._template_config_mapping_dict["enableL3OnBorderVpcBgw"] = "enable_l3_on_border_vpc_bgw"
        self._template_config_mapping_dict["gatewayIpAddress"] = "gateway_ip_address"
        self._template_config_mapping_dict["gatewayIpV6Address"] = "gateway_ipv6_address"
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
        self._template_config_mapping_dict["SVI_NETFLOW_MONITOR"] = "svi_netflow_monitor"
        self._template_config_mapping_dict["tag"] = "tag"
        self._template_config_mapping_dict["trmEnabled"] = "trm_enabled"
        self._template_config_mapping_dict["trmV6Enabled"] = "trm_v6_enabled"
        self._template_config_mapping_dict["vlanId"] = "vlan_id"
        self._template_config_mapping_dict["vlanName"] = "vlan_name"
        self._template_config_mapping_dict["VLAN_NETFLOW_MONITOR"] = "vlan_netflow_monitor"
        self._template_config_mapping_dict["vrf"] = "vrf_name"
        self._template_config_mapping_dict["vrfDhcp"] = "vrf_dhcp"
        self._template_config_mapping_dict["vrfDhcp2"] = "vrf_dhcp_2"
        self._template_config_mapping_dict["vrfDhcp3"] = "vrf_dhcp_3"
        # fmt: on

    def _map_payload_param(self, param):
        """
        Because payload keys are camel case, and pylint does not like camel
        case, we modified the corresponding properties to be snake case.  This
        method maps the camel case keys to their corresponding properties. It
        is used in _final_verification to provide the user with the correct
        property to call if there's a missing mandatory payload property.
        """
        method_name = inspect.stack()[0][3]
        if param not in self._payload_mapping_dict:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"param {param} not in _payload_mapping_dict"
            self.log.warning(msg)
            return param
        return self._payload_mapping_dict[param]

    def _map_template_config_param(self, param):
        """
        Because template_config keys are camel case, and pylint does not like camel
        case, we modified the corresponding properties to be snake case.  This
        method maps the camel case keys to their corresponding properties. It
        is used in _final_verification to provide the user with the correct
        property to call if there's a missing mandatory template_config property.
        """
        method_name = inspect.stack()[0][3]
        if param not in self._template_config_mapping_dict:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"param {param} not in "
            msg += "_template_config_mapping_dict"
            self.log.warning(msg)
            return param
        return self._template_config_mapping_dict[param]

    def _final_verification(self):
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        # pylint: disable=no-member
        if self.rest_send is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.rest_send must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)
        if self.results is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.results must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)
        # pylint: enable=no-member

        for param in self._payload_set_mandatory:
            if self.payload.get(param) == "" or self.payload.get(param) is None:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Call {self.class_name}."
                msg += f"{self._map_payload_param(param)} "
                msg += f"before calling {self.class_name}.commit"
                raise ValueError(msg)
        # fmt: off
        for param in self._template_config_set_mandatory:
            if self.template_config[param] == "":
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Call {self.class_name}.{self._map_template_config_param(param)} "
                msg += f"before calling {self.class_name}.commit"
                raise ValueError(msg)
        # fmt: on

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        if self.vrf_exists_in_fabric() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"vrf {self.vrf_name} does not exist in fabric "
            msg += f"{self.fabric_name}. Create it before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.network_id_exists_in_fabric() is True:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"networkId {self.network_id} already exists "
            msg += f"in fabric {self.fabric_name}. Delete it before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

    def fabric_exists(self):
        """
        Return True if self.fabric_name exists on the controller.
        Return False otherwise.
        """
        instance = FabricDetailsByName()
        # pylint: disable=no-member
        instance.rest_send = self.rest_send
        instance.results = self.results
        # pylint: enable=no-member
        instance.refresh()
        instance.filter = self.fabric_name
        if instance.filtered_data is None:
            return False
        return True

    def vrf_exists_in_fabric(self):
        """
        Return True if self.vrf_name exists in self.fabric_name.
        Else, return False
        """
        method_name = inspect.stack()[0][3]
        # TODO: update when this path is added to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/vrfs"
        verb = "GET"

        # pylint: disable=no-member
        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        for item_d in self.rest_send.response_current["DATA"]:
            if "fabric" not in item_d:
                continue
            if "vrfName" not in item_d:
                continue
            if item_d["fabric"] != self.fabric_name:
                continue
            if item_d["vrfName"] != self.vrf_name:
                continue
            return True
        # pylint: enable=no-member
        return False

    def network_id_exists_in_fabric(self):
        """
        Return True if networkId is present in the fabric
        Else, return False
        """
        method_name = inspect.stack()[0][3]
        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/networks"
        verb = "GET"
        # pylint: disable=no-member
        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        for item in self.rest_send.response_current["DATA"]:
            if "networkId" not in item:
                continue
            if item["networkId"] == self.network_id:
                return True
        return False

    def network_name_exists_in_fabric(self):
        """
        Return True if networkName exists in the fabric.
        Else return False
        """
        method_name = inspect.stack()[0][3]
        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/networks"
        verb = "GET"

        # pylint: disable=no-member
        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        for item in self.rest_send.response_current["DATA"]:
            if "networkName" not in item:
                continue
            if item["networkName"] == self.network_name:
                return True
        return False

    def commit(self):
        """
        Create a network
        """
        method_name = inspect.stack()[0][3]
        self._preprocess_payload()
        self._final_verification()

        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/networks"
        verb = "POST"

        self.payload["networkTemplateConfig"] = json.dumps(self.template_config)
        # pylint: disable=no-member
        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.payload = self.payload
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

    # top_level payload properties
    @property
    def display_name(self):
        """
        return the current payload value of display_name
        """
        return self.payload.get("displayName")

    @display_name.setter
    def display_name(self, value):
        self.payload["displayName"] = value

    @property
    def fabric_name(self):
        """
        return the current payload value of fabric
        """
        return self.payload.get("fabric")

    @fabric_name.setter
    def fabric_name(self, value):
        self.payload["fabric"] = value

    @property
    def network_extension_template(self):
        """
        return the current payload value of network_extension_template
        """
        return self.payload.get("networkExtensionTemplate")

    @network_extension_template.setter
    def network_extension_template(self, value):
        self.payload["networkExtensionTemplate"] = value

    @property
    def network_id(self):
        """
        return the current payload value of networkId
        """
        return self.payload.get("networkId")

    @network_id.setter
    def network_id(self, value):
        self.payload["networkId"] = value

    @property
    def network_name(self):
        """
        return the current payload value of networkName
        """
        return self.payload.get("networkName")

    @network_name.setter
    def network_name(self, value):
        self.payload["networkName"] = value

    @property
    def network_template(self):
        """
        return the current payload value of networkTemplate
        """
        return self.payload.get("networkTemplate")

    @network_template.setter
    def network_template(self, value):
        self.payload["networkTemplate"] = value

    @property
    def service_network_template(self):
        """
        return the current payload value of serviceNetworkTemplate
        """
        return self.payload.get("serviceNetworkTemplate")

    @service_network_template.setter
    def service_network_template(self, value):
        self.payload["serviceNetworkTemplate"] = value

    @property
    def source(self):
        """
        return the current payload value of source
        """
        return self.payload.get("source")

    @source.setter
    def source(self, value):
        self.payload["source"] = value

    @property
    def vrf_name(self):
        """
        return the current payload value of vrf
        """
        return self.payload.get("vrf")

    @vrf_name.setter
    def vrf_name(self, value):
        self.payload["vrf"] = value

    # template_config properties
    @property
    def dhcp_server_addr_1(self):
        """
        return the current template_config value of dhcpServerAddr1
        """
        return self.template_config.get("dhcpServerAddr1")

    @dhcp_server_addr_1.setter
    def dhcp_server_addr_1(self, value):
        self.template_config["dhcpServerAddr1"] = value

    @property
    def dhcp_server_addr_2(self):
        """
        return the current template_config value of dhcpServerAddr2
        """
        return self.template_config.get("dhcpServerAddr2")

    @dhcp_server_addr_2.setter
    def dhcp_server_addr_2(self, value):
        self.template_config["dhcpServerAddr2"] = value

    @property
    def dhcp_server_addr_3(self):
        """
        return the current template_config value of dhcpServerAddr3
        """
        return self.template_config.get("dhcpServerAddr3")

    @dhcp_server_addr_3.setter
    def dhcp_server_addr_3(self, value):
        self.template_config["dhcpServerAddr3"] = value

    @property
    def enable_l3_on_border(self):
        """
        return the current template_config value of enableL3OnBorder
        """
        return self.template_config.get("enableL3OnBorder")

    @enable_l3_on_border.setter
    def enable_l3_on_border(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(value)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["enableL3OnBorder"] = value

    @property
    def enable_l3_on_border_vpc_bgw(self):
        """
        return the current template_config value of enableL3OnBorderVpcBgw
        """
        return self.template_config.get("enableL3OnBorderVpcBgw")

    @enable_l3_on_border_vpc_bgw.setter
    def enable_l3_on_border_vpc_bgw(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(value)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["enableL3OnBorderVpcBgw"] = value

    @property
    def gateway_ip_address(self):
        """
        return the current template_config value of gatewayIpAddress
        """
        return self.template_config.get("gatewayIpAddress")

    @gateway_ip_address.setter
    def gateway_ip_address(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_address_with_prefix(value)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["gatewayIpAddress"] = value

    @property
    def gateway_ipv6_address(self):
        """
        return the current template_config value of gatewayIpV6Address

        Comma-separated list of IPv6/Prefix.

        Example: 2001:db8::1/64,2001:db9::1/64
        """
        return self.template_config.get("gatewayIpV6Address")

    @gateway_ipv6_address.setter
    def gateway_ipv6_address(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv6_address_with_prefix(value)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["gatewayIpV6Address"] = value

    @property
    def igmp_version(self):
        """
        return the current template_config value of igmpVersion
        """
        return self.template_config.get("igmpVersion")

    @igmp_version.setter
    def igmp_version(self, value):
        method_name = inspect.stack()[0][3]
        if value not in self.validations.valid_igmp_versions:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Invalid igmp_version.  Expected one of "
            msg += f"{','.join(self.validations.valid_igmp_versions)}"
            raise ValueError(msg)
        self.template_config["igmpVersion"] = value

    @property
    def intf_description(self):
        """
        return the current template_config value of intfDescription
        """
        return self.template_config.get("intfDescription")

    @intf_description.setter
    def intf_description(self, value):
        self.template_config["intfDescription"] = value

    @property
    def is_layer2_only(self):
        """
        return the current template_config value of isLayer2Only
        """
        return self.template_config.get("isLayer2Only")

    @is_layer2_only.setter
    def is_layer2_only(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(value)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["isLayer2Only"] = value

    @property
    def loopback_id(self):
        """
        return the current template_config value of loopbackId
        """
        return self.template_config.get("loopbackId")

    @loopback_id.setter
    def loopback_id(self, value):
        self.validations.verify_loopback_id(value)
        self.template_config["loopbackId"] = value

    @property
    def mcast_group(self):
        """
        return the current template_config value of mcastGroup
        """
        return self.template_config.get("mcastGroup")

    @mcast_group.setter
    def mcast_group(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_multicast_address(value)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["mcastGroup"] = value

    @property
    def mtu(self):
        """
        return the current template_config value of mtu
        """
        return self.template_config.get("mtu")

    @mtu.setter
    def mtu(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_mtu(value)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["mtu"] = value

    # networkName (see property for self.payload['networkName])
    # We populate self.template_config['networkName'] from the value
    # in self.payload['networkName']

    @property
    def nve_id(self):
        """
        return the current template_config value of nveId
        """
        return self.template_config.get("nveId")

    @nve_id.setter
    def nve_id(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_nve_id(value)
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["nveId"] = value

    @property
    def rt_both_auto(self):
        """
        return the current template_config value of rtBothAuto
        """
        return self.template_config.get("rtBothAuto")

    @rt_both_auto.setter
    def rt_both_auto(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(value)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["rtBothAuto"] = value

    @property
    def secondary_gw_1(self):
        """
        return the current template_config value of secondaryGW1
        """
        return self.template_config.get("secondaryGW1")

    @secondary_gw_1.setter
    def secondary_gw_1(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_address_with_prefix(value)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["secondaryGW1"] = value

    @property
    def secondary_gw_2(self):
        """
        return the current template_config value of secondaryGW2
        """
        return self.template_config.get("secondaryGW2")

    @secondary_gw_2.setter
    def secondary_gw_2(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_address_with_prefix(value)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["secondaryGW2"] = value

    @property
    def secondary_gw_3(self):
        """
        return the current template_config value of secondaryGW3
        """
        return self.template_config.get("secondaryGW3")

    @secondary_gw_3.setter
    def secondary_gw_3(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_address_with_prefix(value)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["secondaryGW3"] = value

    @property
    def secondary_gw_4(self):
        """
        return the current template_config value of secondaryGW4
        """
        return self.template_config.get("secondaryGW4")

    @secondary_gw_4.setter
    def secondary_gw_4(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_ipv4_address_with_prefix(value)
        except AddressValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["secondaryGW4"] = value

    @property
    def segment_id(self):
        """
        return the current template_config value of segmentId
        """
        return self.template_config.get("segmentId")

    @segment_id.setter
    def segment_id(self, value):
        self.validations.verify_vni(value)
        self.template_config["segmentId"] = value

    @property
    def suppress_arp(self):
        """
        return the current template_config value of suppressArp
        """
        return self.template_config.get("suppressArp")

    @suppress_arp.setter
    def suppress_arp(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(value)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["suppressArp"] = value

    @property
    def svi_netflow_monitor(self):
        """
        return the current template_config value of SVI_NETFLOW_MONITOR
        """
        return self.template_config.get("SVI_NETFLOW_MONITOR")

    @svi_netflow_monitor.setter
    def svi_netflow_monitor(self, value):
        self.template_config["SVI_NETFLOW_MONITOR"] = value

    @property
    def tag(self):
        """
        return the current template_config value of tag
        """
        return self.template_config.get("tag")

    @tag.setter
    def tag(self, value):
        self.validations.verify_routing_tag(value)
        self.template_config["tag"] = value

    @property
    def trm_enabled(self):
        """
        return the current template_config value of trmEnabled
        """
        return self.template_config.get("trmEnabled")

    @trm_enabled.setter
    def trm_enabled(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(value)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["trmEnabled"] = value

    @property
    def trm_v6_enabled(self):
        """
        return the current template_config value of trmV6Enabled
        """
        return self.template_config.get("trmV6Enabled")

    @trm_v6_enabled.setter
    def trm_v6_enabled(self, value):
        method_name = inspect.stack()[0][3]
        try:
            self.validations.verify_boolean(value)
        except TypeError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.template_config["trmV6Enabled"] = value

    @property
    def vlan_id(self):
        """
        return the current template_config value of vlanId
        """
        return self.template_config.get("vlanId")

    @vlan_id.setter
    def vlan_id(self, value):
        self.validations.verify_vlan(value)
        self.template_config["vlanId"] = value

    @property
    def vlan_name(self):
        """
        return the current template_config value of vlanName
        """
        return self.template_config.get("vlanName")

    @vlan_name.setter
    def vlan_name(self, value):
        self.template_config["vlanName"] = value

    @property
    def vlan_netflow_monitor(self):
        """
        return the current template_config value of VLAN_NETFLOW_MONITOR
        """
        return self.template_config.get("VLAN_NETFLOW_MONITOR")

    @vlan_netflow_monitor.setter
    def vlan_netflow_monitor(self, value):
        self.template_config["VLAN_NETFLOW_MONITOR"] = value

    @property
    def vrf_dhcp(self):
        """
        return the current template_config value of vrfDhcp
        """
        return self.template_config.get("vrfDhcp")

    @vrf_dhcp.setter
    def vrf_dhcp(self, value):
        self.template_config["vrfDhcp"] = value

    @property
    def vrf_dhcp_2(self):
        """
        return the current template_config value of vrfDhcp2
        """
        return self.template_config.get("vrfDhcp2")

    @vrf_dhcp_2.setter
    def vrf_dhcp_2(self, value):
        self.template_config["vrfDhcp2"] = value

    @property
    def vrf_dhcp_3(self):
        """
        return the current template_config value of vrfDhcp3
        """
        return self.template_config.get("vrfDhcp3")

    @vrf_dhcp_3.setter
    def vrf_dhcp_3(self, value):
        self.template_config["vrfDhcp3"] = value
