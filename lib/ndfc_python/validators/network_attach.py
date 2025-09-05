from pydantic import BaseModel, Field, PositiveInt, StrictBool


class NetworkAttachConfig(BaseModel):
    """
    # Summary

    Base validator for NetworkAttach arguments
    """

    detachSwitchPorts: list[str] = Field(alias="detach_switch_ports", default=[])
    dot1QVlan: PositiveInt | str = Field(alias="dot1q_vlan", default="")
    extensionValues: str = Field(alias="extension_values", default="")
    fabric: str = Field(..., alias="fabric_name")
    freeformConfig: list[str] = Field(alias="freeform_config", default=[])
    instanceValues: str = Field(alias="instance_values", default="")
    networkName: str = Field(..., alias="network_name")
    peer_switch_name: str = Field(default="")
    switch_name: str
    switchPorts: list[str] = Field(alias="switch_ports", default=[])
    torPorts: list[str] = Field(alias="tor_ports", default=[])
    untagged: StrictBool = Field(default=True)
    vlan: PositiveInt | str = Field(default="")


class NetworkAttachConfigValidator(BaseModel):
    """
    # Summary

    config is a list of NetworkAttachConfig
    """

    config: list[NetworkAttachConfig]
