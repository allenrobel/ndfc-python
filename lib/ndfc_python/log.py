#!/usr/bin/env python
our_version = 109
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

import os
import logging
import logging.handlers


def Log(_name, _console_level="INFO", _file_level="DEBUG", _capture_warnings=True):
    """
    returns a logger instance i.e. an instance of <class 'logging.Logger'>
    """
    logging.captureWarnings(_capture_warnings)
    logger = Logger()
    logger.logfile = "/tmp/{}.log".format(_name)
    log = logger.new(_name)
    logger.file_loglevel = _file_level
    logger.console_loglevel = _console_level
    return log


class Logger(object):
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
        self.properties = dict()
        self.properties["logfile"] = "/tmp/logger.log"
        self.properties["file_loglevel"] = "DEBUG"
        self.properties["console_loglevel"] = "ERROR"

        self.valid_loglevels = set()
        self.valid_loglevels.add("DEBUG")
        self.valid_loglevels.add("INFO")
        self.valid_loglevels.add("WARNING")
        self.valid_loglevels.add("ERROR")
        self.valid_loglevels.add("CRITICAL")

        self.loglevel_map = dict()
        self.loglevel_map["DEBUG"] = logging.DEBUG
        self.loglevel_map["INFO"] = logging.INFO
        self.loglevel_map["WARNING"] = logging.WARNING
        self.loglevel_map["ERROR"] = logging.ERROR
        self.loglevel_map["CRITICAL"] = logging.CRITICAL

        self.log = None

    def new(self, _name):
        self.log = logging.getLogger(_name)
        self.log.setLevel(logging.DEBUG)
        self.fh = logging.handlers.RotatingFileHandler(
            self.logfile, maxBytes=10000000, backupCount=3
        )
        self.fh.setLevel(self.file_loglevel)

        self.ch = logging.StreamHandler()
        self.ch.setLevel(self.console_loglevel)

        self.formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(relativeCreated)d.%(lineno)d %(module)s.%(funcName)s %(message)s"
        )
        self.ch.setFormatter(self.formatter)
        self.fh.setFormatter(self.formatter)

        self.log.addHandler(self.ch)
        self.log.addHandler(self.fh)
        return self.log

    @property
    def file_loglevel(self):
        return self.properties["file_loglevel"]

    @file_loglevel.setter
    def file_loglevel(self, _x):
        if _x.upper() not in self.valid_loglevels:
            print(
                "exiting. Logger().file_loglevel invalid: {}. Expected one of {}".format(
                    _x, sorted(self.valid_loglevels)
                )
            )
            exit(1)
        if self.log == None:
            print("exiting. Logger().file_loglevel. Call Logger().new() first.")
            exit(1)
        self.properties["file_loglevel"] = self.loglevel_map[_x.upper()]
        self.fh.setLevel(self.properties["file_loglevel"])
        self.log.debug("set file_loglevel to {}".format(_x))

    @property
    def console_loglevel(self):
        return self.properties["console_loglevel"]

    @console_loglevel.setter
    def console_loglevel(self, _x):
        if _x.upper() not in self.valid_loglevels:
            print(
                "exiting. Logger().console_loglevel invalid: {}. Expected one of {}".format(
                    _x, sorted(self.valid_loglevels)
                )
            )
            exit(1)
        if self.log == None:
            print("exiting. Logger().console_loglevel. Call Logger().new() first.")
            exit(1)
        self.properties["console_loglevel"] = self.loglevel_map[_x.upper()]
        self.ch.setLevel(self.properties["console_loglevel"])
        self.log.debug("set console_loglevel to {}".format(_x))

    @property
    def logfile(self):
        return self.properties["logfile"]

    @logfile.setter
    def logfile(self, _x):
        if self.log != None:
            print(
                "Ignoring. Logger().logfile Logger().new() was already called.  Call Logger().logfile() prior to calling Logger().new()"
            )
        self.properties["logfile"] = _x
