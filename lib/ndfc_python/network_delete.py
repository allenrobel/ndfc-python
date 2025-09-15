"""
# Name

network_delete.py

# Description

Send network delete DELETE requests to the controller

"""

# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import inspect
import logging

from plugins.module_utils.common.properties import Properties


@Properties.add_rest_send
@Properties.add_results
class NetworkDelete:
    """
    # Summary

    Delete networks

    ## Example network delete request

    ### See

    ./examples/network_delete.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self._rest_send = None
        self._results = None
        self._network_name = None
        self._fabric_name = None

    def _final_verification(self):
        """
        final verification of all parameters
        """
        method_name = inspect.stack()[0][3]
        # pylint: disable=no-member
        if self.rest_send is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.rest_send must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.results is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.results must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)
        # pylint: enable=no-member

        if self.network_name == "":
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Call {self.class_name}.networkName before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.fabric_name == "":
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Call {self.class_name}.fabric before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if not self.fabric_exists():
            msg = f"{self.class_name}.{method_name}: "
            msg += f"fabric_name {self.fabric_name} "
            msg += "does not exist on the controller."
            raise ValueError(msg)

        if not self.ok_to_delete_network():
            msg = f"{self.class_name}.{method_name}: "
            msg += f"network_name {self.network_name} "
            msg += f"either does not exist in fabric {self.fabric_name}, "
            msg += "or its status is DEPLOYED.  Check the network status "
            msg += "and either create or detach the network before "
            msg += "attempting to delete it."
            raise ValueError(msg)

    def fabric_exists(self) -> bool:
        """
        Return True if self.fabric_name exists on the controller.
        Return False otherwise.
        """
        method_name = inspect.stack()[0][3]
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/msd/fabric-associations"
        verb = "GET"

        # pylint: disable=no-member
        try:
            self.rest_send.path = path  # type: ignore[attr-defined]
            self.rest_send.verb = verb  # type: ignore[attr-defined]
            self.rest_send.commit()  # type: ignore[attr-defined]
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        for item in self.rest_send.response_current["DATA"]:  # type: ignore[attr-defined]
            if item.get("fabricName") == self.fabric_name:
                return True
        # pylint: enable=no-member
        return False

    def vrf_exists_in_fabric(self):
        """
        Return True if self.vrf_name exists in self.fabric_name.
        Else, return False
        """
        method_name = inspect.stack()[0][3]
        # TODO: update when this path is added to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/vrfs"
        verb = "GET"

        # pylint: disable=no-member
        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        for item_d in self.rest_send.response_current["DATA"]:
            if "fabric" not in item_d:
                continue
            if "vrfName" not in item_d:
                continue
            if item_d["fabric"] != self.fabric_name:
                continue
            if item_d["vrfName"] != self.vrf_name:
                continue
            return True
        # pylint: enable=no-member
        return False

    def ok_to_delete_network(self):
        """
        Return True if network_name exists in fabric_name and its status is not DEPLOYED.
        Return False otherwise.
        """
        method_name = inspect.stack()[0][3]
        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/networks"
        verb = "GET"

        # pylint: disable=no-member
        try:
            self.rest_send.path = path
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
        for item in self.rest_send.response_current["DATA"]:
            if "networkName" not in item:
                continue
            if item["networkName"] == self.network_name:
                network_status = item.get("networkStatus")
                msg = f"{self.class_name}.{method_name}: "
                msg += f"fabric_name {self.fabric_name}, "
                msg += f"network_name {self.network_name}, "
                msg += f"status: {network_status}."
                self.log.debug(msg)
                if network_status != "DEPLOYED":
                    return True
        return False

    def commit(self):
        """
        Delete a network
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        # TODO: Update when we add endpoint to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/networks/{self.network_name}"
        verb = "DELETE"
        # pylint: disable=no-member
        try:
            self.rest_send.path = path
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

    # top_level properties
    @property
    def fabric_name(self):
        """
        return the current payload value of fabric
        """
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value):
        self._fabric_name = value

    @property
    def network_name(self):
        """
        return the current payload value of network_name
        """
        return self._network_name

    @network_name.setter
    def network_name(self, value):
        self._network_name = value
