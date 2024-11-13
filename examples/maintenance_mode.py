#!/usr/bin/env python3
"""
# maintenance_mode.py

## Description

Enable or disable maintenance mode for a switch or switches.

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible-dcnm
```

2. Optional, to enable logging.

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

3. Edit ./examples/config/config_maintenance_mode.yaml with desired values

4. Set credentials via script command line, environment variables, or Ansible Vault

5. Run the script (below we're using command line for credentials)

``` bash
./examples/maintenance_mode.py \
    --config ./examples/config/config_network_create.yaml \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin

```

"""
import argparse
import copy
import inspect
import json
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.parsers.parser_nxos_password import parser_nxos_password
from ndfc_python.parsers.parser_nxos_username import parser_nxos_username
from ndfc_python.read_config import ReadConfig
from plugins.module_utils.common.maintenance_mode import MaintenanceMode
from plugins.module_utils.common.maintenance_mode_info import MaintenanceModeInfo
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results

# from pydantic import ValidationError


@Properties.add_rest_send
class Merged:
    """
    Handle merged state

    ### Raises
    -   ``ValueError`` if Common().__init__() raises ``ValueError``
    """

    def __init__(self):
        """
        ### Raises
        -   ``ValueError`` if Common().__init__() raises ``ValueError``
        """
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        method_name = inspect.stack()[0][3]

        # params = {}
        # params["check_mode"] = False
        # params["state"] = "merged"

        msg = f"ENTERED Merged.{method_name}: "
        self.log.debug(msg)

        self.rest_send = None
        self.have = {}
        self.need = []
        self._want = None
        self.maintenance_mode = None

    def get_have(self):
        """
        ### Summary
        Build self.have, a dict containing the current mode of all switches.

        ### Raises
        -   ``ValueError`` if self.ansible_module is not set
        -   ``ValueError`` if MaintenanceModeInfo() raises ``ValueError``

        ### self.have structure
        Have is a dict, keyed on switch_ip, where each element is a dict
        with the following structure:
        -   ``fabric_name``: The name of the switch's hosting fabric.
        -   ``fabric_freeze_mode``: The current ``freezeMode`` state of the switch's
            hosting fabric.  If ``freeze_mode`` is True, configuration changes cannot
            be made to the fabric or the switches within the fabric.
        -   ``fabric_read_only``: The current ``IS_READ_ONLY`` state of the switch's
            hosting fabric.  If ``fabric_read_only`` is True, configuration changes cannot
            be made to the fabric or the switches within the fabric.
        -   ``mode``: The current maintenance mode of the switch.
            Possible values include: , ``inconsistent``, ``maintenance``,
            ``migration``, ``normal``.
        -   ``role``: The role of the switch in the hosting fabric, e.g.
            ``spine``, ``leaf``, ``border_gateway``, etc.
        -   ``serial_number``: The serial number of the switch.

        ```json
        {
            "192.169.1.2": {
                fabric_deployment_disabled: true
                fabric_freeze_mode: true,
                fabric_name: "MyFabric",
                fabric_read_only: true
                mode: "maintenance",
                role: "spine",
                serial_number: "FCI1234567"
            },
            "192.169.1.3": {
                fabric_deployment_disabled: false
                fabric_freeze_mode: false,
                fabric_name: "YourFabric",
                fabric_read_only: false
                mode: "normal",
                role: "leaf",
                serial_number: "FCH2345678"
            }
        }
        ```
        """
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable

        try:
            instance = MaintenanceModeInfo(self.rest_send.params)
            instance.rest_send = self.rest_send
            instance.results = Results()
            instance.config = [item["ip_address"] for item in self.want]
            instance.refresh()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error while retrieving switch info. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.have = instance.info

    def fabric_deployment_disabled(self) -> None:
        """
        ### Summary
        Handle the following cases:
        -   switch migration mode is ``migration``
        -   fabric is in read-only mode (IS_READ_ONLY is True)
        -   fabric is in freeze mode (Deployment Disable)

        ### Raises
        -   ``ValueError`` if any of the above cases are true
        """
        method_name = inspect.stack()[0][3]
        for ip_address, value in self.have.items():
            fabric_name = value.get("fabric_name")
            mode = value.get("mode")
            serial_number = value.get("serial_number")
            fabric_deployment_disabled = value.get("fabric_deployment_disabled")
            fabric_freeze_mode = value.get("fabric_freeze_mode")
            fabric_read_only = value.get("fabric_read_only")

            additional_info = "Additional info: "
            additional_info += f"hosting_fabric: {fabric_name}, "
            additional_info += "fabric_deployment_disabled: "
            additional_info += f"{fabric_deployment_disabled}, "
            additional_info += "fabric_freeze_mode: "
            additional_info += f"{fabric_freeze_mode}, "
            additional_info += "fabric_read_only: "
            additional_info += f"{fabric_read_only}, "
            additional_info += f"maintenance_mode: {mode}. "

            if mode == "migration":
                msg = f"{self.class_name}.{method_name}: "
                msg += "Switch maintenance mode is in migration state for the "
                msg += "switch with "
                msg += f"ip_address {ip_address}, "
                msg += f"serial_number {serial_number}. "
                msg += "This indicates that the switch configuration is not "
                msg += "compatible with the switch role in the hosting "
                msg += "fabric.  The issue might be resolved by initiating a "
                msg += "fabric Recalculate & Deploy on the controller. "
                msg += "Failing that, the switch configuration might need to "
                msg += "be manually modified to match the switch role in the "
                msg += "hosting fabric. "
                msg += additional_info
                raise ValueError(msg)

            if fabric_read_only is True:
                msg = f"{self.class_name}.{method_name}: "
                msg += "The hosting fabric is in read-only mode for the "
                msg += f"switch with ip_address {ip_address}, "
                msg += f"serial_number {serial_number}. "
                msg += "The issue can be resolved for LAN_Classic fabrics by "
                msg += "unchecking 'Fabric Monitor Mode' in the fabric "
                msg += "settings on the controller. "
                msg += additional_info
                raise ValueError(msg)

            if fabric_freeze_mode is True:
                msg = f"{self.class_name}.{method_name}: "
                msg += "The hosting fabric is in "
                msg += "'Deployment Disable' state for the switch with "
                msg += f"ip_address {ip_address}, "
                msg += f"serial_number {serial_number}. "
                msg += "Review the 'Deployment Enable / Deployment Disable' "
                msg += "setting on the controller at: "
                msg += "Fabric Controller > Overview > "
                msg += "Topology > <fabric> > Actions > More, and change "
                msg += "the setting to 'Deployment Enable'. "
                msg += additional_info
                raise ValueError(msg)

    def get_need(self):
        """
        ### Summary
        Build self.need for merged state.

        ### Raises
        -   ``ValueError`` if the switch is not found on the controller.

        ### self.need structure
        ```json
        [
            {
                "deploy": false,
                "fabric_name": "MyFabric",
                "ip_address": "172.22.150.2",
                "mode": "maintenance",
                "serial_number": "FCI1234567"
                "wait_for_mode_change": true
            },
            {
                "deploy": true,
                "fabric_name": "YourFabric",
                "ip_address": "172.22.150.3",
                "mode": "normal",
                "serial_number": "HMD2345678"
                "wait_for_mode_change": true
            }
        ]
        """
        method_name = inspect.stack()[0][3]
        self.need = []
        for want in self.want:
            ip_address = want.get("ip_address", None)
            if ip_address not in self.have:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Switch {ip_address} not found on the controller."
                raise ValueError(msg)

            serial_number = self.have[ip_address]["serial_number"]
            fabric_name = self.have[ip_address]["fabric_name"]
            if want.get("mode") != self.have[ip_address]["mode"]:
                need = want
                need.update({"deploy": want.get("deploy")})
                need.update({"fabric_name": fabric_name})
                need.update({"ip_address": ip_address})
                need.update({"mode": want.get("mode")})
                need.update({"serial_number": serial_number})
                need.update({"wait_for_mode_change": want.get("wait_for_mode_change")})
                self.need.append(copy.copy(need))

    def patience(self) -> None:
        """
        ### Summary
        Print a message to the console for operations that can take
        a long time to complete.
        """
        msg = "Maintenance mode change can take up to 5 minutes. "
        msg += "Patience is a virtue."
        self.log.debug(msg)
        print(msg)

    def commit(self):
        """
        ### Summary
        Commit the merged state request

        ### Raises
        -   ``ValueError`` if:
                -   ``rest_send`` is not set.
                -   ``get_want()`` raises ``ValueError``
                -   ``get_have()`` raises ``ValueError``
                -   ``send_need()`` raises ``ValueError``
        """
        method_name = inspect.stack()[0][3]
        msg = f"{self.class_name}.{method_name}: entered"
        self.log.debug(msg)

        if self.rest_send is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "rest_send must be set before calling commit."
            raise ValueError(msg)

        if self.want is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "want must be set before calling commit."
            raise ValueError(msg)

        if len(self.want) == 0:
            return

        try:
            self.get_have()
        except ValueError as error:
            raise ValueError(error) from error

        self.fabric_deployment_disabled()

        self.get_need()

        try:
            self.send_need()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error while sending maintenance mode request. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

    def send_need(self) -> None:
        """
        ### Summary
        Build and send the payload to modify maintenance mode.

        ### Raises
        -   ``ValueError`` if MaintenanceMode() raises either
            ``TypeError`` or ``ValueError``

        """
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable

        if len(self.need) == 0:
            msg = f"{self.class_name}.{method_name}: "
            msg += "No switches to modify."
            self.log.debug(msg)
            return

        self.patience()
        try:
            # TODO: For now, we need to pass params to MaintenanceMode.
            # This will be changed in a future ansible-dcnm release.
            self.maintenance_mode = MaintenanceMode(self.rest_send.params)
            self.maintenance_mode.rest_send = self.rest_send
            self.maintenance_mode.results = self.rest_send.results
            self.maintenance_mode.config = self.need
            self.maintenance_mode.commit()
        except (TypeError, ValueError) as error:
            raise ValueError(error) from error

    @property
    def want(self):
        """
        ### Summary
        Return the playbook configuration.

        ### Returns
        -   list: The playbook configuration.
        """
        return self._want

    @want.setter
    def want(self, value):
        """
        ### Summary
        Set the playbook configuration.

        ### Parameters
        -   value: The playbook configuration.
        """
        self._want = value


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        parents=[
            parser_ansible_vault,
            parser_config,
            parser_loglevel,
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
            parser_nxos_password,
            parser_nxos_username,
        ],
        description="DESCRIPTION: Create a network.",
    )
    return parser.parse_args()


