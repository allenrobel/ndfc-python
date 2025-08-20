"""
Name: interface_access.py
Description:

Configure an access port on Nexus Dashboard via the NDFC REST API.

Example usage:

from ndfc_python.ndfc import NDFC
from ndfc_python.interface_access import InterfaceAccessCreate

ndfc = NDFC()
ndfc.domain = "local"
ndfc.ip4 = "10.1.1.1"
ndfc.username = "admin"
ndfc.password = "password"
ndfc.login()

instance = InterfaceAccessCreate()
instance.policy = "int_access_host"
instance.interface_type = "INTERFACE_ETHERNET"
instance.serial_number = "FDO1234567A"
instance.if_name = "Ethernet1/2"
instance.intf_name = "Ethernet1/2"
instance.bpduguard_enabled = "true"
instance.porttype_fast_enabled = "true"
instance.mtu = "jumbo"
instance.speed = "Auto"
instance.access_vlan = "10"
instance.desc = "Eth1/2: Connected to HO1"
instance.conf = ""
instance.admin_state = "true"
instance.ptp = "false"
instance.enable_netflow = "false"
instance.netflow_monitor = ""
instance.commit()
"""

# We are using isort/black to link imports
# pylint: disable=wrong-import-order
import inspect
import logging

from ndfc_python.ndfc import NdfcRequestError
from plugins.module_utils.common.properties import Properties


