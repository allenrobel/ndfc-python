#!/usr/bin/env python

import argparse
import json
import logging
import sys

from ndfc_python.image_policy import Query
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
from plugins.module_utils.common.response_handler import ResponseHandler
from plugins.module_utils.common.rest_send_v2 import RestSend
from pydantic import ValidationError


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
        validated_config = ImagePolicyInfoConfigValidator(**ndfc_config.contents)
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
    params["state"] = "query"
    params["config"] = json.loads(validated_config.model_dump_json())

    rest_send = RestSend({})
    rest_send.sender = ndfc_sender.sender
    rest_send.response_handler = ResponseHandler()

    try:
        task = Query(params)
        task.rest_send = rest_send
        task.commit()
    except ValueError as error:
        err_msg = f"Exiting.  Error detail: {error}"
        log.error(err_msg)
        print(err_msg)
        sys.exit(1)

    task.results.build_final_result()
    # pylint: disable=unsupported-membership-test
    if True in task.results.failed:
        err_msg = "unable to query image policies"
        log.error(err_msg)
        print(err_msg)
    print(json.dumps(task.results.final_result, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
