"""
Name: ndfc_reachability.py
Description: Test switch reachability (from NDFC controller perspective).

The JSON payload constructed by this class is shown below.

{
    "maxHops":"0",
    "seedIP":"10.1.150.104",
    "cdpSecondTimeout":5,
    "snmpV3AuthProtocol":0,
    "username":"admin",
    "password":"myPassword",
    "preserveConfig":false   # or true
}

In self.reachability(), self.response is populated with the contents of
ndfc.response.text, and has the following format:

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
"""
import json
import sys
from ipaddress import AddressValueError

OUR_VERSION = 105


class NdfcReachability:
    """
    Tests switch reachability (from NDFC controller perspective).
    Populates:
        self.result = result code from controller
        self.response = See response in above docstring

    Example

    instance = NdfcReachability(ndfc)
    instance.seed_ip = 'foo'
    instance.cdp_second_timeout = 10
    instance.username = 'admin'
    instance.password = 'myPassword'
    instance.reachability()
    print('response: {}'.format(instance.response))

    """

    def __init__(self, ndfc):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        self.response = None
        self.status_code = None

        self._init_payload_set()
        self._init_payload_set_mandatory()
        self._init_payload_default()
        self._init_payload()

    def _init_payload_set(self):
        """
        Initialize a set containing all payload keys
        """
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
        """
        Initialize a set containing mandatory payload keys
        """
        self.payload_set_mandatory = set()
        self.payload_set_mandatory.add("fabric")
        self.payload_set_mandatory.add("password")
        self.payload_set_mandatory.add("seedIP")
        self.payload_set_mandatory.add("username")

    def _init_payload_default(self):
        """
        Initialize default payload values
        """
        self.payload_default = {}
        self.payload_default["cdpSecondTimeout"] = 5
        self.payload_default["maxHops"] = 0
        self.payload_default["preserveConfig"] = True
        self.payload_default["snmpV3AuthProtocol"] = 0
        self.payload_default["username"] = self.ndfc.username
        self.payload_default["password"] = self.ndfc.password

    def _init_payload(self):
        """
        Initialize the REST payload
        """
        self.payload = {}
        for param in self.payload_set:
            if param in self.payload_default:
                self.payload[param] = self.payload_default[param]
            else:
                self.payload[param] = ""

    def _preprocess_payload(self):
        """
        1. Set a default value for any properties that the caller has not set
        and that NDFC provides a default for.

        2. Copy top-level property values (that need it) into their respective
        template_config properties.

        3. Any other fixup that may be required
        """

    def _final_verification(self):
        """
        verify all mandatory parameters are set
        """
        for param in self.payload_set_mandatory:
            if self.payload[param] == "":
                msg = f"exiting. call instance.{param} before "
                msg += "calling instance.create()"
                self.ndfc.log.error(msg)
                sys.exit(1)

    def reachability(self):
        """
        Send a POST request to NDFC to the test-reachability endpoint
        """
        self._preprocess_payload()
        self._final_verification()

        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}"
        url += "inventory/test-reachability"

        self.ndfc.post(url, self.ndfc.make_headers(), self.payload)
        self.status_code = self.ndfc.response.status_code
        self.response = json.loads(self.ndfc.response.text)

    # top_level properties
    @property
    def cdp_second_timeout(self):
        """
        return the current payload value of cdp_second_timeout
        """
        return self.payload["cdpSecondTimeout"]

    @cdp_second_timeout.setter
    def cdp_second_timeout(self, param):
        self.ndfc.verify_digits(param, "cdp_second_timeout")
        self.payload["cdpSecondTimeout"] = param

    @property
    def fabric_name(self):
        """
        return the current payload value of fabric
        """
        return self.payload["fabric"]

    @fabric_name.setter
    def fabric_name(self, param):
        self.payload["fabric"] = param

    @property
    def max_hops(self):
        """
        return the current payload value of max_hops
        """
        return self.payload["maxHops"]

    @max_hops.setter
    def max_hops(self, param):
        self.ndfc.verify_digits(param, "max_hops")
        self.payload["maxHops"] = param

    @property
    def password(self):
        """
        return the current payload value of password
        """
        return self.payload["password"]

    @password.setter
    def password(self, param):
        self.payload["password"] = param

    @property
    def preserve_config(self):
        """
        return the current payload value of preserve_config
        """
        return self.payload["preserveConfig"]

    @preserve_config.setter
    def preserve_config(self, param):
        try:
            self.ndfc.verify_boolean(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.ndfc.log.error(msg)
            sys.exit(1)
        self.payload["preserveConfig"] = param

    @property
    def seed_ip(self):
        """
        return the current payload value of seed_ip
        """
        return self.payload["seedIP"]

    @seed_ip.setter
    def seed_ip(self, param):
        try:
            self.ndfc.verify_ipv4_address(param)
        except AddressValueError:
            self.ndfc.log.error("Exiting.")
            sys.exit(1)
        self.payload["seedIP"] = param

    @property
    def snmp_v3_auth_protocol(self):
        """
        return the current payload value of snmp_v3_auth_protocol
        """
        return self.payload["snmpV3AuthProtocol"]

    @snmp_v3_auth_protocol.setter
    def snmp_v3_auth_protocol(self, param):
        self.ndfc.verify_digits(param, "snmp_v3_auth_protocol")
        self.payload["snmpV3AuthProtocol"] = param

    @property
    def username(self):
        """
        return the current payload value of username
        """
        return self.payload["username"]

    @username.setter
    def username(self, param):
        self.payload["username"] = param
