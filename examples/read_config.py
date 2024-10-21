#!/usr/bin/env python

import argparse
import logging
import sys

from ndfc_python.ndfc_python_config import NdfcPythonConfig
from ndfc_python.ndfc_python_logger import NdfcPythonLogger
from ndfc_python.parsers.parser_config import parser_config
from ndfc_python.parsers.parser_loglevel import parser_loglevel


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        parents=[parser_config, parser_loglevel],
        description='DESCRIPTION: read YAML configuration files.')
    return parser.parse_args()

args = setup_parser()

NdfcPythonLogger()
log = logging.getLogger("ndfc_python.main")
log.setLevel = args.loglevel

try:
    ndfc_config = NdfcPythonConfig()
    ndfc_config.filename = args.config
    ndfc_config.commit()
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    sys.exit()

contents = ndfc_config.contents
print(f"contents: {contents}")
config = contents.get("config", {})
for option in config:
    print(f"option: {option} = {config[option]}")
