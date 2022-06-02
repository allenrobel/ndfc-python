our_version = 100
import json
from ndfc_lib.common import Common
class NdfcNetwork(Common):
    def __init__(self, ndfc, log):
        super().__init__(log)
        self.lib_version = our_version
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        self.network = dict()
        self.properties_set = set()
        self.properties_set.add('displayName')
        self.properties_set.add('fabric')
        self.properties_set.add('networkExtensionTemplate')
        self.properties_set.add('networkId')
        self.properties_set.add('networkName')
        self.properties_set.add('networkTemplate')
        self.properties_set.add('serviceNetworkTemplate')
        self.properties_set.add('source')
        self.properties_set.add('vrf')

        self.mandatory_properties_set = set()
        self.mandatory_properties_set.add('displayName')
        self.mandatory_properties_set.add('fabric')
        self.mandatory_properties_set.add('segmentId')
        self.mandatory_properties_set.add('vrfName')
        self.mandatory_properties_set.add('vlanId')
        self.mandatory_properties_set.add('displayName')

        self.properties_default = dict()
        self.properties_default['networkExtensionTemplate'] = 'Default_Network_Extension_Universal'
        self.properties_default['networkTemplate'] = 'Default_Network_Universal'

        self.network_template_config_set = set()
        self.network_template_config_set.add('dhcpServerAddr1')
        self.network_template_config_set.add('dhcpServerAddr2')
        self.network_template_config_set.add('enableIR')
        self.network_template_config_set.add('enableL3OnBorder')
        self.network_template_config_set.add('gatewayIpAddress')
        self.network_template_config_set.add('gatewayIpV6Address')
        self.network_template_config_set.add('intfDescription')
        self.network_template_config_set.add('isLayer2Only')
        self.network_template_config_set.add('loopbackId')
        self.network_template_config_set.add('mcastGroup')
        self.network_template_config_set.add('mtu')
        self.network_template_config_set.add('networkName')
        self.network_template_config_set.add('nveId')
        self.network_template_config_set.add('rtBothAuto')
        self.network_template_config_set.add('secondaryGW1')
        self.network_template_config_set.add('secondaryGW2')
        self.network_template_config_set.add('segmentId')
        self.network_template_config_set.add('suppressArp')
        self.network_template_config_set.add('tag')
        self.network_template_config_set.add('trmEnabled')
        self.network_template_config_set.add('vlanId')
        self.network_template_config_set.add('vlanName')
        self.network_template_config_set.add('vrfDhcp')
        self.network_template_config_set.add('vrfName')

        self.network_template_config_default = dict()
        self.network_template_config_default['enableIR'] = False
        self.network_template_config_default['enableL3OnBorder'] = True
        self.network_template_config_default['isLayer2Only'] = False
        self.network_template_config_default['mtu'] = 9216
        self.network_template_config_default['nveId'] = 1
        self.network_template_config_default['rtBothAuto'] = True
        self.network_template_config_default['suppressArp'] = True
        self.network_template_config_default['tag'] = '12345'
        self.network_template_config_default['trmEnabled'] = False
        self.network_template_config_default['rtBothAuto'] = True

    def init_properties(self):
        self.properties = dict()
        for p in self.properties_set:
            if p in self.properties_default:
                self.properties[p] = self.properties_default[p]
            else:
                self.properties[p] = None
    def init_network_template_config(self):
        self.network_template_config = dict()
        for p in self.network_template_config_set:
            if p in self.network_template_config_default:
                self.network_template_config[p] = self.network_template_config_default[p]
            else:
                self.network_template_config[p] = None

    def final_verification(self):
        for p in self.mandatory_properties_set:
            if p == None:
                self.log.error('exiting. call instance.{} before calling instance.post()'.format(p))
                exit(1)

    def post(self):
        self.final_verification()
        self.headers = dict()
        self.headers['Authorization'] = self.ndfc.token
        self.headers['Content-Type'] = 'application/json'
        self.url = '/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{}/networks'.format(self.fabric)

    # top_level properties
    @property
    def displayName(self):
        return self.properties['displayName']
    @displayName.setter
    def displayName(self, x):
        self.properties['displayName'] = x

    @property
    def fabric(self):
        return self.properties['fabric']
    @fabric.setter
    def fabric(self, x):
        self.properties['fabric'] = x

    @property
    def networkExtensionTemplate(self):
        return self.properties['networkExtensionTemplate']
    @networkExtensionTemplate.setter
    def networkExtensionTemplate(self, x):
        self.properties['networkExtensionTemplate'] = x

    @property
    def networkId(self):
        return self.properties['networkId']
    @networkId.setter
    def networkId(self, x):
        self.properties['networkId'] = x

    @property
    def networkName(self):
        return self.properties['networkName']
    @networkName.setter
    def networkName(self, x):
        self.properties['networkName'] = x

    @property
    def networkTemplate(self):
        return self.properties['networkTemplate']
    @networkTemplate.setter
    def networkTemplate(self, x):
        self.properties['networkTemplate'] = x

    @property
    def serviceNetworkTemplate(self):
        return self.properties['serviceNetworkTemplate']
    @serviceNetworkTemplate.setter
    def serviceNetworkTemplate(self, x):
        self.properties['serviceNetworkTemplate'] = x

    @property
    def source(self):
        return self.properties['source']
    @source.setter
    def source(self, x):
        self.properties['source'] = x

    @property
    def vrf(self):
        return self.properties['vrf']
    @vrf.setter
    def vrf(self, x):
        self.properties['vrf'] = x

    # network_template_config properties
    @property
    def dhcpServerAddr1(self):
        return self.network_template_config['dhcpServerAddr1']
    @dhcpServerAddr1.setter
    def dhcpServerAddr1(self, x):
        self.network_template_config['dhcpServerAddr1'] = x

    @property
    def dhcpServerAddr2(self):
        return self.network_template_config['dhcpServerAddr2']
    @dhcpServerAddr2.setter
    def dhcpServerAddr2(self, x):
        self.network_template_config['dhcpServerAddr2'] = x

    @property
    def enableIR(self):
        return self.network_template_config['enableIR']
    @enableIR.setter
    def enableIR(self, x):
        self.verify_boolean(x)
        self.network_template_config['enableIR'] = x

    @property
    def enableL3OnBorder(self):
        return self.network_template_config['enableL3OnBorder']
    @enableL3OnBorder.setter
    def enableL3OnBorder(self, x):
        self.verify_boolean(x)
        self.network_template_config['enableL3OnBorder'] = x

    @property
    def gatewayIpAddress(self):
        return self.network_template_config['gatewayIpAddress']
    @gatewayIpAddress.setter
    def gatewayIpAddress(self, x):
        self.verify_ipv4_address_with_prefix(x)
        self.network_template_config['gatewayIpAddress'] = x

    @property
    def gatewayIpV6Address(self):
        return self.network_template_config['gatewayIpV6Address']
    @gatewayIpV6Address.setter
    def gatewayIpV6Address(self, x):
        self.verify_ipv6_address_with_prefix(x)
        self.network_template_config['gatewayIpV6Address'] = x

    @property
    def intfDescription(self):
        return self.network_template_config['intfDescription']
    @intfDescription.setter
    def intfDescription(self, x):
        self.network_template_config['intfDescription'] = x

    @property
    def isLayer2Only(self):
        return self.network_template_config['isLayer2Only']
    @isLayer2Only.setter
    def isLayer2Only(self, x):
        self.verify_boolean(x)
        self.network_template_config['isLayer2Only'] = x

    @property
    def loopbackId(self):
        return self.network_template_config['loopbackId']
    @loopbackId.setter
    def loopbackId(self, x):
        self.verify_loopback_id(x)
        self.network_template_config['loopbackId'] = x

    @property
    def mcastGroup(self):
        return self.network_template_config['mcastGroup']
    @mcastGroup.setter
    def mcastGroup(self, x):
        self.verify_ipv4_multicast_address(x, '{}.mcastGroup.setter'.format(self.class_name))
        self.network_template_config['mcastGroup'] = x

    @property
    def mtu(self):
        return self.network_template_config['mtu']
    @mtu.setter
    def mtu(self, x):
        self.verify_mtu(x, '{}.mtu.setter'.format(self.class_name))
        self.network_template_config['mtu'] = x

    @property
    def networkName(self):
        return self.network_template_config['networkName']
    @networkName.setter
    def networkName(self, x):
        self.network_template_config['networkName'] = x

    @property
    def nveId(self):
        return self.network_template_config['nveId']
    @nveId.setter
    def nveId(self, x):
        self.verify_nve_id(x, '{}.nveId.setter'.format(self.class_name))
        self.network_template_config['nveId'] = x

    @property
    def rtBothAuto(self):
        return self.network_template_config['rtBothAuto']
    @rtBothAuto.setter
    def rtBothAuto(self, x):
        self.verify_boolean(x)
        self.network_template_config['rtBothAuto'] = x

    @property
    def secondaryGW1(self):
        return self.network_template_config['secondaryGW1']
    @secondaryGW1.setter
    def secondaryGW1(self, x):
        self.verify_ipv4_address_with_prefix(x)
        self.network_template_config['secondaryGW1'] = x

    @property
    def secondaryGW2(self):
        return self.network_template_config['secondaryGW2']
    @secondaryGW2.setter
    def secondaryGW2(self, x):
        self.verify_ipv4_address_with_prefix(x)
        self.network_template_config['secondaryGW2'] = x

    @property
    def segmentId(self):
        return self.network_template_config['segmentId']
    @segmentId.setter
    def segmentId(self, x):
        self.verify_vni(x)
        self.network_template_config['segmentId'] = x

    @property
    def suppressArp(self):
        return self.network_template_config['suppressArp']
    @suppressArp.setter
    def suppressArp(self, x):
        self.verify_boolean(x)
        self.network_template_config['suppressArp'] = x

    @property
    def tag(self):
        return self.network_template_config['tag']
    @tag.setter
    def tag(self, x):
        self.verify_routing_tag(x)
        self.network_template_config['tag'] = x

    @property
    def trmEnabled(self):
        return self.network_template_config['trmEnabled']
    @trmEnabled.setter
    def trmEnabled(self, x):
        self.verify_boolean(x)
        self.network_template_config['trmEnabled'] = x

    @property
    def vlanId(self):
        return self.network_template_config['vlanId']
    @vlanId.setter
    def vlanId(self, x):
        self.verify_vlan(x)
        self.network_template_config['vlanId'] = x

    @property
    def vrfDhcp(self):
        return self.network_template_config['vrfDhcp']
    @vrfDhcp.setter
    def vrfDhcp(self, x):
        self.network_template_config['vrfDhcp'] = x

    @property
    def vrfName(self):
        return self.network_template_config['vrfName']
    @vrfName.setter
    def vrfName(self, x):
        self.network_template_config['vrfName'] = x


