from enum import Enum

from pydantic import BaseModel, Field


class ResourcePool(Enum):
    """Resource Pools Values"""

    ALL = "ALL"
    DISCOVERED_VLAN = "DISCOVERED_VLAN"
    SERVICE_NETWORK_VLAN = "SERVICE_NETWORK_VLAN"
    TOP_DOWN_VRF_VLAN = "TOP_DOWN_VRF_VLAN"
    TOP_DOWN_NETWORK_VLAN = "TOP_DOWN_NETWORK_VLAN"
    VPC_PEER_LINK_VLAN = "VPC_PEER_LINK_VLAN"


class RmSwitchResourceUsageConfig(BaseModel):
    """Base validator for Resource Manager Switch Resource Usage parameters."""

    fabric_name: str = Field(..., description="Fabric Name")
    pool_name: ResourcePool = Field(default=ResourcePool.ALL, description="Optional Resource Pool Name")
    switch_name: str = Field(..., description="Switch Name")


class RmSwitchResourceUsageConfigValidator(BaseModel):
    """Validator for Resource Manager Switch Resource Usage."""

    config: list[RmSwitchResourceUsageConfig]
