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

    pool_name: ResourcePool = Field(default=ResourcePool.ALL, description="Optional Resource Pool Name")
    serial_number: str = Field(..., description="Switch Serial Number")


class RmSwitchResourceUsageConfigValidator(BaseModel):
    """Validator for Resource Manager Switch Resource Usage."""

    config: list[RmSwitchResourceUsageConfig]
