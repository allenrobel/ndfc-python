from pydantic import BaseModel


class NetworkInfoConfig(BaseModel):
    """
    # Summary

    Base validator for NetworkInfo arguments
    """

    fabric_name: str
    network_name: str


class NetworkInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of NetworkInfoConfig
    """

    config: list[NetworkInfoConfig]
