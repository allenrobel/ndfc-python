from pydantic import BaseModel, Field


class PolicyCreateConfig(BaseModel):
    """
    # Summary

    Base validator for PolicyCreate arguments
    """

    description: str = Field(description="Mandatory description of the policy.  Description MUST be unique.")
    entityName: str = Field(alias="entity_name")
    entityType: str = Field(alias="entity_type")
    fabric_name: str = Field(description="Required to retrieve switch information.  Not used in payload.")
    nvPairs: dict = Field(alias="nv_pairs", default={}, description="Policy-specific key-value pairs.")
    priority: int = Field(default=200)
    source: str = Field(default="")
    switchName: str = Field(alias="switch_name")
    templateName: str = Field(alias="template_name", default="")
    templateContentType: str = Field(alias="template_content_type", default="string")


class PolicyCreateConfigValidator(BaseModel):
    """
    # Summary

    config is a list of PolicyCreateConfig
    """

    config: list[PolicyCreateConfig]
