from pydantic import BaseModel, Field


class ConfigDeployConfig(BaseModel):
    """
    # Summary

    Base validator for ConfigDeploy arguments
    """

    fabric_name: str = Field(..., min_length=1, max_length=64, description="Name of the fabric")


class ConfigDeployConfigValidator(BaseModel):
    """
    # Summary

    config is a list of ConfigDeployConfig
    """

    config: list[ConfigDeployConfig]
