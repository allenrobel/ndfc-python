import logging
import sys

from plugins.module_utils.common.properties import Properties


@Properties.add_rest_send
class FabricInventory:
    """
    # Summary

    Class to retrieve fabric inventory information.

    ## Usage

    See examples/fabric_inventory.py

    ## Properties
    - fabric_name (str): getter/setter: name of the fabric to query
    - rest_send (RestSend): getter/setter: RestSend instance to use for REST calls
    - devices (list): getter: list of device names in the fabric inventory
    - inventory (dict): getter: fabric inventory dictionary, keyed on device name
    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")
        self._committed = False
        self._fabric_name = None
        self._inventory = {}
        self.api_v1 = "/appcenter/cisco/ndfc/api/v1"
        self.ep_fabrics = f"{self.api_v1}/lan-fabric/rest/control/fabrics"

    def final_verification(self) -> None:
        """
        Verify that required properties have been set.
        """
        if self.fabric_name is None:
            msg = f"{self.class_name}.final_verification: fabric_name must be set."
            raise ValueError(msg)
        # pylint: disable=no-member
        if self.rest_send is None:  # type: ignore[attr-defined]
            msg = f"{self.class_name}.final_verification: rest_send must be set."
            raise ValueError(msg)
        # pylint: enable=no-member

    def commit(self) -> None:
        """Get switches for a specific fabric.

        Populates self.fabric_switches:
            dict keyed on switch_name, containing switch details.

        Example:

            {
                "VP3": {
                    "switchRoleEnum": "Leaf",
                    "vrf": "management",
                    "fabricTechnology": "VXLANFabric",
                    "deviceType": "Switch_Fabric",
                    "fabricId": 4,
                    "name": null,
                    "domainID": 0,
                    "wwn": null,
                    "membership": null,
                    "ports": 0,
                    "model": "N9K-C9300v",
                    "version": null,
                    "upTime": 0,
                    "ipAddress": "192.168.14.153",
                    "mgmtAddress": null,
                    "vendor": "Cisco",
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
                    "fabricName": "SITE4",
                    "modelType": 0,
                    "logicalName": "VP3",
                    "switchDbID": 30820,
                    "uid": 0,
                    "release": "10.3(8)",
                    "location": null,
                    "contact": null,
                    "upTimeStr": "01:58:36",
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
                    "serialNumber": "9EJ4B3H5GJ3",
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
                    "switchRole": "leaf",
                    "mode": "Normal",
                    "hostName": "VP3",
                    "ipDomain": "",
                    "systemMode": "Normal",
                    "waitForSwitchModeChg": false,
                    "sourceVrf": "management",
                    "sourceInterface": "mgmt0",
                    "protoDiscSettings": null,
                    "operMode": null,
                    "modules": null,
                    "fexMap": {},
                    "isVpcConfigured": true,
                    "vpcDomain": 1,
                    "role": "Primary",
                    "peer": "VP4",
                    "peerSerialNumber": "9XUGSGI5J1O",
                    "peerSwitchDbId": 30780,
                    "peerlinkState": "Peer is OK",
                    "keepAliveState": "Peer is alive",
                    "consistencyState": true,
                    "sendIntf": "Eth1/1",
                    "recvIntf": "Lo0",
                    "interfaces": null,
                    "elementType": null,
                    "monitorMode": null,
                    "freezeMode": null,
                    "cfsSyslogStatus": 1,
                    "isNonNexus": false,
                    "swUUIDId": 30670,
                    "swUUID": "DCNM-UUID-30670",
                    "swType": null,
                    "ccStatus": "In-Sync",
                    "operStatus": "Minor",
                    "intentedpeerName": "VP4",
                    "sharedBorder": false,
                    "isSharedBorder": false
                },
                "switch2": {
                    switch_details
                }
            }
        """
        self.final_verification()
        verb = "GET"
        path = f"{self.ep_fabrics}/{self.fabric_name}/inventory/switchesByFabric"
        # pylint: disable=no-member
        try:
            self.rest_send.path = path  # type: ignore[attr-defined]
            self.rest_send.verb = verb  # type: ignore[attr-defined]
            self.rest_send.commit()  # type: ignore[attr-defined]
        except (TypeError, ValueError) as error:
            msg = f"Unable to send {verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        if self.rest_send.response_current.get("RETURN_CODE") not in [200, 201]:  # type: ignore[attr-defined]
            msg = f"Unable to retrieve fabric inventory for fabric {self.fabric_name}. "
            msg += f"Controller response: {self.rest_send.response_current}."  # type: ignore[attr-defined]
            raise ValueError(msg)
        for switch in self.rest_send.response_current.get("DATA", []):  # type: ignore[attr-defined]
            switch_name = switch.get("logicalName")
            if switch_name is None:
                continue
            self._inventory[switch_name] = switch
        self._committed = True

    def switch_name_to_serial_number(self, switch_name: str) -> str:
        """
        Given a switch_name, return the associated serial number.
        """
        if not self._committed:
            self.commit()
        switch = self.inventory.get(switch_name)
        if switch is None:
            msg = f"Switch name {switch_name} not found in fabric {self.fabric_name}."
            raise ValueError(msg)
        serial_number = switch.get("serialNumber")
        if serial_number is None:
            msg = f"Switch name {switch_name} has no serial number in fabric {self.fabric_name}."
            raise ValueError(msg)
        return serial_number

    @property
    def devices(self):
        """
        return a list of device names in the fabric inventory
        """
        if not self._committed:
            self.commit()
        return list(self.inventory.keys())

    @property
    def inventory(self):
        """
        return the fabric inventory dictionary
        """
        if not self._committed:
            self.commit()
        return self._inventory

    @property
    def fabric_name(self) -> str:
        """
        return the current value of fabric
        """
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value: str) -> None:
        self._fabric_name = value


if __name__ == "__main__":
    print("This is a library of common utilities for ND Python.")
    print("It is not meant to be executed directly.")
    sys.exit(1)
