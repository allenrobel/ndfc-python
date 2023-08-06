"""
Name: ndfc_discover.py
Description: Discover switches and test reachability
Public methods:

- discover() Initiate NDFC discovery of switches.
- is_reachable() Tests for switch reachability from NDFC perspective
- is_up Tests if a switch is up

The JSON payload constructed by the NdfcDiscover() class is shown below.

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
from ipaddress import AddressValueError
from re import sub
from time import sleep

from ndfc_python.log import log
from ndfc_python.validations import Validations

OUR_VERSION = 107


class NdfcDiscover:
    """
    Discover switches
    Populates:
        self.result = result code from controller
        self.response = See response in above docstring

    Public methods:

    - discover() Initiate NDFC discovery of switches.
    - is_reachable() Tests for switch reachability from NDFC perspective
    - is_up Tests if a switch is up

    Examples:

    ndfc = NDFC(log("ndfc_discover_log", "INFO", "DEBUG"))
    ndfc.username = nc.username
    ndfc.password = nc.password
    ndfc.ip4 = nc.ndfc_ip
    ndfc.login()

    # discover() method
    instance = NdfcDiscover(ndfc)
    instance.seed_ip = '10.1.1.1'
    instance.cdp_second_timeout = 10
    instance.discover_username = 'admin'
    instance.discover_password = 'myPassword'
    try:
        instance.discover()
    except ValueError as err:
        instance.logger.error(f"exiting. {err}")
        sys.exit(1)
    print(f"response: {instance.response}")

    # is_up() method
    instance = NdfcDiscover(ndfc)
    instance.discover_password = "myPassword"
    instance.discover_username = "admin"
    instance.fabric_name = "ext1"
    instance.seed_ip = "10.1.1.100"
    try:
        up = discover.is_up()
    except ValueError as err:
        instance.logger.error(f"exiting. {err}")
        sys.exit(1)
    if up is True:
        result = "up"
    else:
        result = "down"
    print(f"seed_ip {instance.seed_ip} is {result}")
    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__

        self.validations = Validations()
        # ordering of the next three items matters
        # properties not passed to NDFC
        self._internal_properties = {}
        self._init_default_logger()
        self._init_internal_properties()

        # time to sleep after each request retry
        self._retry_sleep_time = 10

        # post/get base headers
        self.headers = {}
        self.headers["Content-Type"] = "application/json"

        self._init_properties_set()
        self._init_payload_set()
        self._init_payload_mandatory_set()
        self._init_payload_default()
        self._init_payload()
        self._init_payload_map()

        self.response = ""
        self.discover_status_code = -1
        self._reachability_status_code = -1
        self._reachability_response = {}
        self.discover_response = {}

        # populated in self._populate_raw_fabric_info()
        self.raw_fabric_info = []
        # populated in self._populate_existing_fabric_names()
        self.fabric_names = set()

        # populated in self._populate_fabric_type() from within
        # self._final_verification()
        self._fabric_type = None

        self._reachability_response_keys = [
            "auth",
            "deviceIndex",
            "hopCount",
            "ipaddr",
            "known",
            "lastChange",
            "platform",
            "reachable",
            "selectable",
            "serialNumber",
            "statusReason",
            "sysName",
            "valid",
            "vdcMac",
            "vdcId",
            "version",
        ]

    def _init_default_logger(self):
        """
        This logger will be active if the user hasn't set self.logger
        """
        self.logger = log("ndfc_discover_log")

    def _init_internal_properties(self):
        self._internal_properties["logger"] = self.logger
        self._internal_properties["ndfc"] = None

    def _init_payload_set(self):
        """
        The set of all keys expected by NDFC within the discover payload
        See also:
            self._init_payload()
            self._init_payload_map
        """
        self._payload_set = set()
        self._payload_set.add("cdpSecondTimeout")
        self._payload_set.add("fabric")
        self._payload_set.add("maxHops")
        self._payload_set.add("password")
        self._payload_set.add("preserveConfig")
        self._payload_set.add("seedIP")
        self._payload_set.add("snmpV3AuthProtocol")
        self._payload_set.add("username")

    def _init_payload_default(self):
        """
        Payload items that the caller needn't provide unless modification
        is desired.
        """
        self.payload_default = {}
        self.payload_default["cdpSecondTimeout"] = 5
        self.payload_default["maxHops"] = 0
        self.payload_default["preserveConfig"] = True
        self.payload_default["snmpV3AuthProtocol"] = 0

    def _init_properties_set(self):
        """
        Initialize a set containing all public properties within
        this class. This is not currently used anywhere.
        """
        self._properties_set = set()
        self._properties_set.add("cdp_second_timeout")
        self._properties_set.add("discover_password")
        self._properties_set.add("discover_username")
        self._properties_set.add("fabric_name")
        self._properties_set.add("max_hops")
        self._properties_set.add("preserve_config")
        self._properties_set.add("seed_ip")
        self._properties_set.add("snmp_v3_auth_protocol")

    def _init_payload_mandatory_set(self):
        """
        The set of mandatory payload keys for which the caller needs to
        provide values.  These are payload keys, not propery names
        """
        self.payload_set_mandatory = set()
        self.payload_set_mandatory.add("fabric")
        self.payload_set_mandatory.add("password")
        self.payload_set_mandatory.add("username")
        self.payload_set_mandatory.add("seedIP")

    def _init_payload(self):
        """
        Initialize the payload for the request body.
        """
        self.payload = {}
        for param in self._payload_set:
            if param in self.payload_default:
                self.payload[param] = self.payload_default[param]
            else:
                self.payload[param] = ""

    def _init_payload_map(self):
        """
        This class standardizes on lowercase dunder property names,
        while NDFC uses both camelCase and upper-case SNAKE_CASE names.
        For messages involving the original NDFC parameter names,
        self._payload_map provides a way to map these into the property
        name conventions of this class.

        self._payload_map is keyed on NDFC parameter names. The value is the
        property name used in this class.
        """
        self._payload_map = {}
        for param in self._payload_set:
            # convert all dunder params to lowercase
            if "_" in param:
                self._payload_map[param] = param.lower()
                continue
            # convert camel case to dunder
            pattern = r"(?<!^)(?=[A-Z])"
            self._payload_map[param] = sub(pattern, "_", param).lower()
        # fix any cases the regex above doesn't handle
        self._payload_map["fabric"] = "fabric_name"
        self._payload_map["password"] = "discover_password"
        self._payload_map["username"] = "discover_username"
        self._payload_map["seedIP"] = "seed_ip"
        # for key in self._payload_map:
        #     print("{:<30} -> {:<30}".format(
        #         key,
        #         self._payload_map[key]
        #     ))
        # sys.exit(0)

    def _preprocess_payload(self):
        """
        1. Set a default value for any properties that the caller has not set
        and that NDFC provides a default for.

        2. Any other fixup that may be required
        """

    def _final_verification(self):
        """
        Set of final checks prior to sending the request.

        - verify ndfc is set and is an NDFC instance
        - all mandatory parameters have been set
        - populate vars and structures needed by self.discover()
        - verify fabric exists on the NDFC
        """
        try:
            self.validations.verify_ndfc(self.ndfc)
        except (AttributeError, TypeError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)

        for key in self.payload_set_mandatory:
            if self.payload[key] == "":
                msg = f"exiting. call instance.{self._payload_map[key]} "
                msg += "before calling instance.create()"
                self.logger.error(msg)
                sys.exit(1)
        self._populate_raw_fabric_info()
        self._populate_existing_fabric_names()
        try:
            self._verify_fabric_exists()
        except ValueError as err:
            msg = f"cannot continue due to {err}."
            raise ValueError(msg) from err
        try:
            self._populate_fabric_type()
        except ValueError as err:
            msg = f"cannot continue due to {err}"
            raise ValueError(msg) from err

    def _verify_reachability_response(self):
        """
        raise TypeError if reachability response is not a list()
        raise KeyError if expected keys are not found in all items

        Expected format is:
        [
            {
                'auth': True,
                'deviceIndex': 'cvd-leaf-1311(FDO21120U5D)',
                'hopCount': 0,
                'ipaddr': '172.22.150.102',
                'known': True,
                'lastChange': None,
                'platform': 'N9K-C93180YC-EX',
                'reachable': True,
                'selectable': False,
                'serialNumber': 'FDO21120U5D',
                'statusReason': 'already managed in ext1'
                'sysName': 'cvd-leaf-1311',
                'valid': True,
                'vdcMac': None,
                'vdcId': 0,
                'version': '10.3(2)',
            }
        ]
        """
        if not isinstance(self._reachability_response, list):
            msg = "expected self._reachability_response to be a list. "
            msg += f"got {type({self._reachability_response}).__name__} "
            msg += "instead."
            raise TypeError(msg)
        for item in self._reachability_response:
            for key in self._reachability_response_keys:
                if key not in item:
                    msg = f"self._reachability_response is missing key {key} "
                    msg += f"in item {item}"
                    raise KeyError(msg)

    def is_managed(self):
        """
        Return True if self.seed_ip is managed in fabric self.fabric_name
        Return False otherwise

        NOTE: This is called from self.discover() which, in turn, calls
        self.is_reachable(). where self._reachability_response is populated
        and verified.  So it's safe by the time we access it.
        """
        for item in self._reachability_response:
            if item["ipaddr"] == self.seed_ip:
                if "already managed" in item["statusReason"]:
                    return True
        return False

    def is_reachable(self):
        """
        Return True if self.seed_ip is reachable, per NDFC's test-reachability
        endpoint.
        Return False if self.seed_ip is not reachable
        Exit with error if reachability_response is not a list()
        Exit with error if any items in reachability_response are missing keys
        """
        self._final_verification()
        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}"
        url += "/inventory/test-reachability"
        self.ndfc.post(url, self.ndfc.make_headers(), self.payload)
        self._reachability_status_code = self.ndfc.response.status_code
        self._reachability_response = json.loads(self.ndfc.response.text)

        try:
            self._verify_reachability_response()
        except TypeError as err:
            msg = f"cannot continue. unexpected reachability response. {err}"
            self.logger.error(msg)
            sys.exit(1)
        except KeyError as err:
            msg = f"cannot continue. unexpected reachability response. {err}"
            self.logger.error(msg)
            sys.exit(1)

        if self._reachability_status_code != 200:
            msg = f"Switch {self.seed_ip} is not reachable."
            msg += f" status_code: {self._reachability_status_code}"
            msg += f" response: {self._reachability_response}"
            self.logger.error(msg)
            return False
        return True

    def _populate_raw_fabric_info(self):
        try:
            self.verify_ndfc_is_set()
        except AttributeError as err:
            self.logger.error(err)
            sys.exit(1)
        url = self.ndfc.url_control_fabrics
        self.raw_fabric_info = self.ndfc.get(url, self.ndfc.make_headers())

    def _populate_existing_fabric_names(self):
        """
        populates self.fabric_names, a set containing the names of fabrics
        that exist on the NDFC
        """
        for item in self.raw_fabric_info:
            if "fabricName" in item:
                self.fabric_names.add(item["fabricName"])

    def _populate_fabric_type(self):
        if self.fabric_name not in self.fabric_names:
            msg = f"fabric_name {self.fabric_name} not found in existing "
            msg += f"fabrics {self.fabric_names}"
            raise ValueError(msg)
        for item in self.raw_fabric_info:
            if "fabricName" not in item:
                continue
            if "fabricType" not in item:
                continue
            if item["fabricName"] == self.fabric_name:
                self._fabric_type = item["fabricType"]
                break

    def _verify_fabric_exists(self):
        if self.fabric_name not in self.fabric_names:
            msg = f"fabric_name {self.fabric_name} does not exist "
            msg += f"on the NDFC, current fabrics: {self.fabric_names}"
            raise ValueError(msg)

    def discover(self):
        """
        Issue POST to NDFC's discover endpoint with validated request.
        raise ValueError if fabric does not exist.
        """
        self._preprocess_payload()
        try:
            self._final_verification()
        except ValueError as err:
            msg = f"final verification failed. detail: {err}"
            raise ValueError(msg) from err
        if self.preserve_config is False and self._fabric_type == "External":
            msg = "preserve_config must be True for External fabric_type. "
            msg += f"got preserve_config {self.preserve_config}, "
            msg += f"fabric {self.fabric_name}, "
            msg += f"fabric_type {self._fabric_type}"
            raise ValueError(msg)

        retries = 5
        while self.is_reachable() is False and retries < 5:
            sleep(self._retry_sleep_time)
            retries += 1
        if self.is_reachable() is False:
            msg = f"exiting, {self.seed_ip} not reachable "
            msg += f"after {retries} retries"
            self.logger.error(msg)
            sys.exit(1)

        if self.is_managed() is True:
            msg = f"exiting, {self.seed_ip} is already managed in fabric "
            msg += f"{self.fabric_name}"
            self.logger.error(msg)
            sys.exit(1)

        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}"
        url += "/inventory/discover"

        self.payload["switches"] = self._reachability_response

        self.ndfc.post(url, self.ndfc.make_headers(), self.payload)
        self.discover_status_code = self.ndfc.response.status_code
        self.discover_response = json.loads(self.ndfc.response.text)

    def is_up(self):
        """
        Return True if self.seed_ip is manageable.
        raise ValueError if self.fabric_name does not exist on the NDFC
        raise ValueError if self.seed_ip is not found on the NDFC
        Return False if self.seed_ip is known to NDFC, but is not reachable
        """
        try:
            self._final_verification()
        except ValueError as err:
            msg = "is_up cannot continue. final verification failed."
            msg += f"detail: {err}"
            raise ValueError(msg) from err
        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}"
        url += "/inventory/switchesByFabric"
        headers = self.ndfc.make_headers()
        self.ndfc.get(url, headers)
        response = json.loads(self.ndfc.response.text)
        our_switch = None
        for item in response:
            if "ipAddress" not in item:
                continue
            # The key 'manageable' is mispelled in NDFC's response so we have
            # to mispell it here as well. :-(
            if "managable" not in item:
                msg = "Skipping. 'managable' [sic] key not found in response "
                msg += f"{item}"
                self.logger.error(msg)
                continue
            if item["ipAddress"] == self.seed_ip:
                our_switch = item
                break
        if our_switch is None:
            msg = f"{self.seed_ip} not found in fabric {self.fabric_name} "
            msg += "on the NDFC."
            raise ValueError(msg)
        return our_switch["managable"]

    # properties that are not passed to NDFC
    @property
    def logger(self):
        """
        return/set the current logger instance
        """
        return self._internal_properties["logger"]

    @logger.setter
    def logger(self, param):
        self._internal_properties["logger"] = param

    @property
    def ndfc(self):
        """
        return/set the current ndfc instance
        """
        return self._internal_properties["ndfc"]

    @ndfc.setter
    def ndfc(self, param):
        self._internal_properties["ndfc"] = param

    # top_level properties
    @property
    def cdp_second_timeout(self):
        """
        The number of seconds allowed for CDP discovery of neighbor switches
        """
        return self.payload["cdpSecondTimeout"]

    @cdp_second_timeout.setter
    def cdp_second_timeout(self, param):
        try:
            self.validations.verify_digits(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
        self.payload["cdpSecondTimeout"] = param

    @property
    def fabric_name(self):
        """
        The name of the fabric in which discovery will take place
        """
        return self.payload["fabric"]

    @fabric_name.setter
    def fabric_name(self, param):
        self.payload["fabric"] = param

    @property
    def max_hops(self):
        """
        The radius, in hops, from the seed_ip switch, in which to
        discover neighboring switches.  If set to 0, discovery is
        limited to the seed_ip switch.  If set to > 0, discovery
        will include switches X hops away from the seed_ip switch.
        """
        return self.payload["maxHops"]

    @max_hops.setter
    def max_hops(self, param):
        try:
            self.validations.verify_digits(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
        self.payload["maxHops"] = param

    @property
    def discover_password(self):
        """
        The password of the seed_ip switch.
        """
        return self.payload["password"]

    @discover_password.setter
    def discover_password(self, param):
        self.payload["password"] = param

    @property
    def preserve_config(self):
        """
        If True, the configurations on discovered switches will be preserved.
        Else, a write erase + reload will be done on the discovered switches.
        """
        return self.payload["preserveConfig"]

    @preserve_config.setter
    def preserve_config(self, param):
        try:
            self.validations.verify_boolean(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        self.payload["preserveConfig"] = param

    @property
    def seed_ip(self):
        """
        The IP address of the switch from which discovery will be initiated.
        """
        return self.payload["seedIP"]

    @seed_ip.setter
    def seed_ip(self, param):
        try:
            self.validations.verify_ipv4_address(param)
        except AddressValueError:
            self.logger.error("Exiting.")
            sys.exit(1)
        self.payload["seedIP"] = param

    @property
    def snmp_v3_auth_protocol(self):
        """
        The SNMPv3 authorization protocol to configure on discovered switches.
        """
        return self.payload["snmpV3AuthProtocol"]

    @snmp_v3_auth_protocol.setter
    def snmp_v3_auth_protocol(self, param):
        try:
            self.validations.verify_digits(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
        self.payload["snmpV3AuthProtocol"] = param

    @property
    def discover_username(self):
        """
        The username of the seed_ip switch.
        """
        return self.payload["username"]

    @discover_username.setter
    def discover_username(self, param):
        self.payload["username"] = param
