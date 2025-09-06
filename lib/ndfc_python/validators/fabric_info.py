from pydantic import BaseModel, Field


class FabricInfoConfig(BaseModel):
    """
    # Summary

    Base validator for FabricInfo arguments
    """

    fabric_name: str = Field(..., min_length=1, max_length=64, description="Name of the fabric")


class FabricInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of FabricInfoConfig
    """

    config: list[FabricInfoConfig]
