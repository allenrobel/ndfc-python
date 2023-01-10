our_version = 100
import json
class NdfcFabricSite(object):
    '''
    Create site/child fabrics.

    Example create operation:

    instance = NdfcFabricSite(ndfc)
    instance.fabric = 'bang'
    instance.BGP_AS = 65011
    instance.REPLICATION_MODE = 'Ingress'
    instance.create()

    TODO: Need a delete() method
    '''
    def __init__(self, ndfc):
        self.lib_version = our_version
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        self.properties_set = set()
        self.properties_set.add('fabric')

        self.properties_mandatory_set = set()
        self.properties_mandatory_set.add('fabric')

        self.properties_default = dict()


        self.nv_pairs_set = set()
        self.nv_pairs_set.add('ANYCAST_RP_IP_RANGE')
        self.nv_pairs_set.add('BGP_AS')
        self.nv_pairs_set.add('DCI_SUBNET_RANGE')
        self.nv_pairs_set.add('FABRIC_MTU')
        self.nv_pairs_set.add('LOOPBACK0_IP_RANGE')
        self.nv_pairs_set.add('LOOPBACK1_IP_RANGE')
        self.nv_pairs_set.add('REPLICATION_MODE')
        self.nv_pairs_set.add('SUBNET_RANGE')
        self.nv_pairs_set.add('network_extension_template')
        self.nv_pairs_set.add('vrf_extension_template')

        self.nv_pairs_default = dict()
        self.nv_pairs_default['ANYCAST_RP_IP_RANGE'] = ''
        self.nv_pairs_default['DCI_SUBNET_RANGE'] = '10.33.0.0/16'
        self.nv_pairs_default['FABRIC_MTU'] = '9216'
        self.nv_pairs_default['LOOPBACK0_IP_RANGE'] = '10.2.0.0/22'
        self.nv_pairs_default['LOOPBACK1_IP_RANGE'] = '10.3.0.0/22'
        self.nv_pairs_default['REPLICATION_MODE'] = 'Ingress'
        self.nv_pairs_default['SUBNET_RANGE'] = '10.4.0.0/16'
        self.nv_pairs_default['network_extension_template'] = 'Default_Network_Extension_Universal'
        self.nv_pairs_default['vrf_extension_template'] = 'Default_VRF_Extension_Universal'

        self.nv_pairs_mandatory_set = set()
        self.nv_pairs_mandatory_set = self.nv_pairs_set.difference(
            self.nv_pairs_default
        )

        # All properties, except fabric, live here
        self.nvPairs = dict()

        self.init_properties()
        self.init_nvPairs()

    def init_properties(self):
        self.properties = dict()
        for p in self.properties_set:
            if p in self.properties_default:
                self.properties[p] = self.properties_default[p]
            else:
                self.properties[p] = ""

    def init_nvPairs(self):
        for p in self.nv_pairs_set:
            if p in self.nv_pairs_default:
                self.nvPairs[p] = self.nv_pairs_default[p]
            else:
                self.nvPairs[p] = ""

    def preprocess_properties(self):
        '''
        1. Align the properties to the expectations of NDFC 
        '''
        pass

    def final_verification(self):
        for p in self.properties_mandatory_set:
            if self.properties[p] == "":
                self.ndfc.log.error('exiting. call instance.{} before calling instance.post()'.format(p))
                exit(1)
        for p in self.nv_pairs_mandatory_set:
            if self.nvPairs[p] == "":
                self.ndfc.log.error('exiting. call instance.{} before calling instance.post()'.format(p))
                exit(1)

    def create(self):
        self.final_verification()
        self.preprocess_properties()

        url = 'https://{}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{}/Easy_Fabric'.format(self.ndfc.ip, self.fabric)

        headers = dict()
        headers['Authorization'] = self.ndfc.bearer_token
        headers['Content-Type'] = 'application/json'

        self.ndfc.post(url, headers, self.nvPairs)

    # top_level properties
    @property
    def fabric(self):
        return self.properties['fabric']
    @fabric.setter
    def fabric(self, x):
        self.properties['fabric'] = x

    # nvPairs
    @property
    def ANYCAST_RP_IP_RANGE(self):
        return self.nvPairs['ANYCAST_RP_IP_RANGE']
    @ANYCAST_RP_IP_RANGE.setter
    def ANYCAST_RP_IP_RANGE(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.nvPairs['ANYCAST_RP_IP_RANGE'] = x

    @property
    def BGP_AS(self):
        return self.nvPairs['BGP_AS']
    @BGP_AS.setter
    def BGP_AS(self, x):
        self.ndfc.verify_bgp_asn(x)
        self.nvPairs['BGP_AS'] = x

    @property
    def DCI_SUBNET_RANGE(self):
        return self.nvPairs['DCI_SUBNET_RANGE']
    @DCI_SUBNET_RANGE.setter
    def DCI_SUBNET_RANGE(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.nvPairs['DCI_SUBNET_RANGE'] = x

    @property
    def FABRIC_MTU(self):
        return self.nvPairs['FABRIC_MTU']
    @FABRIC_MTU.setter
    def FABRIC_MTU(self, x):
        self.nvPairs['FABRIC_MTU'] = x

    @property
    def LOOPBACK0_IP_RANGE(self):
        return self.nvPairs['LOOPBACK0_IP_RANGE']
    @LOOPBACK0_IP_RANGE.setter
    def LOOPBACK0_IP_RANGE(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.nvPairs['LOOPBACK0_IP_RANGE'] = x

    @property
    def LOOPBACK1_IP_RANGE(self):
        return self.nvPairs['LOOPBACK1_IP_RANGE']
    @LOOPBACK1_IP_RANGE.setter
    def LOOPBACK1_IP_RANGE(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.nvPairs['LOOPBACK1_IP_RANGE'] = x

    @property
    def REPLICATION_MODE(self):
        return self.nvPairs['REPLICATION_MODE']
    @REPLICATION_MODE.setter
    def REPLICATION_MODE(self, x):
        self.ndfc.verify_replication_mode(x)
        self.nvPairs['REPLICATION_MODE'] = x

    @property
    def SUBNET_RANGE(self):
        return self.nvPairs['SUBNET_RANGE']
    @SUBNET_RANGE.setter
    def SUBNET_RANGE(self, x):
        self.ndfc.verify_ipv4_address_with_prefix(x)
        self.nvPairs['SUBNET_RANGE'] = x
