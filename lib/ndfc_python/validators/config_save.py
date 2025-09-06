from pydantic import BaseModel, Field


class ConfigSaveConfig(BaseModel):
    """
    # Summary

    Base validator for ConfigSave arguments
    """

    fabric_name: str = Field(..., min_length=1, max_length=64, description="Name of the fabric")


class ConfigSaveConfigValidator(BaseModel):
    """
    # Summary

    config is a list of ConfigSaveConfig
    """

    config: list[ConfigSaveConfig]
