"""
Name: ndfc_reachability.py
Description: Test switch reachability (from NDFC controller perspective).

The JSON payload constructed by this class is shown below.

{
    "maxHops":"0",
    "seedIP":"10.1.1.2",
    "cdpSecondTimeout":5,
    "snmpV3AuthProtocol":0,
    "username":"MyNxosUsername",
    "password":"MyNxosPassword",
    "preserveConfig":false   # or true
}

# Example controller response (rest_send.response_current):

{
    "DATA": [
        {
            "auth": true,
            "deviceIndex": "cvd-1314-leaf(FD1234567FV)",
            "hopCount": 0,
            "ipaddr": "10.1.1.2",
            "known": true,
            "lastChange": null,
            "platform": "N9K-C93180YC-EX",
            "reachable": true,
            "selectable": false,
            "serialNumber": "FD1234567FV",
            "statusReason": "already managed in f1",
            "switchRole": null,
            "sysName": "cvd-1314-leaf",
            "valid": true,
            "vdcId": 0,
            "vdcMac": null,
            "vendor": "Cisco",
            "version": "10.2(5)"
        }
    ],
    "MESSAGE": "OK",
    "METHOD": "POST",
    "REQUEST_PATH": "https://10.1.1.1/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/f1/inventory/test-reachability",
    "RETURN_CODE": 200
}

"""

# We're using isort for import linting
# pylint: disable=wrong-import-order

import inspect
import logging
import sys
from ipaddress import AddressValueError

from ndfc_python.validations import Validations
from plugins.module_utils.common.api.v1.lan_fabric.rest.control.fabrics.fabrics import EpFabrics
from plugins.module_utils.common.conversion import ConversionUtils
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.fabric.fabric_details_v2 import FabricDetailsByName


