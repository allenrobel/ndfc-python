#!/usr/bin/env python

import argparse
import json
import logging
import sys

from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.ndfc_python_sender import NdfcPythonSender
from ndfc_python.parsers.parser_ansible_vault import parser_ansible_vault
from ndfc_python.parsers.parser_loglevel import parser_loglevel
from ndfc_python.parsers.parser_nd_domain import parser_nd_domain
from ndfc_python.parsers.parser_nd_ip4 import parser_nd_ip4
from ndfc_python.parsers.parser_nd_password import parser_nd_password
from ndfc_python.parsers.parser_nd_username import parser_nd_username
from ndfc_python.parsers.parser_nxos_password import parser_nxos_password
from ndfc_python.parsers.parser_nxos_username import parser_nxos_username
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results
from plugins.module_utils.image_policy.image_policies import ImagePolicies


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    description = "DESCRIPTION: "
    description += "Query all image policies."
    parser = argparse.ArgumentParser(
        parents=[
            parser_ansible_vault,
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

    image_policies = ImagePolicies()
    image_policies.rest_send = rest_send
    image_policies.results = rest_send.results
    image_policies.results.action = "query_all_image_policies"
    image_policies.results.state = "query"
    image_policies.refresh()
    if len(image_policies.all_policies) > 0:
        image_policies.results.diff_current = image_policies.all_policies
    image_policies.rest_send.results.register_task_result()
    image_policies.rest_send.results.build_final_result()  # type: ignore[attr-defined]
    # pylint: disable=unsupported-membership-test
    if True in image_policies.rest_send.results.failed:  # type: ignore[attr-defined]
        err_msg = "unable to query image policies"
        log.error(err_msg)
        print(err_msg)
    print(json.dumps(image_policies.rest_send.results.final_result, indent=4, sort_keys=True))  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
