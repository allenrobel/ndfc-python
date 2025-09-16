from pydantic import BaseModel, Field


class FabricsInfoConfig(BaseModel):
    """
    # Summary

    Base validator for FabricsInfo arguments
    """

    filter: str = Field(default="", min_length=0, max_length=64, description="Name of the fabric to filter on. Empty string means all fabrics.")


class FabricsInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of FabricsInfoConfig
    """

    config: list[FabricsInfoConfig]
