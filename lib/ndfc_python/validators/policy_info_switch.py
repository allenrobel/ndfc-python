from pydantic import BaseModel


class PolicyInfoSwitchConfig(BaseModel):
    """
    # Summary

    Base validator for PolicyInfoSwitch arguments
    """

    fabric_name: str
    switch_name: str


class PolicyInfoSwitchConfigValidator(BaseModel):
    """
    # Summary

    config is a list of PolicyInfoSwitchConfig
    """

    config: list[PolicyInfoSwitchConfig]
