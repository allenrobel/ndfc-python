our_version = 100
import json
class NdfcVrf(object):
    def __init__(self, ndfc):
        self.lib_version = our_version
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        self.payload_set = set()
        self.payload_set.add('displayName')
        self.payload_set.add('fabric')
        self.payload_set.add('serviceVrfTemplate')
        self.payload_set.add('source')
        self.payload_set.add('vrfExtensionTemplate')
        self.payload_set.add('vrfId')
        self.payload_set.add('vrfName')
        self.payload_set.add('vrfTemplate')

        self.mandatory_payload_set = set()
        self.mandatory_payload_set.add('fabric')
        self.mandatory_payload_set.add('vrfId')
        self.mandatory_payload_set.add('vrfName')

        self.mandatory_template_config_set = set()
        #self.mandatory_template_config_set.add('asn')
        self.mandatory_template_config_set.add('vrfVlanId')

        self.payload_default = dict()
        self.payload_default['vrfExtensionTemplate'] = 'Default_VRF_Extension_Universal'
        self.payload_default['vrfTemplate'] = 'Default_VRF_Universal'

        self.vrf_template_config_set = set()
        self.vrf_template_config_set.add('advertiseHostRouteFlag')
        self.vrf_template_config_set.add('advertiseDefaultRouteFlag')
        # self.vrf_template_config_set.add('asn')
        self.vrf_template_config_set.add('bgpPassword')
        self.vrf_template_config_set.add('bgpPasswordKeyType')
        self.vrf_template_config_set.add('configureStaticDefaultRouteFlag')
        self.vrf_template_config_set.add('ENABLE_NETFLOW')
        self.vrf_template_config_set.add('ipv6LinkLocalFlag')
        self.vrf_template_config_set.add('isRPExternal')
        self.vrf_template_config_set.add('loopbackNumber')
        self.vrf_template_config_set.add('L3VniMcastGroup')
        self.vrf_template_config_set.add('maxBgpPaths')
        self.vrf_template_config_set.add('maxIbgpPaths')
        self.vrf_template_config_set.add('multicastGroup')
        self.vrf_template_config_set.add('mtu')
        self.vrf_template_config_set.add('NETFLOW_MONITOR')
        self.vrf_template_config_set.add('nveId')
        self.vrf_template_config_set.add('rpAddress')
        self.vrf_template_config_set.add('tag')
        self.vrf_template_config_set.add('trmEnabled')
        self.vrf_template_config_set.add('trmBGWMSiteEnabled')
        self.vrf_template_config_set.add('vrfName')
        self.vrf_template_config_set.add('vrfDescription')
        self.vrf_template_config_set.add('vrfIntfDescription')
        self.vrf_template_config_set.add('vrfRouteMap')
        self.vrf_template_config_set.add('vrfSegmentId')
        self.vrf_template_config_set.add('vrfVlanId')
        self.vrf_template_config_set.add('vrfVlanName')

        self.vrf_template_config_default = dict()
        self.vrf_template_config_default['advertiseDefaultRouteFlag'] = True
        self.vrf_template_config_default['advertiseHostRouteFlag'] = False
        self.vrf_template_config_default['bgpPasswordKeyType'] = 3
        self.vrf_template_config_default['configureStaticDefaultRouteFlag'] = True
        self.vrf_template_config_default['ENABLE_NETFLOW'] = False
        self.vrf_template_config_default['ipv6LinkLocalFlag'] = True
        self.vrf_template_config_default['isRPExternal'] = False
        self.vrf_template_config_default['mtu'] = 9216
        self.vrf_template_config_default['nveId'] = 1
        self.vrf_template_config_default['tag'] = '12345'
        self.vrf_template_config_default['vrfRouteMap'] = 'FABRIC-RMAP-REDIST-SUBNET'
        self.vrf_template_config_default['maxBgpPaths'] = '1'
        self.vrf_template_config_default['maxIbgpPaths'] = '2'
        self.vrf_template_config_default['trmEnabled'] = False
        self.vrf_template_config_default['trmBGWMSiteEnabled'] = False

        self.init_payload()
        self.init_vrf_template_config()

    def init_payload(self):
        self.payload = dict()
        for p in self.payload_set:
            if p in self.payload_default:
                self.payload[p] = self.payload_default[p]
            else:
                self.payload[p] = ""

    def init_vrf_template_config(self):
        self.vrf_template_config = dict()
        for p in self.vrf_template_config_set:
            if p in self.vrf_template_config_default:
                self.vrf_template_config[p] = self.vrf_template_config_default[p]
            else:
                self.vrf_template_config[p] = ""

    def final_verification(self):
        for p in self.mandatory_payload_set:
            if self.payload[p] == "":
                self.ndfc.log.error('exiting. call instance.{} before calling instance.post()'.format(p))
                exit(1)
        for p in self.mandatory_template_config_set:
            if self.vrf_template_config[p] == "":
                self.ndfc.log.error('exiting. call instance.{} before calling instance.post()'.format(p))
                exit(1)

    def post(self):
        self.final_verification()

        url = 'https://{}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{}/vrfs'.format(self.ndfc.ip, self.fabric)

        headers = dict()
        headers['Authorization'] = self.ndfc.bearer_token
        headers['Content-Type'] = 'application/json'

        if self.payload['displayName'] == "":
            self.payload['displayName'] = self.vrfName

        for p in self.payload:
            self.payload[p] = str(self.payload[p])
        for p in self.vrf_template_config:
            if type(self.vrf_template_config[p]) == type(bool()):
                self.vrf_template_config[p] = str(self.vrf_template_config[p]).lower()
            else:
                self.vrf_template_config[p] = str(self.vrf_template_config[p])

        self.vrf_template_config['vrfName'] = self.vrfName
        self.vrf_template_config['vrfSegmentId'] = self.vrfId

        self.payload['vrfTemplateConfig'] = json.dumps(self.vrf_template_config)

        self.ndfc.post(url, headers, self.payload)

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
    def vrfExtensionTemplate(self):
        return self.payload['vrfExtensionTemplate']
    @vrfExtensionTemplate.setter
    def vrfExtensionTemplate(self, x):
        self.payload['vrfExtensionTemplate'] = x

    @property
    def vrfId(self):
        return self.payload['vrfId']
    @vrfId.setter
    def vrfId(self, x):
        self.payload['vrfId'] = x

    @property
    def vrfName(self):
        return self.payload['vrfName']
    @vrfName.setter
    def vrfName(self, x):
        self.payload['vrfName'] = x

    @property
    def vrfTemplate(self):
        return self.payload['vrfTemplate']
    @vrfTemplate.setter
    def vrfTemplate(self, x):
        self.payload['vrfTemplate'] = x

    @property
    def serviceVrfTemplate(self):
        return self.payload['serviceVrfTemplate']
    @serviceVrfTemplate.setter
    def serviceVrfTemplate(self, x):
        self.payload['serviceVrfTemplate'] = x

    @property
    def source(self):
        return self.payload['source']
    @source.setter
    def source(self, x):
        self.payload['source'] = x


    # vrf_template_config properties

    @property
    def advertiseHostRouteFlag(self):
        return self.vrf_template_config['advertiseHostRouteFlag']
    @advertiseHostRouteFlag.setter
    def advertiseHostRouteFlag(self, x):
        self.ndfc.verify_boolean(x)
        self.vrf_template_config['advertiseHostRouteFlag'] = x

    @property
    def advertiseDefaultRouteFlag(self):
        return self.vrf_template_config['advertiseDefaultRouteFlag']
    @advertiseDefaultRouteFlag.setter
    def advertiseDefaultRouteFlag(self, x):
        self.ndfc.verify_boolean(x)
        self.vrf_template_config['advertiseDefaultRouteFlag'] = x

    # @property
    # def asn(self):
    #     return self.vrf_template_config['asn']
    # @asn.setter
    # def asn(self, x):
    #     self.verify_bgp_asn(x)
    #     self.vrf_template_config['asn'] = x

    @property
    def bgpPassword(self):
        return self.vrf_template_config['bgpPassword']
    @bgpPassword.setter
    def bgpPassword(self, x):
        self.vrf_template_config['bgpPassword'] = x

    @property
    def bgpPasswordKeyType(self):
        return self.vrf_template_config['bgpPasswordKeyType']
    @bgpPasswordKeyType.setter
    def bgpPasswordKeyType(self, x):
        self.ndfc.verify_bgp_password_key_type(x, 'bgpPasswordKeyType')
        self.vrf_template_config['bgpPasswordKeyType'] = x

    @property
    def configureStaticDefaultRouteFlag(self):
        return self.vrf_template_config['configureStaticDefaultRouteFlag']
    @configureStaticDefaultRouteFlag.setter
    def configureStaticDefaultRouteFlag(self, x):
        self.ndfc.verify_boolean(x)
        self.vrf_template_config['configureStaticDefaultRouteFlag'] = x

    @property
    def ENABLE_NETFLOW(self):
        return self.vrf_template_config['ENABLE_NETFLOW']
    @ENABLE_NETFLOW.setter
    def ENABLE_NETFLOW(self, x):
        self.ndfc.verify_boolean(x)
        self.vrf_template_config['ENABLE_NETFLOW'] = x

    @property
    def ipv6LinkLocalFlag(self):
        return self.vrf_template_config['ipv6LinkLocalFlag']
    @ipv6LinkLocalFlag.setter
    def ipv6LinkLocalFlag(self, x):
        self.ndfc.verify_boolean(x)
        self.vrf_template_config['ipv6LinkLocalFlag'] = x

    @property
    def isRPExternal(self):
        return self.vrf_template_config['isRPExternal']
    @isRPExternal.setter
    def isRPExternal(self, x):
        self.ndfc.verify_boolean(x)
        self.vrf_template_config['isRPExternal'] = x

    @property
    def L3VniMcastGroup(self):
        return self.vrf_template_config['L3VniMcastGroup']
    @L3VniMcastGroup.setter
    def L3VniMcastGroup(self, x):
        self.ndfc.verify_ipv4_multicast_address(x, '{}.L3VniMcastGroup.setter'.format(self.class_name))
        self.vrf_template_config['L3VniMcastGroup'] = x

    @property
    def loopbackNumber(self):
        return self.vrf_template_config['loopbackNumber']
    @loopbackNumber.setter
    def loopbackNumber(self, x):
        self.ndfc.verify_loopback_id(x)
        self.vrf_template_config['loopbackNumber'] = x

    @property
    def maxBgpPaths(self):
        return self.vrf_template_config['maxBgpPaths']
    @maxBgpPaths.setter
    def maxBgpPaths(self, x):
        self.ndfc.verify_max_bgp_paths(x, '{}.maxBgpPaths.setter'.format(self.class_name))
        self.vrf_template_config['maxBgpPaths'] = x

    @property
    def maxIbgpPaths(self):
        return self.vrf_template_config['maxIbgpPaths']
    @maxIbgpPaths.setter
    def maxIbgpPaths(self, x):
        self.ndfc.verify_max_bgp_paths(x, '{}.maxIbgpPaths.setter'.format(self.class_name))
        self.vrf_template_config['maxIbgpPaths'] = x

    @property
    def multicastGroup(self):
        return self.vrf_template_config['multicastGroup']
    @multicastGroup.setter
    def multicastGroup(self, x):
        self.ndfc.verify_ipv4_multicast_address(x, '{}.multicastGroup.setter'.format(self.class_name))
        self.vrf_template_config['multicastGroup'] = x

    @property
    def mtu(self):
        return self.vrf_template_config['mtu']
    @mtu.setter
    def mtu(self, x):
        self.ndfc.verify_mtu(x, '{}.mtu.setter'.format(self.class_name))
        self.vrf_template_config['mtu'] = x

    @property
    def NETFLOW_MONITOR(self):
        return self.vrf_template_config['NETFLOW_MONITOR']
    @NETFLOW_MONITOR.setter
    def NETFLOW_MONITOR(self, x):
        self.vrf_template_config['NETFLOW_MONITOR'] = x

    @property
    def nveId(self):
        return self.vrf_template_config['nveId']
    @nveId.setter
    def nveId(self, x):
        self.ndfc.verify_nve_id(x, '{}.nveId.setter'.format(self.class_name))
        self.vrf_template_config['nveId'] = x

    @property
    def rpAddress(self):
        return self.vrf_template_config['rpAddress']
    @rpAddress.setter
    def rpAddress(self, x):
        self.ndfc.verify_ipv4_address(x)
        self.vrf_template_config['rpAddress'] = x

    @property
    def tag(self):
        return self.vrf_template_config['tag']
    @tag.setter
    def tag(self, x):
        self.ndfc.verify_routing_tag(x)
        self.vrf_template_config['tag'] = x

    @property
    def trmBGWMSiteEnabled(self):
        return self.vrf_template_config['trmBGWMSiteEnabled']
    @trmBGWMSiteEnabled.setter
    def trmBGWMSiteEnabled(self, x):
        self.ndfc.verify_boolean(x)
        self.vrf_template_config['trmBGWMSiteEnabled'] = x

    @property
    def trmEnabled(self):
        return self.vrf_template_config['trmEnabled']
    @trmEnabled.setter
    def trmEnabled(self, x):
        self.ndfc.verify_boolean(x)
        self.vrf_template_config['trmEnabled'] = x

    @property
    def vrfDescription(self):
        return self.vrf_template_config['vrfDescription']
    @vrfDescription.setter
    def vrfDescription(self, x):
        self.vrf_template_config['vrfDescription'] = x

    @property
    def vrfIntfDescription(self):
        return self.vrf_template_config['vrfIntfDescription']
    @vrfIntfDescription.setter
    def vrfIntfDescription(self, x):
        self.vrf_template_config['vrfIntfDescription'] = x

    @property
    def vrfRouteMap(self):
        return self.vrf_template_config['vrfRouteMap']
    @vrfRouteMap.setter
    def vrfRouteMap(self, x):
        self.vrf_template_config['vrfRouteMap'] = x

    @property
    def vrfVlanId(self):
        return self.vrf_template_config['vrfVlanId']
    @vrfVlanId.setter
    def vrfVlanId(self, x):
        self.ndfc.verify_vrf_vlan_id(x)
        self.vrf_template_config['vrfVlanId'] = x

    @property
    def vrfVlanName(self):
        return self.vrf_template_config['vrfVlanName']
    @vrfVlanName.setter
    def vrfVlanName(self, x):
        self.vrf_template_config['vrfVlanName'] = x

