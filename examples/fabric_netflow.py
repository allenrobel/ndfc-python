#!/usr/bin/env python3
"""
Name: fabric_netflow.py
Description: Create a fabric with netflow configured
"""
from ndfc_python.log import log
from ndfc_python.ndfc import NDFC
from ndfc_python.ndfc_credentials import NdfcCredentials
from ndfc_python.ndfc_easy_fabric import NdfcEasyFabric

nc = NdfcCredentials()

logger = log("fabric_netflow_log", "INFO", "DEBUG")

ndfc = NDFC()
ndfc.username = nc.username
ndfc.password = nc.password
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = logger
ndfc.login()

exporter_dict = {}
exporter_dict["EXPORTER_NAME"] = "exporter1"
exporter_dict["IP"] = "172.22.150.103"
exporter_dict["VRF"] = "default"
exporter_dict["SRC_IF_NAME"] = "Loopback0"
exporter_dict["UDP_PORT"] = 6500
exporter_list = []
exporter_list.append(exporter_dict)

record_dict = {}
record_dict["RECORD_NAME"] = "ipv4-record"
record_dict["RECORD_TEMPLATE"] = "netflow_ipv4_record"
record_dict["LAYER2_RECORD"] = False
record_list = []
record_list.append(record_dict)

monitor_dict = {}
monitor_dict["MONITOR_NAME"] = "netflow-monitor"
monitor_dict["RECORD_NAME"] = "ipv4-record"
monitor_dict["EXPORTER1"] = "exporter1"
monitor_list = []
monitor_list.append(monitor_dict)

instance = NdfcEasyFabric()
instance.ndfc = ndfc
instance.logger = logger
instance.fabric_name = "easy_netflow"
instance.bgp_as = 65001
instance.dci_subnet_range = "10.25.0.0/16"
instance.loopback0_ip_range = "10.26.0.0/16"
instance.loopback1_ip_range = "10.27.0.0/16"
instance.enable_netflow = True
instance.netflow_exporter_list = exporter_list
instance.netflow_record_list = record_list
instance.netflow_monitor_list = monitor_list
instance.create()
