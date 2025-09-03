from pydantic import BaseModel, Field, StrictBool


class VrfDetachConfig(BaseModel):
    """Base validator for VrfDetach parameters."""

    deployment: StrictBool = Field(default=True)

    fabric: str = Field(..., alias="fabric_name")
    serialNumber: str = Field(..., alias="serial_number")
    vrfName: str = Field(..., alias="vrf_name")


class VrfDetachConfigValidator(BaseModel):
    """Validator for VRF detach configuration."""

    config: list[VrfDetachConfig]
