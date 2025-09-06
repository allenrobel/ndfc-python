from pydantic import BaseModel, Field


class FabricInventoryConfig(BaseModel):
    """
    # Summary

    Base validator for FabricInventory arguments
    """

    fabric_name: str = Field(..., min_length=1, max_length=64, description="Name of the fabric")


class FabricInventoryConfigValidator(BaseModel):
    """
    # Summary

    config is a list of FabricInventoryConfig
    """

    config: list[FabricInventoryConfig]
