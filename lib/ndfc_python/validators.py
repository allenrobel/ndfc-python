"""
# Summary

Validators for class input properties.
"""

from enum import Enum
from ipaddress import IPv4Address, IPv4Interface
from typing import List, Optional

from pydantic import BaseModel, PositiveInt


class DeviceInfoConfig(BaseModel):
    """
    # Summary

    Base validator for DeviceInfo arguments
    """

    switch_ip4: IPv4Address


class FabricDetailsConfig(BaseModel):
    """
    # Summary

    Base validator for FabricDetails arguments
    """

    fabric_name: str


class MaintenanceModeConfig(BaseModel):
    """
    # Summary

    Base validator for MaintenanceMode arguments
    """

    class ModeEnum(str, Enum):
        """
        # Summary

        Enum for MaintenanceModeConfig.mode
        """

        maintenance = "maintenance"
        normal = "normal"

    ip_address: IPv4Address
    deploy: Optional[bool] = True
    wait_for_mode_change: Optional[bool] = True
    mode: ModeEnum


class MaintenanceModeInfoConfig(BaseModel):
    """
    # Summary

    Base validator for MaintenanceModeInfo arguments
    """

    ip_address: IPv4Address


class NetworkCreateConfig(BaseModel):
    """
    # Summary

    Base validator for NetworkCreate arguments
    """

    fabric_name: str
    gateway_ip_address: Optional[IPv4Interface] = None
    is_layer2_only: Optional[bool] = None
    network_id: PositiveInt
    network_name: str
    vlan_id: PositiveInt
    vrf_name: str


class NetworkDeleteConfig(BaseModel):
    """
    # Summary

    Base validator for NetworkDelete arguments
    """

    fabric_name: str
    network_name: str


class ReachabilityConfig(BaseModel):
    """
    # Summary

    Base validator for Reachability arguments
    """

    fabric_name: str
    seed_ip: IPv4Address


class VrfCreateConfig(BaseModel):
    """
    # Summary

    Base validator for VrfCreate arguments
    """

    fabric_name: str
    vrf_display_name: str
    vrf_id: int
    vrf_name: str
    vrf_vlan_id: int


class DeviceInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of DeviceInfoConfig
    """

    config: List[DeviceInfoConfig]


class FabricDetailsConfigValidator(BaseModel):
    """
    # Summary

    config is a list of FabricDetailsConfig
    """

    config: List[FabricDetailsConfig]


class MaintenanceModeConfigValidator(BaseModel):
    """
    # Summary

    config is a list of MaintenanceModeConfig
    """

    config: List[MaintenanceModeConfig]


class MaintenanceModeInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of MaintenanceModeInfoConfig
    """

    config: List[MaintenanceModeInfoConfig]


class NetworkCreateConfigValidator(BaseModel):
    """
    # Summary

    config is a list of NetworkCreateConfig
    """

    config: List[NetworkCreateConfig]


class NetworkDeleteConfigValidator(BaseModel):
    """
    # Summary

    config is a list of NetworkDeleteConfig
    """

    config: List[NetworkDeleteConfig]


class ReachabilityConfigValidator(BaseModel):
    """
    # Summary

    config is a list of ReachabilityConfig
    """

    config: List[ReachabilityConfig]


class VrfCreateConfigValidator(BaseModel):
    """
    # Summary

    config is a list of VrfCreateConfig
    """

    config: List[VrfCreateConfig]
