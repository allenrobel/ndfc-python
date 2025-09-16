import logging
import sys

from ndfc_python.common.properties import Properties


class FabricsInfo:
    """
    # Summary

    Class to retrieve information for all fabrics.

    ## Usage

    See examples/fabrics_info.py

    ## Properties
    - rest_send (RestSend): getter/setter: RestSend instance to use for REST calls
    - results (Results): getter/setter: Results instance to manage controller responses
    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.properties = Properties()
        self.rest_send = self.properties.rest_send

        self._committed = False
        self._filter = None
        self._fabrics_by_fabric_name = {}
        self._fabrics = []
        self._return_code = 0
        self.api_v1 = "/appcenter/cisco/ndfc/api/v1"
        self.ep_path = f"{self.api_v1}/lan-fabric/rest/control/fabrics"
        self.ep_verb = "GET"

    def final_verification(self) -> None:
        """
        Verify that required properties have been set.
        """
        if self.rest_send is None:
            msg = f"{self.class_name}.final_verification: rest_send must be set."
            raise ValueError(msg)

    def commit(self) -> None:
        """Retrieve information for all fabrics.

        Populates self._fabrics_by_fabric_name.:
            dict keyed on fabric_name, containing fabric details.

        """
        self.final_verification()
        try:
            self.rest_send.path = self.ep_path
            self.rest_send.verb = self.ep_verb
            self.rest_send.commit()
        except (TypeError, ValueError) as error:
            msg = f"Unable to send {self.ep_verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error
        self._return_code = self.rest_send.response_current.get("RETURN_CODE", 0)
        if self._return_code not in [200, 201]:
            msg = "Unable to retrieve fabrics information. "
            msg += f"Controller response: {self.rest_send.response_current}."
            raise ValueError(msg)
        self._fabrics = self.rest_send.response_current.get("DATA", [])
        self._build_fabrics_by_fabric_name()
        self._committed = True

    def _build_fabrics_by_fabric_name(self) -> None:
        """Build the fabric inventory keyed on fabric name."""
        self._fabrics_by_fabric_name = {}
        for fabric in self._fabrics:
            fabric_name = fabric.get("nvPairs", {}).get("FABRIC_NAME")
            if not fabric_name:
                continue
            self._fabrics_by_fabric_name[fabric_name] = fabric

    @property
    def fabric(self) -> dict:
        """
        Return information for the fabric specified in self.filter
        as a dictionary.

        Return an empty dictionary if the fabric does not exist

        instance.filter must be set to a fabric name before calling fabric
        """
        if not self._committed:
            self.commit()
        return self._fabrics_by_fabric_name.get(self._filter, {})

    @property
    def fabric_exists(self) -> bool:
        """
        return True if the filtered fabric exists on the controller

        instance.filter must be set to a fabric name before calling fabric_exists
        """
        if not self._filter:
            msg = f"{self.class_name}.fabric_exists: "
            msg += "instance.filter must be set to a fabric name before calling fabric_exists."
            raise ValueError(msg)
        if not isinstance(self._filter, str):
            msg = f"{self.class_name}.fabric_exists: "
            msg += "filter must be a string."
            raise ValueError(msg)
        if not self._committed:
            self.commit()
        return bool(self._fabrics_by_fabric_name.get(self._filter))

    @property
    def fabrics(self) -> list:
        """
        return all fabrics as a list of dictionaries
        """
        if not self._committed:
            self.commit()
        return self._fabrics

    @property
    def fabrics_by_fabric_name(self) -> dict:
        """
        return the fabric inventory dictionary keyed on fabric name
        """
        if not self._committed:
            self.commit()
        return self._fabrics_by_fabric_name

    @property
    def filter(self) -> str:
        """
        filter (setter) accepts a fabric_name and filter (getter) returns the current value of filter
        """
        return self._filter

    @filter.setter
    def filter(self, value: str) -> None:
        self._filter = value

    @property
    def return_code(self) -> int:
        """
        return the current value of return_code as an integer
        """
        if not self._committed:
            self.commit()
        return self._return_code


if __name__ == "__main__":
    print("This is a library for ND Python.")
    print("It is not meant to be executed directly.")
    sys.exit(1)
