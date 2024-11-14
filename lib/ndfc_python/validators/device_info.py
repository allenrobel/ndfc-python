from ipaddress import IPv4Address
from typing import List

from pydantic import BaseModel


class DeviceInfoConfig(BaseModel):
    """
    # Summary

    Base validator for DeviceInfo arguments
    """

    switch_ip4: IPv4Address


class DeviceInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of DeviceInfoConfig
    """

    config: List[DeviceInfoConfig]
