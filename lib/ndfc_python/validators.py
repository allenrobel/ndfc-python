from typing import Optional, TypedDict

from pydantic import BaseModel, IPvAnyInterface, PositiveInt


class NetworkCreateConfig(BaseModel):
    fabric_name: str
    network_id: PositiveInt
    network_name: str
    vlan_id: PositiveInt
    vrf_name: str
    gateway_ip_address: Optional[IPvAnyInterface] = None
    layer2_only: Optional[bool] = None


class NetworkDeleteConfig(TypedDict):
    fabric_name: str
    network_name: str


class NetworkCreateConfigValidator(BaseModel):
    config: NetworkCreateConfig


class NetworkDeleteConfigValidator(BaseModel):
    config: NetworkDeleteConfig
