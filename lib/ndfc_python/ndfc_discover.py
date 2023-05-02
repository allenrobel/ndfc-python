"""
Initiate NDFC discovery of switches.
REST: POST
URL: https://<ip>/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/2/inventory/discover
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
    "switches":[
        {
            "ipaddr":"10.1.150.104",
            "sysName":"cvd-1313-leaf",
            "deviceIndex":"cvd-1313-leaf(FDO011218HH)",
            "platform":"N9K-C93180YC-EX",
            "version":"10.2(3)",
            "serialNumber":"FDO011218HH",
            "vdcId":0,
            "vdcMac":null
        }
    ]
}




Response from NdfcDiscover() class is shown below.
Note, this can be used as the "switches" value in the NdfcDiscover() payload:

    [
        {
            "reachable":true,
            "auth":true,
            "known":false,
            "valid":true,
            "selectable":true,
            "sysName":"cvd-1314-leaf",
            "serialNumber":"FDO011218FV",
            "vdcMac":null,
            "vdcId":0,
            "ipaddr":"10.1.150.105",
            "platform":"N9K-C93180YC-EX",
            "version":"10.2(3)",
            "lastChange":null,
            "hopCount":0,
            "deviceIndex":"cvd-1314-leaf(FDO011218FV)",
            "statusReason":"manageable"
        }
    ]
"""
import json
import sys
from time import sleep

OUR_VERSION = 103


class NdfcDiscover:
    """
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

    """

    def __init__(self, ndfc):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        # time to sleep after each request retry
        self._retry_sleep_time = 10

        # post/get base headers
        self.headers = {}
        self.headers["Content-Type"] = "application/json"

        self.payload_set = set()
        self.payload_set.add("cdpSecondTimeout")
        self.payload_set.add("fabric")
        self.payload_set.add("maxHops")
        self.payload_set.add("password")
        self.payload_set.add("preserveConfig")
        self.payload_set.add("seedIP")
        self.payload_set.add("snmpV3AuthProtocol")
        self.payload_set.add("username")

        self.payload_set_mandatory = set()
        self.payload_set_mandatory.add("fabric")
        self.payload_set_mandatory.add("password")
        self.payload_set_mandatory.add("seedIP")

        self.payload_default = {}
        self.payload_default["cdpSecondTimeout"] = 5
        self.payload_default["maxHops"] = 0
        self.payload_default["preserveConfig"] = True
        self.payload_default["snmpV3AuthProtocol"] = 0
        self.payload_default["username"] = "admin"

        self.response = ""
        self.discover_status_code = -1
        self.reachability_status_code = -1
        self.reachability_response = {}
        self.discover_response = {}

        self.init_payload()

    def init_payload(self):
        """
        Initialize the payload for the request body.
        """
        self.payload = {}
        for p in self.payload_set:
            if p in self.payload_default:
                self.payload[p] = self.payload_default[p]
            else:
                self.payload[p] = ""

    def preprocess_payload(self):
        """
        1. Set a default value for any properties that the caller has not set and
        that NDFC provides a default for.

        3. Any other fixup that may be required
        """

    def final_verification(self):
        """
        Set of final checks prior to sending the request.

        1. Verify all mandatory parameters have been set
        """
        for key in self.payload_set_mandatory:
            if self.payload[key] == "":
                self.ndfc.log.error(
                    f"exiting. call instance.{key} before calling instance.create()"
                )
                sys.exit(1)

    def is_reachable(self):
        """
        Return True if self.seedIP is reachable, per test-reachability endpoint.
        Return False otherwise.
        """
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
        """
        Issue POST to NDFC's discover endpoint with validated request.
        """
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

        self.payload["switches"] = self.reachability_response
        self.ndfc.log.info(f"self.payload {self.payload}")

        self.ndfc.post(url, self.ndfc.make_headers(), self.payload)
        self.discover_status_code = self.ndfc.response.status_code
        self.discover_response = json.loads(self.ndfc.response.text)

    def is_up(self):
        """
        Return True if self.seedIP is manageable.
        Return False otherwise.
        """
        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}/inventory/switchesByFabric"
        headers = self.ndfc.make_headers()
        self.ndfc.get(url, headers)
        response = json.loads(self.ndfc.response.text)
        our_switch = None
        for item in response:
            if "ipAddress" not in item:
                continue
            # The key 'manageable' is mispelled in the response
            if "managable" not in item:
                message = (
                    f"Skipping. 'managable' [sic] key not found in response {item}"
                )
                self.ndfc.log.error(message)
                continue
            if item["ipAddress"] == self.seedIP:
                our_switch = item
                break
        if our_switch is None:
            self.ndfc.log.warning(f"{self.seedIP} not found. Returning False")
            return False
        return our_switch["managable"]

    # top_level properties
    @property
    def cdpSecondTimeout(self):
        """
        The number of seconds allowed for CDP discovery of neighbor switches
        """
        return self.payload["cdpSecondTimeout"]

    @cdpSecondTimeout.setter
    def cdpSecondTimeout(self, x):
        self.ndfc.verify_digits(x, "cdpSecondTimeout")
        self.payload["cdpSecondTimeout"] = x

    @property
    def fabric_name(self):
        """
        The name of the fabric in which discovery will take place
        """
        return self.payload["fabric"]

    @fabric_name.setter
    def fabric_name(self, x):
        self.payload["fabric"] = x

    @property
    def maxHops(self):
        """
        The radius, in hops, from the seedIP switch, in which to
        discover neighboring switches.  If set to 0, discovery is
        limited to the seedIP switch.  If set to > 0, discovery
        will include switches X hops away from the seedIP switch.
        """
        return self.payload["maxHops"]

    @maxHops.setter
    def maxHops(self, x):
        self.ndfc.verify_digits(x, "maxHops")
        self.payload["maxHops"] = x

    @property
    def password(self):
        """
        The password of the seedIP switch and any discovered switches.
        """
        return self.payload["password"]

    @password.setter
    def password(self, x):
        self.payload["password"] = x

    @property
    def preserveConfig(self):
        """
        If set to True, the configurations on the discovered switches will be preserved.
        Else, the configurations on the discovered switches will be erased.
        """
        return self.payload["preserveConfig"]

    @preserveConfig.setter
    def preserveConfig(self, x):
        self.ndfc.verify_boolean(x)
        self.payload["preserveConfig"] = x

    @property
    def seedIP(self):
        """
        The IP address of the switch from which discovery will be initiated.
        """
        return self.payload["seedIP"]

    @seedIP.setter
    def seedIP(self, x):
        self.ndfc.verify_ipv4_address(x, "seedIP")
        self.payload["seedIP"] = x

    @property
    def snmpV3AuthProtocol(self):
        """
        The SNMPv3 authorization protocol to configure on discovered switches.
        """
        return self.payload["snmpV3AuthProtocol"]

    @snmpV3AuthProtocol.setter
    def snmpV3AuthProtocol(self, x):
        self.ndfc.verify_digits(x, "snmpV3AuthProtocol")
        self.payload["snmpV3AuthProtocol"] = x

    @property
    def username(self):
        """
        The username of the seedIP switch and any discovered switches.
        """
        return self.payload["username"]

    @username.setter
    def username(self, x):
        self.payload["username"] = x
