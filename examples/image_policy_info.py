#!/usr/bin/env python

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
from ndfc_python.validators.image_policy_info import ImagePolicyInfoConfigValidator
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.image_policy.image_policies import ImagePolicies
from plugins.module_utils.image_policy.query import ImagePolicyQuery
from pydantic import ValidationError


@Properties.add_rest_send
class Query:
    """
    Handle query state
    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]
        self.state = "query"
        self.check_mode = False

        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.image_policies = None
        self.query = None
        self._rest_send = None

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def commit(self) -> None:
        """
        1.  query the fabrics in self.want that exist on the controller
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}: "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        if self._rest_send is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Set rest_send before calling commit."
            raise ValueError(msg)

        if self.want is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Set want before calling commit."
            raise ValueError(msg)

        if len(self.want) == 0:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Nothing to query."
            print("msg")
            return

        policy_names_to_query = set()
        for want in self.want:
            policy_names_to_query.add(want["name"])

        self.image_policies = ImagePolicies()
        self.image_policies.rest_send = self._rest_send
        self.image_policies.results = self._rest_send.results

        params = {}
        params["check_mode"] = self.check_mode
        params["state"] = self.state

        self.query = ImagePolicyQuery()
        self.query.params = params
        self.query.results = self._rest_send.results
        self.query.rest_send = self._rest_send
        self.query.image_policies = self.image_policies
        self.query.policy_names = list(policy_names_to_query)
        self.query.commit()

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
    description += "Query one or more image policies by name."
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


def main():
    """
    main entry point for module execution
    """
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
        ImagePolicyInfoConfigValidator(**ndfc_config.contents)
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

    rest_send = RestSend({})
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
        err_msg = "unable to query image policies"
        log.error(err_msg)
        print(err_msg)
    print(json.dumps(task.rest_send.results.final_result, indent=4, sort_keys=True))  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
