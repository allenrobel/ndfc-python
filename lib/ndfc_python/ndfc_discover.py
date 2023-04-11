import sys
import json
from time import sleep
OUR_VERSION = 102
'''
Discover switch.
REST: POST
URL: https://10.195.225.167/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/2/inventory/discover
PAYLOAD:  The JSON payload constructed by the NdfcDiscover() class is shown below.

    { "maxHops":"0",
    "seedIP":"10.1.150.104",
    "cdpSecondTimeout":5,
    "snmpV3AuthProtocol":0,
    "username":"admin",
    "password":"myPassword",
    "preserveConfig":false   # or true
    }

{
    "maxHops":"0",
    "seedIP":"10.1.150.104",
    "cdpSecondTimeout":5,
    "snmpV3AuthProtocol":0,
    "username":"admin",
    "password":"myPassword",
    "preserveConfig":false,
    "switches":[{"ipaddr":"10.1.150.104","sysName":"cvd-1313-leaf","deviceIndex":"cvd-1313-leaf(FDO211218HH)","platform":"N9K-C93180YC-EX","version":"10.2(3)","serialNumber":"FDO211218HH","vdcId":0,"vdcMac":null}]}




Response from NdfcDiscover() class is shown below.  Note, this can be used as the "switches" value in the NdfcDiscover() payload:

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
            "ipaddr":"10.1.150.105",
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
    Discover switches
    Populates:
        self.result = result code from controller
        self.response = See response in above docstring

    Example

    instance = NdfcDiscover(ndfc)
    instance.seedIP = '10.1.1.1'
    instance.cdpSecondTimeout = 10
    instance.username = 'admin'
    instance.password = 'myPassword'
    instance.discover()
    print('response: {}'.format(instance.response))

    '''
    def __init__(self, ndfc):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        # time to sleep after each request retry
        self._retry_sleep_time = 10

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
        for key in self.payload_set_mandatory:
            if self.payload[key] == "":
                self.ndfc.log.error(
                    f"exiting. call instance.{key} before calling instance.create()"
                )
                sys.exit(1)

    def is_reachable(self):
        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}/inventory/test-reachability"
        self.ndfc.post(url, self.ndfc.make_headers(), self.payload)
        self.reachability_status_code = self.ndfc.response.status_code
        self.reachability_response = json.loads(self.ndfc.response.text)

        if self.reachability_status_code != 200:
            msg = f"Switch {self.seedIP} is not reachable."
            msg += f" status_code: {self.reachability_status_code}"
            msg += f" response: {self.reachability_response}"
            self.ndfc.log.error(msg)
            return False
        return True

    def discover(self):
        self.preprocess_payload()
        self.final_verification()
        retries = 4
        while self.is_reachable() is False and retries > 0:
            sleep(self._retry_sleep_time)
            retries -= 1
        if self.is_reachable() is False:
            self.ndfc.log.error(f"Exiting. {self.seedIP} not reachable after 5 retries")
            sys.exit(1)

        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}/inventory/discover"

        self.payload['switches'] = self.reachability_response
        self.ndfc.log.info('self.payload {}'.format(self.payload))

        self.ndfc.post(url, self.ndfc.make_headers(), self.payload)
        self.discover_status_code = self.ndfc.response.status_code
        self.discover_response = json.loads(self.ndfc.response.text)

    def is_up(self):
        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}/inventory/switchesByFabric"
        headers = self.ndfc.make_headers()
        self.ndfc.get(url, headers)
        response = json.loads(self.ndfc.response.text)
        found = None
        for item in response:
            if "ipAddress" not in item:
                continue
            # The key 'manageable' is mispelled in the response
            if "managable" not in item:
                self.ndfc.log.error(f"skipping due to 'managable [sic]' not in response {item}")
                continue
            if item["ipAddress"] == self.seedIP:
                found = item
                break
        if found is None:
            self.ndfc.log.warning(f"{self.seedIP} not found. Returning False")
            return False
        return item["managable"]

    # top_level properties
    @property
    def cdpSecondTimeout(self):
        return self.payload['cdpSecondTimeout']
    @cdpSecondTimeout.setter
    def cdpSecondTimeout(self, x):
        self.ndfc.verify_digits(x, 'cdpSecondTimeout')
        self.payload['cdpSecondTimeout'] = x

    @property
    def fabric_name(self):
        return self.payload['fabric']
    @fabric_name.setter
    def fabric_name(self, x):
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