# network = {'displayName': 'MyNetwork_30000',
#  'fabric': 'IBM_VxLAN_Fabric',
#  'networkExtensionTemplate': 'Default_Network_Extension_Universal',
#  'networkId': '30000',
#  'networkName': 'MyNetwork_30000',
#  'networkTemplate': 'Default_Network_Universal',
#  'networkTemplateConfig': {'dhcpServerAddr1': '',
#                            'dhcpServerAddr2': '',
#                            'enableIR': False,
#                            'enableL3OnBorder': True,
#                            'gatewayIpAddress': '10.1.1.1/24',
#                            'gatewayIpV6Address': '',
#                            'intfDescription': '',
#                            'isLayer2Only': False,
#                            'loopbackId': '',
#                            'mcastGroup': '',
#                            'mtu': '9216',
#                            'networkName': 'MyNetwork_30000',
#                            'nveId': 1,
#                            'rtBothAuto': True,
#                            'secondaryGW1': '',
#                            'secondaryGW2': '',
#                            'segmentId': '30000',
#                            'suppressArp': True,
#                            'tag': '12345',
#                            'trmEnabled': False,
#                            'vlanId': '',
#                            'vlanName': '',
#                            'vrfDhcp': '',
#                            'vrfName': 'Customer-001'},
#  'serviceNetworkTemplate': None,
#  'source': None,
#  'vrf': 'Customer-001'}