args = setup_parser()
NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

try:
    ndfc_config = ReadConfig()
    ndfc_config.filename = args.config
    ndfc_config.commit()
except ValueError as error:
    err_msg = f"Exiting: Error detail: {error}"
    log.error(err_msg)
    print(err_msg)
    sys.exit(1)

# TODO: Uncomment and implement MaintenanceModeConfigValidator
# try:
#     validator = MaintenanceModeConfigValidator(**ndfc_config.contents)
# except ValidationError as error:
#     msg = f"{error}"
#     log.error(msg)
#     print(msg)
#     sys.exit(1)

try:
    ndfc_sender = NdfcPythonSender()
    ndfc_sender.args = args
    ndfc_sender.commit()
except ValueError as error:
    err_msg = f"Exiting.  Error detail: {error}"
    log.error(err_msg)
    print(err_msg)
    sys.exit(1)

params = {}
params["check_mode"] = False
params["state"] = "merged"
rest_send = RestSend(params)
rest_send.sender = ndfc_sender.sender
rest_send.response_handler = ResponseHandler()
rest_send.results = Results()

try:
    task = Merged()
    task.rest_send = rest_send
    task.want = ndfc_config.contents["config"]
    task.commit()
except ValueError as error:
    err_msg = f"Exiting.  Error detail: {error}"
    log.error(err_msg)
    print(err_msg)
    sys.exit(1)

task.rest_send.results.build_final_result()
if True in task.rest_send.results.failed:  # pylint: disable=unsupported-membership-test
    err_msg = "unable to set maintenance mode"
    log.error(err_msg)
    print(err_msg)
print(json.dumps(task.rest_send.results.final_result, indent=4, sort_keys=True))
