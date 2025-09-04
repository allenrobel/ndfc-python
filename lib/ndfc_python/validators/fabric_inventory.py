from typing import List

from pydantic import BaseModel


class FabricInventoryConfig(BaseModel):
    """
    # Summary

    Base validator for FabricInventory arguments
    """

    fabric_name: str


class FabricInventoryConfigValidator(BaseModel):
    """
    # Summary

    config is a list of VrfCreateConfig
    """

    config: List[FabricInventoryConfig]
