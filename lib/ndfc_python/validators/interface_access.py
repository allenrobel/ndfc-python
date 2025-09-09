from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class InterfaceAccessCreateConfig(BaseModel):
    """
    # Summary

    Base validator for InterfaceAccessCreate arguments
    """

    access_vlan: Optional[PositiveInt | str] = Field(default="")
    admin_state: Optional[bool] = Field(default=True)
    bpduguard_enabled: Optional[bool] = Field(default=True)
    conf: Optional[str] = Field(alias="freeform_config", default="")
    desc: Optional[str] = Field(default="")
    enable_netflow: Optional[bool] = Field(default=False)
    fabric_name: str = Field(...)
    intf_name: str = Field(..., alias="interface_name")
    mtu: Optional[PositiveInt | str] = Field(default="jumbo")
    netflow_monitor: Optional[str] = Field(default="")
    porttype_fast_enabled: Optional[bool] = Field(default=True)
    ptp: Optional[bool] = Field(default=False)
    speed: Optional[PositiveInt | str] = Field(default="Auto")
    switch_name: str = Field(...)


class InterfaceAccessCreateConfigValidator(BaseModel):
    """
    # Summary

    config is a list of InterfaceAccessCreateConfig
    """

    config: list[InterfaceAccessCreateConfig]
