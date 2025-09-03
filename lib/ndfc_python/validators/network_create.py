from ipaddress import IPv4Interface
from typing import List, Optional

from pydantic import BaseModel, PositiveInt


class NetworkCreateConfig(BaseModel):
    """
    # Summary

    Base validator for NetworkCreate arguments
    """

    fabric_name: str
    gateway_ip_address: Optional[IPv4Interface] = None
    is_layer2_only: Optional[bool] = False
    network_id: PositiveInt
    network_name: str
    suppress_arp: Optional[bool] = True
    vlan_id: PositiveInt
    vrf_name: str


class NetworkCreateConfigValidator(BaseModel):
    """
    # Summary

    config is a list of NetworkCreateConfig
    """

    config: List[NetworkCreateConfig]
