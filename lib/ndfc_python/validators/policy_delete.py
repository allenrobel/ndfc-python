from pydantic import BaseModel, Field


class PolicyDeleteConfig(BaseModel):
    """
    # Summary

    Base validator for PolicyDelete arguments
    """

    description: str = Field(description="Mandatory description of the policy.  Description MUST be unique.")
    fabric_name: str = Field(description="Required to retrieve switch information.  Not used in payload.")
    switch_name: str = Field(description="Name of the switch from which to delete the policy.")


class PolicyDeleteConfigValidator(BaseModel):
    """
    # Summary

    config is a list of PolicyDeleteConfig
    """

    config: list[PolicyDeleteConfig]
