from pydantic import BaseModel, Field, PositiveInt


class NetworkDetachConfig(BaseModel):
    """
    # Summary

    Base validator for NetworkDetach arguments
    """

    detachSwitchPorts: list[str] = Field(alias="detach_switch_ports", default=[])
    dot1QVlan: PositiveInt | str = Field(alias="dot1q_vlan", default="")
    fabric: str = Field(..., alias="fabric_name")
    networkName: str = Field(..., alias="network_name")
    peer_switch_name: str = Field(default="")
    switch_name: str
    vlan: PositiveInt | str = Field(default="")


class NetworkDetachConfigValidator(BaseModel):
    """
    # Summary

    config is a list of NetworkDetachConfig
    """

    config: list[NetworkDetachConfig]