@Properties.add_rest_send
@Properties.add_results
class Reachability:
    """
    # Summary

    Send a switch reachability POST request to the controller and store the result.

    # Usage example

    See the following script.

    ./examples/reachability.py
    """

    def __init__(self):
        self.class_name = __class__.__name__

        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.conversion = ConversionUtils()
        self.validations = Validations()
        self.ep_rest_control_fabrics = EpFabrics()

        self._response_data = None

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
        self.payload_default["username"] = ""
        self.payload_default["password"] = ""

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
        # TODO: If fabric is EasyFabric, and preserve_config is True
        # need to throw an error and exit here.
        for param in self.payload_set_mandatory:
            if self.payload[param] == "":
                msg = f"exiting. call instance.{param} before "
                msg += "calling instance.create()"
                self.log.error(msg)
                sys.exit(1)

    def fabric_exists(self):
        """
        Return True if self.fabric_name exists on the controller.
        Return False otherwise.
        """
        instance = FabricDetailsByName()
        # pylint: disable=no-member
        instance.rest_send = self.rest_send
        instance.results = self.results
        # pylint: enable=no-member
        instance.refresh()
        instance.filter = self.fabric_name
        if instance.filtered_data is None:
            return False
        return True

    def commit(self):
        """
        Send a POST request to the controller to the test-reachability endpoint
        """
        method_name = inspect.stack()[0][3]
        self._preprocess_payload()
        self._final_verification()

        if self.fabric_exists() is False:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        path = self.ep_rest_control_fabrics
        path.fabric_name = self.fabric_name
        verb = "POST"

        # pylint: disable=no-member
        try:
            self.rest_send.path = f"{path.path_fabric_name}/inventory/test-reachability"
            self.rest_send.payload = self.payload
            self.rest_send.verb = verb
            self.rest_send.save_settings()
            # Don't wait long in case there's a non-200 response
            self.rest_send.retries = 1
            self.rest_send.timeout = 10
            self.rest_send.commit()
            self.rest_send.restore_settings()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        self._response_data = self.rest_send.response_current.get("DATA")[0]
        if self.response_data is None:
            msg = f"{self.class_name}.refresh() failed: response "
            msg += "does not contain DATA key. Controller response: "
            msg += f"{self.rest_send.response_current}"
            raise ValueError(msg)
        # pylint: enable=no-member

    def _get(self, item):
        """
        Return values for keys within self.response_data

        See accessor properties
        """
        method_name = inspect.stack()[0][3]
        if self.response_data is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Call {self.class_name}.commit before calling "
            msg += "response accessor properties."
            raise ValueError(msg)
        return self.conversion.make_none(self.conversion.make_boolean(self.response_data.get(item)))

    # top_level properties
    @property
    def cdp_second_timeout(self):
        """
        return the current payload value of cdp_second_timeout
        """
        return self.payload["cdpSecondTimeout"]

    @cdp_second_timeout.setter
    def cdp_second_timeout(self, param):
        try:
            self.validations.verify_digits(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.log.error(msg)
            sys.exit(1)
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
        try:
            self.validations.verify_digits(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.log.error(msg)
            sys.exit(1)
        self.payload["maxHops"] = param

    @property
    def nxos_password(self):
        """
        The password credential for the NX-OS switch which the controller
        uses for switch discovery.

        Required before calling commit.
        """
        return self.payload["password"]

    @nxos_password.setter
    def nxos_password(self, param):
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
            self.validations.verify_boolean(param)
        except TypeError as err:
            msg = f"exiting. {err}"
            self.log.error(msg)
            sys.exit(1)
        self.payload["preserveConfig"] = param

    @property
    def response_data(self):
        """
        Return the data retrieved from the request
        """
        return self._response_data

    @property
    def seed_ip(self):
        """
        return the current payload value of seed_ip
        """
        return self.payload["seedIP"]

    @seed_ip.setter
    def seed_ip(self, param):
        try:
            self.validations.verify_ipv4_address(param)
        except AddressValueError as err:
            msg = f"exiting. {err}"
            self.log.error(msg)
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
        try:
            self.validations.verify_digits(param)
        except ValueError as err:
            msg = f"exiting. {err}"
            self.log.error(msg)
            sys.exit(1)
        self.payload["snmpV3AuthProtocol"] = param

    @property
    def nxos_username(self):
        """
        The username credential for the NX-OS switch which the controller
        uses for switch discovery.

        Required before calling commit.
        """
        return self.payload["username"]

    @nxos_username.setter
    def nxos_username(self, param):
        self.payload["username"] = param

    # Controller response accessors
    @property
    def auth(self):
        """
        auth key from controller response
        """
        return self._get("auth")

    @property
    def device_index(self):
        """
        deviceIndex key from controller response
        """
        return self._get("deviceIndex")

    @property
    def hop_count(self):
        """
        hopCount key from controller response
        """
        return self._get("hopCount")

    @property
    def ip_addr(self):
        """
        ipaddr key from controller response
        """
        return self._get("ipaddr")

    @property
    def known(self):
        """
        known key from controller response
        """
        return self._get("known")

    @property
    def last_change(self):
        """
        lastChange key from controller response
        """
        return self._get("lastChange")

    @property
    def platform(self):
        """
        platform key from controller response
        """
        return self._get("platform")

    @property
    def reachable(self):
        """
        reachable key from controller response
        """
        return self._get("reachable")

    @property
    def selectable(self):
        """
        selectable key from controller response
        """
        return self._get("selectable")

    @property
    def serial_number(self):
        """
        serialNumber key from controller response
        """
        return self._get("serialNumber")

    @property
    def status_reason(self):
        """
        statusReason key from controller response
        """
        return self._get("statusReason")

    @property
    def switch_role(self):
        """
        switchRole key from controller response
        """
        return self._get("switchRole")

    @property
    def sys_name(self):
        """
        sysName key from controller response
        """
        return self._get("sysName")

    @property
    def valid(self):
        """
        valid key from controller response
        """
        return self._get("valid")

    @property
    def vdc_id(self):
        """
        vdcId key from controller response
        """
        return self._get("vdcId")

    @property
    def vdc_mac(self):
        """
        vdcMac key from controller response
        """
        return self._get("vdcMac")

    @property
    def vendor(self):
        """
        vendor key from controller response
        """
        return self._get("vendor")

    @property
    def version(self):
        """
        version key from controller response
        """
        return self._get("version")