@Properties.add_rest_send
@Properties.add_results
class InterfaceAccessCreate:
    """
    Configure an access port on Nexus Dashboard via the NDFC REST API.
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")
        self._rest_send = None
        self._results = None
        self._init_payload_set()
        self._init_payload_set_mandatory()
        self._init_payload_default()
        self._init_nvpair_set()
        self._init_nvpair_set_mandatory()
        self._init_nvpair_default()
        self._init_payload()
        self._init_nvpair()

    def _init_payload_set(self):
        self._payload_set = set()
        self._payload_set.add("policy")
        self._payload_set.add("interfaceType")
        self._payload_set.add("interfaces")

    def _init_payload_set_mandatory(self):
        self._payload_set_mandatory = set()
        self._payload_set_mandatory.add("policy")
        self._payload_set_mandatory.add("interfaceType")

    def _init_payload_default(self):
        """Default values if user does not provide them"""
        self._payload_default = {}
        self._payload_default["policy"] = "int_access_host"
        self._payload_default["interfaceType"] = "INTERFACE_ETHERNET"
        # Add default values here as needed

    def _init_nvpair_set(self):
        """All values in nvPairs"""
        self._nvpair_set = set()
        self._nvpair_set.add("INTF_NAME")
        self._nvpair_set.add("SERIAL_NUMBER")
        self._nvpair_set.add("BPDUGUARD_ENABLED")
        self._nvpair_set.add("PORTTYPE_FAST_ENABLED")
        self._nvpair_set.add("MTU")
        self._nvpair_set.add("SPEED")
        self._nvpair_set.add("ACCESS_VLAN")
        self._nvpair_set.add("DESC")
        self._nvpair_set.add("CONF")
        self._nvpair_set.add("ADMIN_STATE")
        self._nvpair_set.add("PTP")
        self._nvpair_set.add("ENABLE_NETFLOW")
        self._nvpair_set.add("NETFLOW_MONITOR")

    def _init_nvpair_set_mandatory(self):
        """Mandatory nvPair properties that must be set by the user."""
        self._nvpair_set_mandatory = set()
        self._nvpair_set_mandatory.add("INTF_NAME")
        self._nvpair_set_mandatory.add("SERIAL_NUMBER")
        # Add more as needed

    def _init_nvpair_default(self):
        self._nvpair_default = {}
        self._nvpair_default["ACCESS_VLAN"] = ""
        self._nvpair_default["ADMIN_STATE"] = "true"
        self._nvpair_default["BPDUGUARD_ENABLED"] = "true"
        self._nvpair_default["DESC"] = ""
        self._nvpair_default["ENABLE_NETFLOW"] = "false"
        self._nvpair_default["MTU"] = "jumbo"
        self._nvpair_default["NETFLOW_MONITOR"] = ""
        self._nvpair_default["PORTTYPE_FAST_ENABLED"] = "true"
        self._nvpair_default["PTP"] = "false"
        self._nvpair_default["SPEED"] = "Auto"
        # Add default values here as needed

    def _init_payload(self):
        self.payload = {}
        for param in self._payload_set:
            if param in self._payload_default:
                self.payload[param] = self._payload_default[param]
            else:
                self.payload[param] = None

    def _init_nvpair(self):
        self.nvpair = {}
        for param in self._nvpair_set:
            if param in self._nvpair_default:
                self.nvpair[param] = self._nvpair_default[param]
            else:
                self.nvpair[param] = None

    # Top-level payload properties
    @property
    def policy(self):
        """return payload.policy"""
        return self.payload["policy"]

    @policy.setter
    def policy(self, value):
        self.payload["policy"] = value

    @property
    def interface_type(self):
        """return payload.interfaceType"""
        return self.payload["interfaceType"]

    @interface_type.setter
    def interface_type(self, value):
        self.payload["interfaceType"] = value

    # nvPair properties
    @property
    def access_vlan(self):
        """return nvpair.ACCESS_VLAN"""
        return self.nvpair["ACCESS_VLAN"]

    @access_vlan.setter
    def access_vlan(self, value):
        self.nvpair["ACCESS_VLAN"] = value

    @property
    def admin_state(self):
        """return nvpair.ADMIN_STATE"""
        return self.nvpair["ADMIN_STATE"]

    @admin_state.setter
    def admin_state(self, value):
        self.nvpair["ADMIN_STATE"] = value

    @property
    def bpduguard_enabled(self):
        """return nvpair.BPDUGUARD_ENABLED"""
        return self.nvpair["BPDUGUARD_ENABLED"]

    @bpduguard_enabled.setter
    def bpduguard_enabled(self, value):
        self.nvpair["BPDUGUARD_ENABLED"] = value

    @property
    def conf(self):
        """return nvpair.CONF"""
        return self.nvpair["CONF"]

    @conf.setter
    def conf(self, value):
        self.nvpair["CONF"] = value

    @property
    def desc(self):
        """return nvpair.DESC"""
        return self.nvpair["DESC"]

    @desc.setter
    def desc(self, value):
        self.nvpair["DESC"] = value

    @property
    def enable_netflow(self):
        """return nvpair.ENABLE_NETFLOW"""
        return self.nvpair["ENABLE_NETFLOW"]

    @enable_netflow.setter
    def enable_netflow(self, value):
        self.nvpair["ENABLE_NETFLOW"] = value

    @property
    def intf_name(self):
        """return nvpair.INTF_NAME"""
        return self.nvpair["INTF_NAME"]

    @intf_name.setter
    def intf_name(self, value):
        self.nvpair["INTF_NAME"] = value

    @property
    def mtu(self):
        """return nvpair.MTU"""
        return str(self.nvpair["MTU"])

    @mtu.setter
    def mtu(self, value):
        self.nvpair["MTU"] = value

    @property
    def netflow_monitor(self):
        """return nvpair.NETFLOW_MONITOR"""
        return self.nvpair["NETFLOW_MONITOR"]

    @netflow_monitor.setter
    def netflow_monitor(self, value):
        self.nvpair["NETFLOW_MONITOR"] = value

    @property
    def porttype_fast_enabled(self):
        """return nvpair.PORTTYPE_FAST_ENABLED"""
        return self.nvpair["PORTTYPE_FAST_ENABLED"]

    @porttype_fast_enabled.setter
    def porttype_fast_enabled(self, value):
        self.nvpair["PORTTYPE_FAST_ENABLED"] = value

    @property
    def ptp(self):
        """return nvpair.PTP"""
        return self.nvpair["PTP"]

    @ptp.setter
    def ptp(self, value):
        self.nvpair["PTP"] = value

    @property
    def serial_number(self):
        """return nvpair.SERIAL_NUMBER"""
        return self.nvpair["SERIAL_NUMBER"]

    @serial_number.setter
    def serial_number(self, value):
        self.nvpair["SERIAL_NUMBER"] = value

    @property
    def speed(self):
        """return nvpair.SPEED"""
        return self.nvpair["SPEED"]

    @speed.setter
    def speed(self, value):
        self.nvpair["SPEED"] = value

    def _final_verification(self):
        """final verification of user configuration"""
        method_name = inspect.stack()[0][3]
        for param in self._payload_set_mandatory:
            if self.payload[param] in (None, ""):
                msg = f"{self.class_name}.{method_name}: Missing mandatory payload property: {param}"
                self.log.error(msg)
                raise ValueError(msg)
        for param in self._nvpair_set_mandatory:
            if self.nvpair[param] in (None, ""):
                msg = f"{self.class_name}.{method_name}: Missing mandatory nvPair property: {param}"
                self.log.error(msg)
                raise ValueError(msg)

    def commit(self):
        """Commit the configuration changes to the controller."""
        method_name = inspect.stack()[0][3]
        self._final_verification()
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/interface"
        verb = "POST"
        interface_obj = {
            "serialNumber": self.serial_number,
            "ifName": self.intf_name,
            "nvPairs": self.nvpair.copy(),
        }
        self.payload["interfaces"] = [interface_obj]
        try:
            # pylint: disable=no-member
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.payload = self.payload
            self.rest_send.commit()
            self.results.build_final_result()
            return self.rest_send.response_current
            # pylint: enable=no-member
        except (TypeError, ValueError, NdfcRequestError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Error sending POST request to the controller. Error detail: {error}"
            self.log.error(msg)
            raise ValueError(msg) from error
