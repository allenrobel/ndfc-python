our_version = 100
import json
'''
Discover switch.
REST: POST
URL: https://10.195.225.167/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/2/inventory/discover
PAYLOAD:  The JSON payload constructed by the NdfcReachability() class is shown below.

    { "maxHops":"0",
    "seedIP":"172.22.150.104",
    "cdpSecondTimeout":5,
    "snmpV3AuthProtocol":0,
    "username":"admin",
    "password":"myPassword",
    "preserveConfig":false   # or true
    }

{
    "maxHops":"0",
    "seedIP":"172.22.150.104",
    "cdpSecondTimeout":5,
    "snmpV3AuthProtocol":0,
    "username":"admin",
    "password":"myPassword",
    "preserveConfig":false,
    "switches":[{"ipaddr":"172.22.150.104","sysName":"cvd-1313-leaf","deviceIndex":"cvd-1313-leaf(FDO211218HH)","platform":"N9K-C93180YC-EX","version":"10.2(3)","serialNumber":"FDO211218HH","vdcId":0,"vdcMac":null}]}




Response from NdfcReachability() class is shown below.  Note, this can be used as the "switches" value in the NdfcDiscover() payload:

    [
        {
            "reachable":true,
            "auth":true,
            "known":false,
            "valid":true,
            "selectable":true,
            "sysName":"cvd-1314-leaf",
            "serialNumber":"FDO211218FV",
            "vdcMac":null,
            "vdcId":0,
            "ipaddr":"172.22.150.105",
            "platform":"N9K-C93180YC-EX",
            "version":"10.2(3)",
            "lastChange":null,
            "hopCount":0,
            "deviceIndex":"cvd-1314-leaf(FDO211218FV)",
            "statusReason":"manageable"
        }
    ]
'''
class NdfcDiscover(object):
    '''
    Tests switch reachability (from NDFC controller perspective).
    Populates:
        self.result = result code from controller
        self.response = See response in above docstring

    Example

    instance = NdfcReachability(ndfc)
    instance.seedIP = 'foo'
    instance.cdpSecondTimeout = 10
    instance.username = 'admin'
    instance.password = 'myPassword'
    instance.reachability()
    print('response: {}'.format(instance.response))

    '''
    def __init__(self, ndfc):
        self.lib_version = our_version
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        # post/get base headers
        self.headers = dict()
        self.headers['Content-Type'] = 'application/json'

        self.payload_set = set()
        self.payload_set.add('cdpSecondTimeout')
        self.payload_set.add('fabric')
        self.payload_set.add('maxHops')
        self.payload_set.add('password')
        self.payload_set.add('preserveConfig')
        self.payload_set.add('seedIP')
        self.payload_set.add('snmpV3AuthProtocol')
        self.payload_set.add('username')

        self.payload_set_mandatory = set()
        self.payload_set_mandatory.add('fabric')
        self.payload_set_mandatory.add('password')
        self.payload_set_mandatory.add('seedIP')

        self.payload_default = dict()
        self.payload_default['cdpSecondTimeout'] = 5
        self.payload_default['maxHops'] = 0
        self.payload_default['preserveConfig'] = True
        self.payload_default['snmpV3AuthProtocol'] = 0
        self.payload_default['username'] = 'admin'

        self.response = ""
        self.discover_status_code = -1
        self.reachability_status_code = -1
        self.reachability_response = dict()
        self.discover_response = dict()

        self.init_payload()

    def init_payload(self):
        self.payload = dict()
        for p in self.payload_set:
            if p in self.payload_default:
                self.payload[p] = self.payload_default[p]
            else:
                self.payload[p] = ""

    def preprocess_payload(self):
        '''
        1. Set a default value for any properties that the caller has not set and that NDFC provides a default for. 

        2. Copy top-level property values (that need it) into their respective template_config properties.

        3. Any other fixup that may be required
        '''
        pass

    def final_verification(self):
        for p in self.payload_set_mandatory:
            if self.payload[p] == "":
                self.ndfc.log.error('exiting. call instance.{} before calling instance.create()'.format(p))
                exit(1)

    def discover(self):
        self.preprocess_payload()
        self.final_verification()

        url = 'https://{}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{}/inventory/test-reachability'.format(
            self.ndfc.ip,
            self.fabric)

        headers = self.headers
        headers['Authorization'] = self.ndfc.bearer_token

        self.ndfc.post(url, headers, self.payload)
        self.reachability_status_code = self.ndfc.response.status_code
        self.reachability_response = json.loads(self.ndfc.response.text)

        if self.reachability_status_code != 200:
            self.ndfc.log.error('exiting. Switch {} is not reachable. status_code: {}, response: {}'.format(
                self.seedIP,
                self.reachability_status_code,
                self.reachability_response))
            exit(1)

        url = 'https://{}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{}/inventory/discover'.format(
            self.ndfc.ip,
            self.fabric)

        self.payload['switches'] = self.reachability_response
        self.ndfc.log.info('self.payload {}'.format(self.payload))

        self.ndfc.post(url, headers, self.payload)
        self.discover_status_code = self.ndfc.response.status_code
        self.discover_response = json.loads(self.ndfc.response.text)

    # top_level properties
    @property
    def cdpSecondTimeout(self):
        return self.payload['cdpSecondTimeout']
    @cdpSecondTimeout.setter
    def cdpSecondTimeout(self, x):
        self.ndfc.verify_digits(x, 'cdpSecondTimeout')
        self.payload['cdpSecondTimeout'] = x

    @property
    def fabric(self):
        return self.payload['fabric']
    @fabric.setter
    def fabric(self, x):
        self.payload['fabric'] = x

    @property
    def maxHops(self):
        return self.payload['maxHops']
    @maxHops.setter
    def maxHops(self, x):
        self.ndfc.verify_digits(x, 'maxHops')
        self.payload['maxHops'] = x

    @property
    def password(self):
        return self.payload['password']
    @password.setter
    def password(self, x):
        self.payload['password'] = x

    @property
    def preserveConfig(self):
        return self.template_config['preserveConfig']
    @preserveConfig.setter
    def preserveConfig(self, x):
        self.ndfc.verify_boolean(x)
        self.payload['preserveConfig'] = x

    @property
    def seedIP(self):
        return self.payload['seedIP']
    @seedIP.setter
    def seedIP(self, x):
        self.ndfc.verify_ipv4_address(x, 'seedIP')
        self.payload['seedIP'] = x

    @property
    def snmpV3AuthProtocol(self):
        return self.payload['snmpV3AuthProtocol']
    @snmpV3AuthProtocol.setter
    def snmpV3AuthProtocol(self, x):
        self.ndfc.verify_digits(x, 'snmpV3AuthProtocol')
        self.payload['snmpV3AuthProtocol'] = x

    @property
    def username(self):
        return self.payload['username']
    @username.setter
    def username(self, x):
        self.payload['username'] = x
