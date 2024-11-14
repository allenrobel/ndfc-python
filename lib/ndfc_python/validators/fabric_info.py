from typing import List

from pydantic import BaseModel


class FabricInfoConfig(BaseModel):
    """
    # Summary

    Base validator for FabricInfo arguments
    """

    fabric_name: str


class FabricInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of FabricInfoConfig
    """

    config: List[FabricInfoConfig]
