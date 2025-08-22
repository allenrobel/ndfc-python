from pydantic import BaseModel, Field, PositiveInt, StrictBool


class InstanceValues(BaseModel):
    """Model for instance values in VRF attach requests."""

    loopbackId: int | str = Field(alias="loopback_id", default="")
    loopbackIpAddress: str = Field(alias="loopback_ip_address", default="")
    loopbackIpV6Address: str = Field(alias="loopback_ip_v6_address", default="")
    switchRouteTargetImportEvpn: str = Field(alias="switch_route_target_import_evpn", default="")
    switchRouteTargetExportEvpn: str = Field(alias="switch_route_target_export_evpn", default="")


class VrfAttachConfig(BaseModel):
    """Base validator for VrfAttach parameters."""

    deployment: StrictBool = Field(default=True)
    extensionValues: str = Field(alias="extension_values", default="")
    fabric: str = Field(..., alias="fabric_name")
    freeformConfig: list[str] = Field(alias="freeform_config", default=[])
    instanceValues: InstanceValues = Field(alias="instance_values", default=InstanceValues().model_dump())
    msoCreated: StrictBool = Field(alias="mso_created", default=False)
    msoSetVlan: StrictBool = Field(alias="mso_set_vlan", default=False)
    serialNumber: str = Field(..., alias="serial_number")
    vlan: PositiveInt | str = Field(default="")
    vrfName: str = Field(..., alias="vrf_name")


class VrfAttachConfigValidator(BaseModel):
    """Validator for VRF attach configuration."""

    config: list[VrfAttachConfig]
