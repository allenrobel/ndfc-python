our_version = 100
import json
'''
Create / delete networks  The JSON payload constructed by this
class is shown below.

network = {'displayName': 'MyNetwork_30000',
 'fabric': 'IBM_VxLAN_Fabric',
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
 
'''
class NdfcNetwork(object):
    '''
    create / delete networks

    Example create operation

    instance = NdfcNetwork(ndfc)
    instance.fabric = 'foo'
    instance.networkId = 30000
    instance.vlanId = 3000
    instance.vrf = 'foo_vrf'
    instance.create()

    Example delete operation

    instance = NdfcNetwork(ndfc)
    instance.fabric = 'foo'
    instance.networkName = 'MyNetwork_30000'
    instance.delete()

    '''
    def __init__(self, ndfc):
        self.lib_version = our_version
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        # post/get base headers
        self.headers = dict()
        self.headers['Content-Type'] = 'application/json'

        self.payload_set = set()
        self.payload_set.add('displayName')
        self.payload_set.add('fabric')
        self.payload_set.add('networkExtensionTemplate')
        self.payload_set.add('networkId')
        self.payload_set.add('networkName')
        self.payload_set.add('networkTemplate')
        self.payload_set.add('serviceNetworkTemplate')
        self.payload_set.add('source')
        self.payload_set.add('vrf')

        self.payload_set_mandatory = set()
        self.payload_set_mandatory.add('fabric')
        self.payload_set_mandatory.add('networkId')
        self.payload_set_mandatory.add('vrf')

        self.payload_default = dict()
        self.payload_default['networkExtensionTemplate'] = 'Default_Network_Extension_Universal'
        self.payload_default['networkTemplate'] = 'Default_Network_Universal'

        self.template_config_set = set()
        self.template_config_set.add('dhcpServerAddr1')
        self.template_config_set.add('dhcpServerAddr2')
        self.template_config_set.add('dhcpServerAddr3')
        self.template_config_set.add('enableIR')
        self.template_config_set.add('enableL3OnBorder')
        self.template_config_set.add('gatewayIpAddress')
        self.template_config_set.add('gatewayIpV6Address')
        self.template_config_set.add('intfDescription')
        self.template_config_set.add('isLayer2Only')
        self.template_config_set.add('loopbackId')
        self.template_config_set.add('mcastGroup')
        self.template_config_set.add('mtu')
        self.template_config_set.add('networkName')
        self.template_config_set.add('nveId')
        self.template_config_set.add('rtBothAuto')
        self.template_config_set.add('secondaryGW1')
        self.template_config_set.add('secondaryGW2')
        self.template_config_set.add('secondaryGW3')
        self.template_config_set.add('secondaryGW4')
        self.template_config_set.add('segmentId')
        self.template_config_set.add('suppressArp')
        self.template_config_set.add('tag')
        self.template_config_set.add('trmEnabled')
        self.template_config_set.add('vlanId')
        self.template_config_set.add('vlanName')
        self.template_config_set.add('vrfDhcp')
        self.template_config_set.add('vrfDhcp2')
        self.template_config_set.add('vrfDhcp3')
        self.template_config_set.add('vrfName')

        self.template_config_set_mandatory = set()
        self.template_config_set_mandatory.add('vlanId')

        self.template_config_default = dict()
        self.template_config_default['enableIR'] = True
        self.template_config_default['enableL3OnBorder'] = False
        self.template_config_default['isLayer2Only'] = False
        self.template_config_default['mtu'] = 9216
        self.template_config_default['nveId'] = 1
        self.template_config_default['rtBothAuto'] = False
        self.template_config_default['suppressArp'] = True
        self.template_config_default['tag'] = '12345'
        self.template_config_default['trmEnabled'] = False

        self.init_payload()
        self.init_template_config()

    def init_payload(self):
        self.payload = dict()
        for p in self.payload_set:
            if p in self.payload_default:
                self.payload[p] = self.payload_default[p]
            else:
                self.payload[p] = ""
    def init_template_config(self):
        self.template_config = dict()
        for p in self.template_config_set:
            if p in self.template_config_default:
                self.template_config[p] = self.template_config_default[p]
            else:
                self.template_config[p] = ""

    def preprocess_payload(self):
        '''
        1. Set a default value for any properties that the caller has not set and that NDFC provides a default for. 

        2. Copy top-level property values (that need it) into their respective template_config properties.

        3. Any other fixup that may be required
        '''
        # if source is null, NDFC complains if it's present
        if self.source == "":
            self.payload.pop('source', None)
            self.ndfc.log.debug('deleted null source key from payload to avoid ndfc complaints')
        if self.networkName == "":
            self.networkName = 'MyNetwork_{}'.format(self.networkId)
            self.template_config['networkName'] = self.networkName
        if self.displayName == "":
            self.displayName = self.networkName
        self.template_config['vrfName'] = self.vrf
        if self.segmentId == "":
            self.segmentId = self.networkId

    def final_verification(self):
        for p in self.payload_set_mandatory:
            if self.payload[p] == "":
                self.ndfc.log.error('exiting. call instance.{} before calling instance.create()'.format(p))
                exit(1)
        for p in self.template_config_set_mandatory:
            if self.template_config[p] == "":
                self.ndfc.log.error('exiting. call instance.{} before calling instance.create()'.format(p))
                exit(1)

    def verify_vrf_exists_in_fabric(self):
        '''
        Return True if vrfName is present in the fabric
        Else, return False
        '''
        url = f"{self.ndfc.url_api_v1}/lan-fabric/rest/top-down/fabrics/{self.fabric}/vrfs"
        headers = self.headers
        headers['Authorization'] = self.ndfc.bearer_token

        response = self.ndfc.get(url, headers)
        for d in response:
            if 'fabric' not in d:
                continue
            if 'vrfName' not in d:
                continue
            if d['fabric'] != self.fabric:
                continue
            if d['vrfName'] != self.vrf:
                continue
            return True
        return False

    def verify_network_id_does_not_exist_in_fabric(self):
        '''
        Return True if networkId is not present in the fabric
        Else, return False
        '''
        url = f"{self.ndfc.url_api_v1}/lan-fabric/rest/top-down/fabrics/{self.fabric}/networks"
        headers = self.headers
        headers['Authorization'] = self.ndfc.bearer_token

        response = self.ndfc.get(url, headers)
        for d in response:
            if 'networkId' not in d:
                continue
            if d['networkId'] == self.networkId:
                return False
        return True

    def verify_network_name_exists_in_fabric(self):
        '''
        Return True if networkId exists in the fabric.
        Else return False
        '''
        url = f"{self.ndfc.url_api_v1}/lan-fabric/rest/top-down/fabrics/{self.fabric}/networks"
        headers = self.headers
        headers['Authorization'] = self.ndfc.bearer_token

        response = self.ndfc.get(url, headers)
        for d in response:
            if 'networkName' not in d:
                continue
            if d['networkName'] == self.networkName:
                return True
            print('type(d[networkName] {} type(self.networkName) {}'.format(type(d['networkName'], type(self.networkName))))
        return False

    def create(self):
        self.preprocess_payload()
        self.final_verification()

        result = self.verify_vrf_exists_in_fabric()
        if result == False:
            self.ndfc.log.error(
                f'vrf {self.vrf} does not exist in fabric {self.fabric}.  Create it before calling NdfcNetwork()'    
            )
            exit(1)

        result = self.verify_network_id_does_not_exist_in_fabric()
        if result == False:
            self.ndfc.log.error('networkId {} already exists in fabric {}.  Delete it before calling NdfcNetwork.create()'.format(
                self.networkId,
                self.fabric
            ))
            exit(1)

        url = f"{self.ndfc.url_api_v1}/lan-fabric/rest/top-down/fabrics/{self.fabric}/networks"

        headers = self.headers
        headers['Authorization'] = self.ndfc.bearer_token

        self.payload['networkTemplateConfig'] = json.dumps(self.template_config)

        self.ndfc.post(url, headers, self.payload)

    def delete(self):
        if self.networkName == "":
            self.ndfc.log.error('call instance.networkName before calling NdfcNetworks.delete()')
            exit(1)
        if self.fabric == "":
            self.ndfc.log.error('call instance.fabric before calling NdfcNetworks.delete()')
            exit(1)

        headers = self.headers
        headers['Authorization'] = self.ndfc.bearer_token

        result = self.verify_network_name_exists_in_fabric()
        if result == False:
            self.ndfc.log.error('networName {} does not exist in fabric {}.'.format(
                self.networkName,
                self.fabric
            ))
            exit(1)

        url = f"{self.ndfc.url_api_v1}/lan-fabric/rest/top-down/fabrics/{self.fabric}/networks/{self.networkName}"

        self.ndfc.delete(url, headers)

    # top_level properties
    @property
    def displayName(self):
        return self.payload['displayName']
    @displayName.setter
    def displayName(self, x):
        self.payload['displayName'] = x

    @property
    def fabric(self):
        return self.payload['fabric']
    @fabric.setter
    def fabric(self, x):
        self.payload['fabric'] = x

    @property
    def networkExtensionTemplate(self):
        return self.payload['networkExtensionTemplate']
    @networkExtensionTemplate.setter
    def networkExtensionTemplate(self, x):
        self.payload['networkExtensionTemplate'] = x

    @property
    def networkId(self):
        return self.payload['networkId']
    @networkId.setter
    def networkId(self, x):
        self.payload['networkId'] = x

    @property
    def networkName(self):
        return self.payload['networkName']
    @networkName.setter
    def networkName(self, x):
        self.payload['networkName'] = x

    @property
    def networkTemplate(self):
        return self.payload['networkTemplate']
    @networkTemplate.setter
    def networkTemplate(self, x):
        self.payload['networkTemplate'] = x

    @property
    def serviceNetworkTemplate(self):
        return self.payload['serviceNetworkTemplate']
    @serviceNetworkTemplate.setter
    def serviceNetworkTemplate(self, x):
        self.payload['serviceNetworkTemplate'] = x

    @property
    def source(self):
        return self.payload['source']
    @source.setter
    def source(self, x):
        self.payload['source'] = x

    @property
    def vrf(self):
        return self.payload['vrf']
    @vrf.setter
    def vrf(self, x):
        self.payload['vrf'] = x

    # template_config properties
    @property
    def dhcpServerAddr1(self):
        return self.template_config['dhcpServerAddr1']
    @dhcpServerAddr1.setter
    def dhcpServerAddr1(self, x):
        self.template_config['dhcpServerAddr1'] = x

    @property
    def dhcpServerAddr2(self):
        return self.template_config['dhcpServerAddr2']
    @dhcpServerAddr2.setter
    def dhcpServerAddr2(self, x):
        self.template_config['dhcpServerAddr2'] = x

    @property
    def dhcpServerAddr3(self):
        return self.template_config['dhcpServerAddr3']
    @dhcpServerAddr3.setter
    def dhcpServerAddr3(self, x):
        self.template_config['dhcpServerAddr3'] = x

    @property
    def enableIR(self):
        return self.template_config['enableIR']
    @enableIR.setter
    def enableIR(self, x):
        self.ndfc.verify_boolean(x)
        self.template_config['enableIR'] = x

    @property
    def enableL3OnBorder(self):
        return self.template_config['enableL3OnBorder']
    @enableL3OnBorder.setter
    def enableL3OnBorder(self, x):
        self.ndfc.verify_boolean(x)
        self.template_config['enableL3OnBorder'] = x

    @property
    def gatewayIpAddress(self):
        return self.template_config['gatewayIpAddress']
    @gatewayIpAddress.setter
    def gatewayIpAddress(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.template_config['gatewayIpAddress'] = x

    @property
    def gatewayIpV6Address(self):
        return self.template_config['gatewayIpV6Address']
    @gatewayIpV6Address.setter
    def gatewayIpV6Address(self, x):
        self.ndfc.verify_ipv6_address_with_prefix(x)
        self.template_config['gatewayIpV6Address'] = x

    @property
    def intfDescription(self):
        return self.template_config['intfDescription']
    @intfDescription.setter
    def intfDescription(self, x):
        self.template_config['intfDescription'] = x

    @property
    def isLayer2Only(self):
        return self.template_config['isLayer2Only']
    @isLayer2Only.setter
    def isLayer2Only(self, x):
        self.ndfc.verify_boolean(x)
        self.template_config['isLayer2Only'] = x

    @property
    def loopbackId(self):
        return self.template_config['loopbackId']
    @loopbackId.setter
    def loopbackId(self, x):
        self.ndfc.verify_loopback_id(x)
        self.template_config['loopbackId'] = x

    @property
    def mcastGroup(self):
        return self.template_config['mcastGroup']
    @mcastGroup.setter
    def mcastGroup(self, x):
        self.ndfc.verify_ipv4_multicast_address(x, '{}.mcastGroup.setter'.format(self.class_name))
        self.template_config['mcastGroup'] = x

    @property
    def mtu(self):
        return self.template_config['mtu']
    @mtu.setter
    def mtu(self, x):
        self.ndfc.verify_mtu(x, '{}.mtu.setter'.format(self.class_name))
        self.template_config['mtu'] = x

    # networkName (see property for self.payload['networkName])
    # We populate self.template_config['networkName'] from the value
    # in self.payload['networkName']

    @property
    def nveId(self):
        return self.template_config['nveId']
    @nveId.setter
    def nveId(self, x):
        self.ndfc.verify_nve_id(x, '{}.nveId.setter'.format(self.class_name))
        self.template_config['nveId'] = x

    @property
    def rtBothAuto(self):
        return self.template_config['rtBothAuto']
    @rtBothAuto.setter
    def rtBothAuto(self, x):
        self.ndfc.verify_boolean(x)
        self.template_config['rtBothAuto'] = x

    @property
    def secondaryGW1(self):
        return self.template_config['secondaryGW1']
    @secondaryGW1.setter
    def secondaryGW1(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.template_config['secondaryGW1'] = x

    @property
    def secondaryGW2(self):
        return self.template_config['secondaryGW2']
    @secondaryGW2.setter
    def secondaryGW2(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.template_config['secondaryGW2'] = x

    @property
    def secondaryGW3(self):
        return self.template_config['secondaryGW3']
    @secondaryGW3.setter
    def secondaryGW3(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.template_config['secondaryGW3'] = x

    @property
    def secondaryGW4(self):
        return self.template_config['secondaryGW4']
    @secondaryGW4.setter
    def secondaryGW4(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.template_config['secondaryGW4'] = x

    @property
    def segmentId(self):
        return self.template_config['segmentId']
    @segmentId.setter
    def segmentId(self, x):
        self.ndfc.verify_vni(x)
        self.template_config['segmentId'] = x

    @property
    def suppressArp(self):
        return self.template_config['suppressArp']
    @suppressArp.setter
    def suppressArp(self, x):
        self.ndfc.verify_boolean(x)
        self.template_config['suppressArp'] = x

    @property
    def tag(self):
        return self.template_config['tag']
    @tag.setter
    def tag(self, x):
        self.ndfc.verify_routing_tag(x)
        self.template_config['tag'] = x

    @property
    def trmEnabled(self):
        return self.template_config['trmEnabled']
    @trmEnabled.setter
    def trmEnabled(self, x):
        self.ndfc.verify_boolean(x)
        self.template_config['trmEnabled'] = x

    @property
    def vlanId(self):
        return self.template_config['vlanId']
    @vlanId.setter
    def vlanId(self, x):
        self.ndfc.verify_vlan(x)
        self.template_config['vlanId'] = x

    @property
    def vrfDhcp(self):
        return self.template_config['vrfDhcp']
    @vrfDhcp.setter
    def vrfDhcp(self, x):
        self.template_config['vrfDhcp'] = x

    @property
    def vrfDhcp2(self):
        return self.template_config['vrfDhcp2']
    @vrfDhcp2.setter
    def vrfDhcp2(self, x):
        self.template_config['vrfDhcp2'] = x

    @property
    def vrfDhcp3(self):
        return self.template_config['vrfDhcp3']
    @vrfDhcp3.setter
    def vrfDhcp3(self, x):
        self.template_config['vrfDhcp3'] = x
