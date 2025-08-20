"""
Name: config_save.py
Description: Save the current configuration on the NDFC controller.

The JSON payload constructed by this class is shown below.

```json
{}
```

# Example controller response (rest_send.response_current):

```json
{
    "RETURN_CODE": 200,
    "DATA": {
        "status": "Config save is completed"
    },
    "MESSAGE": "OK",
    "METHOD": "POST",
    "REQUEST_PATH": "https://192.168.7.7/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/SITE2/config-save"
}
```
"""

# We're using isort for import linting
# pylint: disable=wrong-import-order

import inspect
import logging

from ndfc_python.validations import Validations
from plugins.module_utils.common.api.v1.lan_fabric.rest.control.fabrics.fabrics import EpFabrics
from plugins.module_utils.common.conversion import ConversionUtils
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.fabric.fabric_details_v2 import FabricDetailsByName


@Properties.add_rest_send
@Properties.add_results
class ConfigSave:
    """
    # Summary

    Save the current configuration on the NDFC controller.

    # Usage example

    See the following script.

    ./examples/config_save.py
    """

    def __init__(self):
        self.class_name = __class__.__name__

        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.conversion = ConversionUtils()
        self.validations = Validations()
        self.ep_rest_control_fabrics = EpFabrics()

        self._response_data = None

        self._init_payload()

    def _init_payload(self):
        """
        Initialize the REST payload
        """
        self.payload = {}

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
        Any final verification steps before sending the request
        """

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
        Send a POST request to the controller to the config-save endpoint
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
            self.rest_send.path = f"{path.path_fabric_name}/config-save"
            self.rest_send.payload = self.payload
            self.rest_send.verb = verb
            self.rest_send.save_settings()
            self.rest_send.retries = 1
            # config-save can take a while
            self.rest_send.timeout = 300
            self.rest_send.commit()
            self.rest_send.restore_settings()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Unable to send {self.rest_send.verb} request to the controller. "
            msg += f"Error details: {error}"
            raise ValueError(msg) from error

        self._response_data = self.rest_send.response_current.get("DATA")
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
        return self.response_data.get(item)

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
    def response_data(self):
        """
        Return the data retrieved from the request
        """
        return self._response_data

    # Controller response accessors
    @property
    def status(self):
        """
        auth key from controller response
        """
        return self._get("status")
