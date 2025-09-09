from enum import Enum
from ipaddress import IPv4Address
from typing import Optional

from pydantic import BaseModel


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


class MaintenanceModeConfigValidator(BaseModel):
    """
    # Summary

    config is a list of MaintenanceModeConfig
    """

    config: list[MaintenanceModeConfig]


class MaintenanceModeInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of MaintenanceModeInfoConfig
    """

    config: list[MaintenanceModeInfoConfig]
