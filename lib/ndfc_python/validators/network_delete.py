from pydantic import BaseModel


class NetworkDeleteConfig(BaseModel):
    """
    # Summary

    Base validator for NetworkDelete arguments
    """

    fabric_name: str
    network_name: str


class NetworkDeleteConfigValidator(BaseModel):
    """
    # Summary

    config is a list of NetworkDeleteConfig
    """

    config: list[NetworkDeleteConfig]
