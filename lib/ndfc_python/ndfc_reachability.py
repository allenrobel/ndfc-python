"""
Test switch reachability (from NDFC controller perspective). The JSON payload constructed by this
class is shown below.

    { "maxHops":"0",
    "seedIP":"172.22.150.104",
    "cdpSecondTimeout":5,
    "snmpV3AuthProtocol":0,
    "username":"admin",
    "password":"myPassword",
    "preserveConfig":false   # or true
    }

Response is found in ndfc.response.text and has the following format:

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
"""
import json
import sys

OUR_VERSION = 102


class NdfcReachability:
    """
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

    """

    def __init__(self, ndfc):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        # post/get base headers
        self.headers = dict()
        self.headers["Content-Type"] = "application/json"

        self.response = None
        self.status_code = None

        self._init_payload_set()
        self._init_payload_set_mandatory()
        self._init_payload_default()
        self._init_payload()

    def _init_payload_set(self):
        self.payload_set = set()
        self.payload_set.add("cdpSecondTimeout")
        self.payload_set.add("fabric")
        self.payload_set.add("maxHops")
        self.payload_set.add("password")
        self.payload_set.add("preserveConfig")
        self.payload_set.add("seedIP")
        self.payload_set.add("snmpV3AuthProtocol")
        self.payload_set.add("username")

    def _init_payload_set_mandatory(self):
        self.payload_set_mandatory = set()
        self.payload_set_mandatory.add("fabric")
        self.payload_set_mandatory.add("seedIP")
        self.payload_set_mandatory.add("password")

    def _init_payload_default(self):
        self.payload_default = dict()
        self.payload_default["cdpSecondTimeout"] = 5
        self.payload_default["maxHops"] = 0
        self.payload_default["preserveConfig"] = True
        self.payload_default["snmpV3AuthProtocol"] = 0
        self.payload_default["username"] = "admin"

    def _init_payload(self):
        self.payload = dict()
        for p in self.payload_set:
            if p in self.payload_default:
                self.payload[p] = self.payload_default[p]
            else:
                self.payload[p] = ""

    def _preprocess_payload(self):
        """
        1. Set a default value for any properties that the caller has not set and that
        NDFC provides a default for.

        2. Copy top-level property values (that need it) into their respective
        template_config properties.

        3. Any other fixup that may be required
        """

    def _final_verification(self):
        for param in self.payload_set_mandatory:
            if self.payload[param] == "":
                self.ndfc.log.error(
                    f"exiting. call instance.{param} before calling instance.create()"
                )
                sys.exit(1)

    def reachability(self):
        self._preprocess_payload()
        self._final_verification()

        url = (
            f"{self.ndfc.url_control_fabrics}/{self.fabric}/inventory/test-reachability"
        )

        headers = self.headers
        headers["Authorization"] = self.ndfc.bearer_token

        self.ndfc.post(url, headers, self.payload)
        self.status_code = self.ndfc.response.status_code
        self.response = json.loads(self.ndfc.response.text)

    # top_level properties
    @property
    def cdpSecondTimeout(self):
        return self.payload["cdpSecondTimeout"]

    @cdpSecondTimeout.setter
    def cdpSecondTimeout(self, param):
        self.ndfc.verify_digits(param, "cdpSecondTimeout")
        self.payload["cdpSecondTimeout"] = param

    @property
    def fabric(self):
        return self.payload["fabric"]

    @fabric.setter
    def fabric(self, param):
        self.payload["fabric"] = param

    @property
    def maxHops(self):
        return self.payload["maxHops"]

    @maxHops.setter
    def maxHops(self, param):
        self.ndfc.verify_digits(param, "maxHops")
        self.payload["maxHops"] = param

    @property
    def password(self):
        return self.payload["password"]

    @password.setter
    def password(self, param):
        self.payload["password"] = param

    @property
    def preserveConfig(self):
        return self.template_config["preserveConfig"]

    @preserveConfig.setter
    def preserveConfig(self, param):
        self.ndfc.verify_boolean(param)
        self.template_config["preserveConfig"] = param

    @property
    def seedIP(self):
        return self.payload["seedIP"]

    @seedIP.setter
    def seedIP(self, param):
        self.ndfc.verify_ipv4_address(param, "seedIP")
        self.payload["seedIP"] = param

    @property
    def snmpV3AuthProtocol(self):
        return self.payload["snmpV3AuthProtocol"]

    @snmpV3AuthProtocol.setter
    def snmpV3AuthProtocol(self, param):
        self.ndfc.verify_digits(param, "snmpV3AuthProtocol")
        self.payload["snmpV3AuthProtocol"] = param

    @property
    def username(self):
        return self.payload["username"]

    @username.setter
    def username(self, param):
        self.payload["username"] = param
