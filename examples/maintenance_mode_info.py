#!/usr/bin/env python3
"""
# maintenance_mode_info.py

## Description

Query maintenance mode status for a switch or switches.

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ndfc-python/lib:$HOME/repos/ansible-dcnm
```

2. Optional, to enable logging.

``` bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

3. Edit ./examples/config/config_maintenance_mode_info.yaml with desired values

4. Set credentials via script command line, environment variables, or Ansible Vault

5. Run the script (below we're using command line for credentials)

``` bash
./examples/maintenance_mode_info.py \
    --config ./examples/config/config_maintenance_mode_info.yaml \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin

```

"""
import argparse
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
from ndfc_python.validators import MaintenanceModeInfoConfigValidator
from plugins.module_utils.common.maintenance_mode_info import MaintenanceModeInfo
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from pydantic import ValidationError


@Properties.add_rest_send
class Query:
    """
    Handle query state

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

        msg = f"ENTERED Query.{method_name}: "
        self.log.debug(msg)

        self._rest_send = None
        self.have = {}
        self._want = None

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

    def commit(self):
        """
        ### Summary
        Query the switches in self.want that exist on the controller
        and update ``self.results`` with the query results.

        ### Raises
        -   ``ValueError`` if:
                -   ``rest_send`` is not set.
                -   ``get_want()`` raises ``ValueError``
                -   ``get_have()`` raises ``ValueError``
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
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error while retrieving switch information "
            msg += "from the controller. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        # If we got this far, the requests were successful.
        self.rest_send.results.action = "maintenance_mode_info"
        self.rest_send.results.changed = False
        self.rest_send.results.diff_current = self.have
        self.rest_send.results.failed = False
        self.rest_send.results.response_current = {"MESSAGE": "MaintenanceModeInfo OK."}
        self.rest_send.results.response_current.update({"METHOD": "NA"})
        self.rest_send.results.response_current.update({"REQUEST_PATH": "NA"})
        self.rest_send.results.response_current.update({"RETURN_CODE": 200})
        self.rest_send.results.result_current = {"changed": False, "success": True}
        self.rest_send.results.register_task_result()

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
    description = "DESCRIPTION: "
    description += "Query the maintenance mode state of one or more switches."
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
        description=description,
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

try:
    validator = MaintenanceModeInfoConfigValidator(**ndfc_config.contents)
except ValidationError as error:
    err_msg = f"{error}"
    log.error(err_msg)
    print(err_msg)
    sys.exit(1)

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
    task = Query()
    # pylint: disable=attribute-defined-outside-init
    task.rest_send = rest_send  # type: ignore[attr-defined]
    task.want = ndfc_config.contents["config"]
    task.commit()
except ValueError as error:
    err_msg = f"Exiting.  Error detail: {error}"
    log.error(err_msg)
    print(err_msg)
    sys.exit(1)

task.rest_send.results.build_final_result()  # type: ignore[attr-defined]
# pylint: disable=unsupported-membership-test
if True in task.rest_send.results.failed:  # type: ignore[attr-defined]
    err_msg = "unable to set maintenance mode"
    log.error(err_msg)
    print(err_msg)
print(json.dumps(task.rest_send.results.final_result, indent=4, sort_keys=True))  # type: ignore[attr-defined]
