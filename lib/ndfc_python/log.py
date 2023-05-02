#!/usr/bin/env python
"""
==============
Log() - log.py
==============

Description
-----------
Basic logger for ndfc-python

Synopsis
--------
from ndfc_lib.log import Log

# create a log instance which will log INFO messages to the console and
# DEBUG messages to a rotating logfile /tmp/my_logger_name.log
log = Log('my_logger_name', 'INFO', 'DEBUG')

Notes
-----
1. Valid logging levels: CRITICAL, DEBUG, ERROR, INFO, WARNING
"""
import logging
import logging.handlers
import sys

OUR_VERSION = 112


def log(_name, _console_level="INFO", _file_level="DEBUG", _capture_warnings=True):
    """
    returns a logger instance i.e. an instance of <class 'logging.Logger'>
    """
    logging.captureWarnings(_capture_warnings)
    logger = Logger()
    logger.logfile = f"/tmp/{_name}.log"
    log_obj = logger.new(_name)
    logger.file_loglevel = _file_level
    logger.console_loglevel = _console_level
    return log_obj


class Logger:
    """
    Synopsis
    --------

    ::

    logger = Logger()
    logger.logfile = '/tmp/foobar.log'
    log = logger.new('mylog')
    logger.file_loglevel = 'DEBUG'
    logger.console_loglevel = 'ERROR'
    log.debug('this is a debug log')
    log.error('this is an error log')
    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self._init_properties()
        self._init_valid_loglevels()
        self._init_loglevel_map()

        self._filehandler = None
        self._stream_handler = None
        self.formatter = None
        self.log = None

    def _init_properties(self):
        """
        Initialize all properties
        """
        self.properties = {}
        self.properties["logfile"] = "/tmp/logger.log"
        self.properties["file_loglevel"] = "DEBUG"
        self.properties["console_loglevel"] = "ERROR"

    def _init_valid_loglevels(self):
        """
        Initialize a set containing valid logging level names
        """
        self.valid_loglevels = set()
        self.valid_loglevels.add("DEBUG")
        self.valid_loglevels.add("INFO")
        self.valid_loglevels.add("WARNING")
        self.valid_loglevels.add("ERROR")
        self.valid_loglevels.add("CRITICAL")

    def _init_loglevel_map(self):
        """
        Map log level names to their corresponding logging object properties
        """
        self.loglevel_map = {}
        self.loglevel_map["DEBUG"] = logging.DEBUG
        self.loglevel_map["INFO"] = logging.INFO
        self.loglevel_map["WARNING"] = logging.WARNING
        self.loglevel_map["ERROR"] = logging.ERROR
        self.loglevel_map["CRITICAL"] = logging.CRITICAL

    def new(self, _name):
        """
        Create a new log file
        """
        self.log = logging.getLogger(_name)
        self.log.setLevel(logging.DEBUG)
        self._filehandler = logging.handlers.RotatingFileHandler(
            self.logfile, maxBytes=10000000, backupCount=3
        )
        self._filehandler.setLevel(self.file_loglevel)

        self._stream_handler = logging.StreamHandler()
        self._stream_handler.setLevel(self.console_loglevel)

        format_string = "%(asctime)s %(levelname)s %(relativeCreated)d.%(lineno)d"
        format_string += " %(module)s.%(funcName)s %(message)s"
        self.formatter = logging.Formatter(format_string)
        self._stream_handler.setFormatter(self.formatter)
        self._filehandler.setFormatter(self.formatter)

        self.log.addHandler(self._stream_handler)
        self.log.addHandler(self._filehandler)
        return self.log

    @property
    def console_loglevel(self):
        """
        return the current console logging level
        """
        return self.properties["console_loglevel"]

    @console_loglevel.setter
    def console_loglevel(self, param):
        if param.upper() not in self.valid_loglevels:
            print(f"exiting. Logger().console_loglevel invalid: {param}.")
            print(f" Expected one of {self.valid_loglevels}")
            sys.exit(1)
        if self.log is None:
            print("exiting. Logger().console_loglevel. Call Logger().new() first.")
            sys.exit(1)
        self.properties["console_loglevel"] = self.loglevel_map[param.upper()]
        self._stream_handler.setLevel(self.properties["console_loglevel"])

    @property
    def file_loglevel(self):
        """
        return the current logging level
        """
        return self.properties["file_loglevel"]

    @file_loglevel.setter
    def file_loglevel(self, param):
        if param.upper() not in self.valid_loglevels:
            print(f"Exiting. Logger().file_loglevel invalid: {param}.")
            print(f"Expected one of {sorted(self.valid_loglevels)}")
            sys.exit(1)
        if self.log is None:
            print("exiting. Logger().file_loglevel. Call Logger().new() first.")
            sys.exit(1)
        self.properties["file_loglevel"] = self.loglevel_map[param.upper()]
        self._filehandler.setLevel(self.properties["file_loglevel"])

    @property
    def logfile(self):
        """
        return the current log file
        """
        return self.properties["logfile"]

    @logfile.setter
    def logfile(self, param):
        if self.log is not None:
            print("Ignoring. Logger().logfile Logger().new() was already called.)")
            print("Call Logger().logfile() prior to calling Logger().new(")
        self.properties["logfile"] = param
