"""
Name: ndfc_device_info.py
Description: Retrieve information about a device
"""
import json
import sys
from ipaddress import AddressValueError

from ndfc_python.ndfc import NdfcRequestError

OUR_VERSION = 100


class NdfcDeviceInfo:
    """
    Retrieve information about a device
    Populates:
        self.status_code = status_code from controller after refresh()
        self.response = response from controller after refresh()

    Public properties:
    Mandatory for retrieving device information i.e. before calling refresh()
    - fabric : fabric in which device resides
    - ip_address : ip address of the device

    Public methods:

    - refresh() Refresh a device's information

    Public read-write properties:

    - fabric_name
    - ipv4_address

    Public read-only properties (many more, see )
    - device_id
    - logical_name
    - model
    - release
    - serial_number
    - switch_db_id
    - switch_role

    Public methods
    - refresh() : refresh the device's information

    Examples:

    from ndfc_python.log import log
    from ndfc_python.ndfc import NDFC
    from ndfc_python.ndfc_credentials import NdfcCredentials
    from ndfc_python.ndfc_device_info import NdfcDeviceInfo

    nc = NdfcCredentials()

    ndfc = NDFC(log("ndfc_device_info_log", "INFO", "DEBUG"))
    ndfc.username = nc.username
    ndfc.password = nc.password
    ndfc.ip4 = nc.ndfc_ip
    ndfc.login()

    instance = NdfcDeviceInfo(ndfc)
    instance.fabric_name = "easy"
    instance.ip_address = "172.22.150.103"
    instance.refresh()
    print(f"device: {instance.ip_address}")
    print(f"fabric: {instance.fabric_name}")
    print(f"   name: {instance.logical_name}")
    print(f"   role: {instance.switch_role}")
    print(f"   db_id: {instance.switch_db_id}")
    print(f"   serial_number: {instance.serial_number}")
    print(f"   model: {instance.model}")
    print(f"   release: {instance.release}")



    REST API Endpoint
    Returned information type: JSON list of objects
    Example returned information:

    [
        {
            "switchRoleEnum": "Spine",
            "vrf": "management",
            "fabricTechnology": "VXLANFabric",
            "deviceType": "Switch_Fabric",
            "fabricId": 5,
            "name": null,
            "domainID": 0,
            "wwn": null,
            "membership": null,
            "ports": 0,
            "model": "N9K-C9336C-FX2",
            "version": null,
            "upTime": 0,
            "ipAddress": "10.1.1.1",
            "mgmtAddress": null,
            "vendor": null,
            "displayHdrs": null,
            "displayValues": null,
            "colDBId": 0,
            "fid": 0,
            "isLan": false,
            "is_smlic_enabled": false,
            "present": true,
            "licenseViolation": false,
            "managable": true,
            "mds": false,
            "connUnitStatus": 0,
            "standbySupState": 0,
            "activeSupSlot": 0,
            "unmanagableCause": "",
            "lastScanTime": 0,
            "fabricName": "LC_1",
            "modelType": 0,
            "logicalName": "cvd-111-dci",
            "switchDbID": 1158430,
            "uid": 0,
            "release": "10.2(2)",
            "location": null,
            "contact": null,
            "upTimeStr": "4 days, 08:44:31",
            "upTimeNumber": 0,
            "network": null,
            "nonMdsModel": null,
            "numberOfPorts": 0,
            "availPorts": 0,
            "usedPorts": 0,
            "vsanWwn": null,
            "vsanWwnName": null,
            "swWwn": null,
            "swWwnName": null,
            "serialNumber": "FDO2222222H",
            "domain": null,
            "principal": null,
            "status": "ok",
            "index": 0,
            "licenseDetail": null,
            "isPmCollect": false,
            "sanAnalyticsCapable": false,
            "vdcId": 0,
            "vdcName": "",
            "vdcMac": null,
            "fcoeEnabled": false,
            "cpuUsage": 0,
            "memoryUsage": 0,
            "scope": null,
            "fex": false,
            "health": -1,
            "npvEnabled": false,
            "linkName": null,
            "username": null,
            "primaryIP": "",
            "primarySwitchDbID": 0,
            "secondaryIP": "",
            "secondarySwitchDbID": 0,
            "isEchSupport": false,
            "moduleIndexOffset": 9999,
            "sysDescr": "",
            "isTrapDelayed": false,
            "switchRole": "spine",
            "mode": "Normal",
            "hostName": null,
            "ipDomain": null,
            "systemMode": "Normal",
            "sourceVrf": "management",
            "sourceInterface": "mgmt0",
            "modules": null,
            "fexMap": {},
            "isVpcConfigured": false,
            "vpcDomain": 0,
            "role": null,
            "peer": null,
            "peerSerialNumber": null,
            "peerSwitchDbId": 0,
            "peerlinkState": null,
            "keepAliveState": null,
            "consistencyState": false,
            "sendIntf": null,
            "recvIntf": null,
            "interfaces": null,
            "elementType": null,
            "monitorMode": false,
            "freezeMode": false,
            "isNonNexus": false,
            "swUUIDId": 1142610,
            "swUUID": "DCNM-UUID-1142610",
            "swType": null,
            "ccStatus": "NA",
            "operStatus": "Minor"
        }
    ]
    """

    def __init__(self, ndfc):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        # get base headers
        self.headers = {}
        self.headers["Content-Type"] = "application/json"

        self._init_property_set()
        self._init_property_mandatory_set()
        self._init_properties()

        # set with the public properties of this class
        self._properties = {}

        self._response = {}
        self._status_code = -1

        # populated in self._populate_raw_fabric_info()
        self._raw_fabric_info = []
        # populated in self._populate_existing_fabric_names()
        self._fabric_names = set()

        # populated in self._populate_fabric_type() from within
        # self._final_verification()
        self._fabric_type = None
        self._populate_raw_fabric_info()
        self._populate_existing_fabric_names()

        # populated in self._populate_device_info()
        self._device_info = {}

        # The returned information from endpoint
        # /inventory/SwitchesByFabric
        self._switches_by_fabric = {}

        self._inventory_response_keys = {
            "switchRoleEnum",
            "fabricTechnology",
            "deviceType",
            "fabricId",
            "name",
            "domainID",
            "wwn",
            "membership",
            "ports",
            "model",
            "version",
            "upTime",
            "ipAddress",
            "mgmtAddress",
            "vrf",
            "vendor",
            "displayHdrs",
            "displayValues",
            "colDBId",
            "fid",
            "isLan",
            "is_smlic_enabled",
            "present",
            "licenseViolation",
            "managable",
            "mds",
            "connUnitStatus",
            "standbySupState",
            "activeSupSlot",
            "unmanagableCause",
            "lastScanTime",
            "fabricName",
            "modelType",
            "logicalName",
            "switchDbID",
            "uid",
            "release",
            "location",
            "contact",
            "upTimeStr",
            "upTimeNumber",
            "network",
            "nonMdsModel",
            "numberOfPorts",
            "availPorts",
            "usedPorts",
            "vsanWwn",
            "vsanWwnName",
            "swWwn",
            "swWwnName",
            "serialNumber",
            "domain",
            "principal",
            "status",
            "index",
            "licenseDetail",
            "isPmCollect",
            "sanAnalyticsCapable",
            "vdcId",
            "vdcName",
            "vdcMac",
            "fcoeEnabled",
            "cpuUsage",
            "memoryUsage",
            "scope",
            "fex",
            "health",
            "npvEnabled",
            "linkName",
            "username",
            "primaryIP",
            "primarySwitchDbID",
            "secondaryIP",
            "secondarySwitchDbID",
            "isEchSupport",
            "moduleIndexOffset",
            "sysDescr",
            "isTrapDelayed",
            "switchRole",
            "mode",
            "hostName",
            "ipDomain",
            "systemMode",
            "sourceVrf",
            "sourceInterface",
            "modules",
            "fexMap",
            "isVpcConfigured",
            "vpcDomain",
            "role",
            "peer",
            "peerSerialNumber",
            "peerSwitchDbId",
            "peerlinkState",
            "keepAliveState",
            "consistencyState",
            "sendIntf",
            "recvIntf",
            "interfaces",
            "elementType",
            "monitorMode",
            "freezeMode",
            "isNonNexus",
            "swUUIDId",
            "swUUID",
            "swType",
            "ccStatus",
            "operStatus",
        }

    def _init_property_set(self):
        """
        Initialize a set containing all public read-write
        properties within this class.
        """
        self._property_set = set()
        self._property_set.add("fabric_name")
        self._property_set.add("ip_address")

    def _init_property_mandatory_set(self):
        """
        The set of mandatory properties for which the caller needs to
        provide values prior to calling refresh().
        """
        self._property_mandatory_set = set()
        self._property_mandatory_set.add("fabric_name")
        self._property_mandatory_set.add("ip_address")

    def _init_properties(self):
        """
        Initialize all read-write properties
        """
        self._properties = {}
        for key in self._property_set:
            self._properties[key] = None

    def _final_verification(self):
        """
        Set of final checks prior to sending the request.

        1. Verify all mandatory parameters have been set
        2. Populate vars and structures needed by self.refresh()
        """
        for key in self._property_mandatory_set:
            if self._properties[key] is None:
                msg = f"exiting. call instance.{key} "
                msg += "before calling instance.refresh()"
                self.ndfc.log.error(msg)
                sys.exit(1)
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

    def _verify_inventory_switches_by_fabric(self, response):
        """
        raise TypeError if response is not a list()
        raise KeyError if expected keys are not found in all items

        See: self._inventory_response_keys
        """
        if not isinstance(response, list):
            msg = "expected self._inventory_response to be a list. "
            msg += f"got {type({response}).__name__} "
            msg += "instead."
            raise TypeError(msg)
        for item in response:
            for key in self._inventory_response_keys:
                if key not in item:
                    msg = f"self._inventory_response is missing key {key} "
                    msg += f"in item {item}"
                    raise KeyError(msg)

    def _populate_raw_fabric_info(self):
        """
        populate self._raw_fabric_info (a JSON list of fabric objects)

        If unsuccessful, exit with error
        """
        try:
            self._raw_fabric_info = self.ndfc.get(
                self.ndfc.url_control_fabrics, self.ndfc.make_headers()
            )
        except NdfcRequestError as err:
            msg = "exiting. unable to populate fabric "
            msg += f"information via url {self.ndfc.url_control_fabrics}. "
            msg += f"exception detail: {err}"
            self.ndfc.log.error(msg)
            sys.exit(1)

    def _populate_existing_fabric_names(self):
        """
        populates self._fabric_names, a set containing the names of fabrics
        that exist on the NDFC
        """
        for item in self._raw_fabric_info:
            if "fabricName" in item:
                self._fabric_names.add(item["fabricName"])

    def _populate_fabric_type(self):
        if self.fabric_name not in self._fabric_names:
            msg = f"fabric_name {self.fabric_name} not found in existing "
            msg += f"fabrics {self._fabric_names}"
            raise ValueError(msg)
        for item in self._raw_fabric_info:
            if "fabricName" not in item:
                continue
            if "fabricType" not in item:
                continue
            if item["fabricName"] == self.fabric_name:
                self._fabric_type = item["fabricType"]
                break

    def _verify_fabric_exists(self):
        """
        raise ValueError if fabric does not exist on the NDFC
        """
        if self.fabric_name not in self._fabric_names:
            msg = f"fabric_name {self.fabric_name} does not exist "
            msg += f"on the NDFC, current fabrics: {self._fabric_names}"
            raise ValueError(msg)

    def _populate_device_info(self):
        """
        set self._device_info if self.ip_address is found in
        self._switches_by_fabric

        raise ValueError otherwise.
        """
        self._device_info = {}
        for device in self._switches_by_fabric:
            if device["ipAddress"] == self.ip_address:
                self._device_info = device
                return
        msg = f"device {self.ip_address} not found in fabric "
        msg += f"{self.fabric_name}"
        raise ValueError(msg)

    def refresh(self):
        """
        Refresh a device's information
        """
        try:
            self._final_verification()
        except ValueError as err:
            msg = f"final verification failed. detail: {err}"
            self.ndfc.log.error(f"exiting. {err}")
            sys.exit(1)

        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}"
        url += "/inventory/switchesByFabric"

        self.ndfc.get(url, self.ndfc.make_headers())
        self._status_code = self.ndfc.response.status_code
        self._response = json.loads(self.ndfc.response.text)
        if self._status_code != 200:
            msg = f"exiting. got non-200 status code {self._status_code} "
            msg += f"for url {url}"
            self.ndfc.log.error(msg)
            sys.exit(1)

        try:
            self._verify_inventory_switches_by_fabric(self._response)
        except (TypeError, KeyError) as err:
            self.ndfc.log.error(f"exiting. {err}")
            sys.exit(1)
        self._switches_by_fabric = self._response

        try:
            self._populate_device_info()
        except ValueError as err:
            msg = f"exiting. {err}"
            self.ndfc.log.error(msg)
            sys.exit(1)

    # Public read-write properties
    @property
    def fabric_name(self):
        """
        The name of the fabric in which discovery will take place
        """
        return self._properties["fabric_name"]

    @fabric_name.setter
    def fabric_name(self, param):
        self._properties["fabric_name"] = param

    @property
    def ip_address(self):
        """
        The IP address of the switch.
        """
        return self._properties["ip_address"]

    @ip_address.setter
    def ip_address(self, param):
        try:
            self.ndfc.verify_ipv4_address(param)
        except AddressValueError:
            self.ndfc.log.error("Exiting.")
            sys.exit(1)
        self._properties["ip_address"] = param

    # Public read-only properties

    @property
    def active_sup_slot(self):
        """
        return the current value of active_sup_slot
        """
        return self._device_info["activeSupSlot"]

    @property
    def avail_ports(self):
        """
        return the current value of avail_ports
        """
        return self._device_info["availPorts"]

    @property
    def cc_status(self):
        """
        return the current value of cc_status
        """
        return self._device_info["ccStatus"]

    @property
    def col_db_id(self):
        """
        return the current value of col_db_id
        """
        return self._device_info["colDBId"]

    @property
    def conn_unit_status(self):
        """
        return the current value of conn_unit_status
        """
        return self._device_info["connUnitStatus"]

    @property
    def consistency_state(self):
        """
        return the current value of consistency_state
        """
        return self._device_info["consistencyState"]

    @property
    def contact(self):
        """
        return the current value of contact
        """
        return self._device_info["contact"]

    @property
    def cpu_usage(self):
        """
        return the current value of cpu_usage
        """
        return self._device_info["cpuUsage"]

    @property
    def device_type(self):
        """
        return the current value of device_type
        """
        return self._device_info["deviceType"]

    @property
    def display_hdrs(self):
        """
        return the current value of display_hdrs
        """
        return self._device_info["displayHdrs"]

    @property
    def display_values(self):
        """
        return the current value of display_values
        """
        return self._device_info["displayValues"]

    @property
    def domain(self):
        """
        return the current value of domain
        """
        return self._device_info["domain"]

    @property
    def domain_id(self):
        """
        return the current value of domain_id
        """
        return self._device_info["domainID"]

    @property
    def element_type(self):
        """
        return the current value of element_type
        """
        return self._device_info["elementType"]

    @property
    def fabric_id(self):
        """
        return the current value of fabric_id
        """
        return self._device_info["fabricId"]

    # fabric_name (see Public read-write properties)

    @property
    def fabric_technology(self):
        """
        return the current value of fabric_technology
        """
        return self._device_info["fabricTechnology"]

    @property
    def fcoe_enabled(self):
        """
        return the current value of fcoe_enabled
        """
        return self._device_info["fcoeEnabled"]

    @property
    def fex(self):
        """
        return the current value of fex
        """
        return self._device_info["fex"]

    @property
    def fex_map(self):
        """
        return the current value of fex_map
        """
        return self._device_info["fexMap"]

    @property
    def fid(self):
        """
        return the current value of fid
        """
        return self._device_info["fid"]

    @property
    def freeze_mode(self):
        """
        return the current value of freeze_mode
        """
        return self._device_info["freezeMode"]

    @property
    def health(self):
        """
        return the current value of health
        """
        return self._device_info["health"]

    @property
    def host_name(self):
        """
        return the current value of host_name
        """
        return self._device_info["hostName"]

    @property
    def index(self):
        """
        return the current value of index
        """
        return self._device_info["index"]

    @property
    def interfaces(self):
        """
        return the current value of interfaces
        """
        return self._device_info["interfaces"]

    # ip_address (see Public read-write properties)

    @property
    def ip_domain(self):
        """
        return the current value of ip_domain
        """
        return self._device_info["ipDomain"]

    @property
    def is_ech_support(self):
        """
        return the current value of is_ech_support
        """
        return self._device_info["isEchSupport"]

    @property
    def is_lan(self):
        """
        return the current value of is_lan
        """
        return self._device_info["isLan"]

    @property
    def is_non_nexus(self):
        """
        return the current value of is_non_nexus
        """
        return self._device_info["isNonNexus"]

    @property
    def is_pm_collect(self):
        """
        return the current value of is_pm_collect
        """
        return self._device_info["isPmCollect"]

    @property
    def is_trap_delayed(self):
        """
        return the current value of is_trap_delayed
        """
        return self._device_info["isTrapDelayed"]

    @property
    def is_vpc_configured(self):
        """
        return the current value of is_vpc_configured
        """
        return self._device_info["isVpcConfigured"]

    @property
    def is_smlic_enabled(self):
        """
        return the current value of is_smlic_enabled
        """
        return self._device_info["is_smlic_enabled"]

    @property
    def keep_alive_state(self):
        """
        return the current value of keep_alive_state
        """
        return self._device_info["keepAliveState"]

    @property
    def last_scan_time(self):
        """
        return the current value of last_scan_time
        """
        return self._device_info["lastScanTime"]

    @property
    def license_detail(self):
        """
        return the current value of license_detail
        """
        return self._device_info["licenseDetail"]

    @property
    def license_violation(self):
        """
        return the current value of license_violation
        """
        return self._device_info["licenseViolation"]

    @property
    def link_name(self):
        """
        return the current value of link_name
        """
        return self._device_info["linkName"]

    @property
    def location(self):
        """
        return the current value of location
        """
        return self._device_info["location"]

    @property
    def logical_name(self):
        """
        return the current value of logical_name
        """
        return self._device_info["logicalName"]

    @property
    def managable(self):
        """
        return the current value of managable
        """
        return self._device_info["managable"]

    @property
    def mds(self):
        """
        return the current value of mds
        """
        return self._device_info["mds"]

    @property
    def membership(self):
        """
        return the current value of membership
        """
        return self._device_info["membership"]

    @property
    def memory_usage(self):
        """
        return the current value of memory_usage
        """
        return self._device_info["memoryUsage"]

    @property
    def mgmt_address(self):
        """
        return the current value of mgmt_address
        """
        return self._device_info["mgmtAddress"]

    @property
    def mode(self):
        """
        return the current value of mode
        """
        return self._device_info["mode"]

    @property
    def model(self):
        """
        return the current value of model
        """
        return self._device_info["model"]

    @property
    def model_type(self):
        """
        return the current value of model_type
        """
        return self._device_info["modelType"]

    @property
    def module_index_offset(self):
        """
        return the current value of module_index_offset
        """
        return self._device_info["moduleIndexOffset"]

    @property
    def modules(self):
        """
        return the current value of modules
        """
        return self._device_info["modules"]

    @property
    def monitor_mode(self):
        """
        return the current value of monitor_mode
        """
        return self._device_info["monitorMode"]

    @property
    def name(self):
        """
        return the current value of name
        """
        return self._device_info["name"]

    @property
    def network(self):
        """
        return the current value of network
        """
        return self._device_info["network"]

    @property
    def non_mds_model(self):
        """
        return the current value of non_mds_model
        """
        return self._device_info["nonMdsModel"]

    @property
    def npv_enabled(self):
        """
        return the current value of npv_enabled
        """
        return self._device_info["npvEnabled"]

    @property
    def number_of_ports(self):
        """
        return the current value of number_of_ports
        """
        return self._device_info["numberOfPorts"]

    @property
    def oper_status(self):
        """
        return the current value of oper_status
        """
        return self._device_info["operStatus"]

    @property
    def peer(self):
        """
        return the current value of peer
        """
        return self._device_info["peer"]

    @property
    def peer_serial_number(self):
        """
        return the current value of peer_serial_number
        """
        return self._device_info["peerSerialNumber"]

    @property
    def peer_switch_db_id(self):
        """
        return the current value of peer_switch_db_id
        """
        return self._device_info["peerSwitchDbId"]

    @property
    def peerlink_state(self):
        """
        return the current value of peerlink_state
        """
        return self._device_info["peerlinkState"]

    @property
    def ports(self):
        """
        return the current value of ports
        """
        return self._device_info["ports"]

    @property
    def present(self):
        """
        return the current value of present
        """
        return self._device_info["present"]

    @property
    def primary_ip(self):
        """
        return the current value of primary_ip
        """
        return self._device_info["primaryIP"]

    @property
    def primary_switch_db_id(self):
        """
        return the current value of primary_switch_db_id
        """
        return self._device_info["primarySwitchDbID"]

    @property
    def principal(self):
        """
        return the current value of principal
        """
        return self._device_info["principal"]

    @property
    def recv_intf(self):
        """
        return the current value of recv_intf
        """
        return self._device_info["recvIntf"]

    @property
    def release(self):
        """
        return the current value of release
        """
        return self._device_info["release"]

    @property
    def status_code(self):
        """
        return the status_code from the last refresh()
        """
        return self._status_code

    @property
    def role(self):
        """
        return the current value of role
        """
        return self._device_info["role"]

    @property
    def san_analytics_capable(self):
        """
        return the current value of san_analytics_capable
        """
        return self._device_info["sanAnalyticsCapable"]

    @property
    def scope(self):
        """
        return the current value of scope
        """
        return self._device_info["scope"]

    @property
    def secondary_ip(self):
        """
        return the current value of secondary_ip
        """
        return self._device_info["secondaryIP"]

    @property
    def secondary_switch_db_id(self):
        """
        return the current value of secondary_switch_db_id
        """
        return self._device_info["secondarySwitchDbID"]

    @property
    def send_intf(self):
        """
        return the current value of send_intf
        """
        return self._device_info["sendIntf"]

    @property
    def serial_number(self):
        """
        return the current value of serial_number
        """
        return self._device_info["serialNumber"]

    @property
    def source_interface(self):
        """
        return the current value of source_interface
        """
        return self._device_info["sourceInterface"]

    @property
    def source_vrf(self):
        """
        return the current value of source_vrf
        """
        return self._device_info["sourceVrf"]

    @property
    def standby_sup_state(self):
        """
        return the current value of standby_sup_state
        """
        return self._device_info["standbySupState"]

    @property
    def status(self):
        """
        return the current value of status
        """
        return self._device_info["status"]

    @property
    def sw_type(self):
        """
        return the current value of sw_type
        """
        return self._device_info["swType"]

    @property
    def sw_uuid(self):
        """
        return the current value of sw_uuid
        """
        return self._device_info["swUUID"]

    @property
    def sw_uuid_id(self):
        """
        return the current value of sw_uuid_id
        """
        return self._device_info["swUUIDId"]

    @property
    def sw_wwn(self):
        """
        return the current value of sw_wwn
        """
        return self._device_info["swWwn"]

    @property
    def sw_wwn_name(self):
        """
        return the current value of sw_wwn_name
        """
        return self._device_info["swWwnName"]

    @property
    def switch_db_id(self):
        """
        return the current value of switch_db_id
        """
        return self._device_info["switchDbID"]

    @property
    def switch_role(self):
        """
        return the current value of switch_role
        """
        return self._device_info["switchRole"]

    @property
    def switch_role_enum(self):
        """
        return the current value of switch_role_enum
        """
        return self._device_info["switchRoleEnum"]

    @property
    def sys_descr(self):
        """
        return the current value of sys_descr
        """
        return self._device_info["sysDescr"]

    @property
    def system_mode(self):
        """
        return the current value of system_mode
        """
        return self._device_info["systemMode"]

    @property
    def uid(self):
        """
        return the current value of uid
        """
        return self._device_info["uid"]

    @property
    def unmanagable_cause(self):
        """
        return the current value of unmanagable_cause
        """
        return self._device_info["unmanagableCause"]

    @property
    def up_time(self):
        """
        return the current value of up_time
        """
        return self._device_info["upTime"]

    @property
    def up_time_number(self):
        """
        return the current value of up_time_number
        """
        return self._device_info["upTimeNumber"]

    @property
    def up_time_str(self):
        """
        return the current value of up_time_str
        """
        return self._device_info["upTimeStr"]

    @property
    def used_ports(self):
        """
        return the current value of used_ports
        """
        return self._device_info["usedPorts"]

    @property
    def username(self):
        """
        return the current value of username
        """
        return self._device_info["username"]

    @property
    def vdc_id(self):
        """
        return the current value of vdc_id
        """
        return self._device_info["vdcId"]

    @property
    def vdc_mac(self):
        """
        return the current value of vdc_mac
        """
        return self._device_info["vdcMac"]

    @property
    def vdc_name(self):
        """
        return the current value of vdc_name
        """
        return self._device_info["vdcName"]

    @property
    def vendor(self):
        """
        return the current value of vendor
        """
        return self._device_info["vendor"]

    @property
    def version(self):
        """
        return the current value of version
        """
        return self._device_info["version"]

    @property
    def vpc_domain(self):
        """
        return the current value of vpc_domain
        """
        return self._device_info["vpcDomain"]

    @property
    def vrf(self):
        """
        return the current value of vrf
        """
        return self._device_info["vrf"]

    @property
    def vsan_wwn(self):
        """
        return the current value of vsan_wwn
        """
        return self._device_info["vsanWwn"]

    @property
    def vsan_wwn_name(self):
        """
        return the current value of vsan_wwn_name
        """
        return self._device_info["vsanWwnName"]

    @property
    def wwn(self):
        """
        return the current value of wwn
        """
        return self._device_info["wwn"]
