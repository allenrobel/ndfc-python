"""
Name: vrf_delete.py
Description: Delete VRFs
"""

# We use isort for import linting
# pylint: disable=wrong-import-order
import copy
import inspect
import logging
import re

from ndfc_python.common.properties import Properties
from ndfc_python.validations import Validations


class VrfDelete:
    """
    # Summary

    Delete VRFs

    ## Usage

    See examples/vrf_delete.py
    """

    def __init__(self):
        self.class_name = __class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.properties = Properties()
        self.rest_send = self.properties.rest_send
        self.results = self.properties.results

        self.validations = Validations()

        self._rest_send = None
        self._results = None
        # _vrf_cache is keyed on fabric_name
        # The value is a dictionary, keyed on vrf_name.
        # _vrf_cache = {
        #     "fabric_1": {
        #        "vrf_1": {
        #            "fabric": "fabric_1",
        #            "vrfName": "vrf_1",
        #            "vrfTemplate": "Default_VRF_Universal",
        #            "vrfExtensionTemplate": "Default_VRF_Extension_Universal",
        #            "vrfTemplateConfig": "stringified template config key/value pairs"
        #            "id": 12,
        #            "vrfId": 50002,
        #            "tenantName": "",
        #            "vrfServiceTemplate": null,
        #            "source": null,
        #            "vrfStatus": "NA",
        #            "hierarchicalKey": "fabric_1"
        #            etc...
        #        },
        #        "vrf_2": {vrf info for vrf_2}
        #     },
        #    "fabric_2": {
        #        "vrf_3": {vrf info for vrf_3},
        #        "vrf_4": {vrf info for vrf_4}
        #    }
        # }
        self._vrf_cache = {}

        self._fabric_name = None
        self._vrf_names = None

    def _final_verification(self) -> None:
        """
        # Summary

        Verify the following:

        - verify rest_send is set
        - verify results is set
        - Each vrf in self.vrf_names exists in self.fabric_name

        # Raises

        - `ValueError` if above verifications fail.
        """
        method_name = inspect.stack()[0][3]
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

        if self.fabric_name is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.fabric_name must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        if self.vrf_names is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{self.class_name}.vrf_names must be set before calling "
            msg += f"{self.class_name}.commit"
            raise ValueError(msg)

        self.get_vrfs()

        for vrf_name in self.vrf_names:
            if self.vrf_exists_in_fabric(vrf_name) is False:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"VRF {vrf_name} does not exist in "
                msg += f"fabric {self.fabric_name}"
                raise ValueError(msg)

    def commit(self) -> None:
        """
        # Summary

        Commit VRF deletion

        ## Raises

        - ValueError if an error is encountered while sending the request.
        """
        method_name = inspect.stack()[0][3]
        self._final_verification()

        vrf_names = ",".join(self.vrf_names)
        # TODO: update when this path is added to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/bulk-delete/vrfs?vrf-names={vrf_names}"

        try:
            self.rest_send.path = path
            self.rest_send.verb = "DELETE"
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        if self.rest_send.result_current.get("success") is False:
            failure_list = self.rest_send.response_current.get("DATA", {}).get("failureList", [])
            errmsg = ", ".join([item.get("message", "") for item in failure_list])
            errmsg = re.sub(r"\t", " ", errmsg)
            msg = f"{self.class_name}.{method_name}: "
            msg += "RestSend returned an unsuccessful result "
            msg += f"{self.rest_send.result_current}. "
            msg += f"More detail (if any): {errmsg}"
            raise ValueError(msg)

    def get_vrfs(self) -> None:
        """
        # Summary

        Get information for all vrfs in self.fabric_name and cache the results.

        For each vrf in self.fabric_name, set:

        self._vrf_cache[self.fabric_name][vrf_name] = {vrf_info dict}

        ## Raises

        -   `ValueError` if errors are encountered retrieving VRF information
            from the controller.
        """
        if self._vrf_cache.get(self.fabric_name) is not None:
            return
        method_name = inspect.stack()[0][3]
        # TODO: update when this path is added to ansible-dcnm
        path = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
        path += f"/{self.fabric_name}/vrfs"
        verb = "GET"

        try:
            self.rest_send.path = path
            self.rest_send.verb = verb
            self.rest_send.commit()
            data = self.rest_send.response_current["DATA"]
            if not isinstance(data, list):
                if data.get("message") == "Resource not found":
                    error = f"Fabric {self.fabric_name} does not exist "
                    error += "on the controller."
                else:
                    error = data.get("message")
                raise ValueError(error)

            if self.fabric_name not in self._vrf_cache:
                self._vrf_cache[self.fabric_name] = {}

            for item in data:
                vrf_name = item.get("vrfName")
                if vrf_name is None:
                    continue
                self._vrf_cache[self.fabric_name][vrf_name] = copy.deepcopy(item)
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{error}"
            raise ValueError(msg) from error

    def vrf_exists_in_fabric(self, vrf_name: str) -> bool:
        """
        # Summary

        Return True if `vrf_name` exists in fabric `self.fabric_name`.

        Return False otherwise.
        """
        if self.fabric_name not in self._vrf_cache:
            return False
        if vrf_name not in self._vrf_cache[self.fabric_name]:
            return False
        return True

    @property
    def fabric_name(self) -> str:
        """
        # Summary

        The fabric_name set by the user
        """
        return self._fabric_name

    @fabric_name.setter
    def fabric_name(self, value: str):
        self._fabric_name = value

    @property
    def vrf_names(self) -> str:
        """
        The list of vrf names set by the user
        """
        return self._vrf_names

    @vrf_names.setter
    def vrf_names(self, value: str) -> None:
        if not isinstance(value, list):
            msg = "vrf_names must be a list of vrf names. "
            msg += f"Got: {value}"
            raise ValueError(msg)
        self._vrf_names = value
