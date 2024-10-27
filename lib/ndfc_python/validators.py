"""
# Summary

Validators for input class properties.
"""

from typing import Optional

from pydantic import BaseModel, IPvAnyInterface, PositiveInt


class FabricDetailsConfig(BaseModel):
    """
    # Summary

    Base validator for FabricDetails arguments
    """

    fabric_name: str


class NetworkCreateConfig(BaseModel):
    """
    # Summary

    Base validator for NetworkCreate arguments
    """

    fabric_name: str
    gateway_ip_address: Optional[IPvAnyInterface] = None
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


class FabricDetailsConfigValidator(BaseModel):
    """
    # Summary

    Wrap base validator in a dict
    """

    config: FabricDetailsConfig


class NetworkCreateConfigValidator(BaseModel):
    """
    # Summary

    Wrap base validator in a dict
    """

    config: NetworkCreateConfig


class NetworkDeleteConfigValidator(BaseModel):
    """
    # Summary

    Wrap base validator in a dict
    """

    config: NetworkDeleteConfig
