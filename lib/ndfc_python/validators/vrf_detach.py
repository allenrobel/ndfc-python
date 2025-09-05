from pydantic import BaseModel, Field, StrictBool


class VrfDetachConfig(BaseModel):
    """Base validator for VrfDetach parameters."""

    deployment: StrictBool = Field(default=True)

    fabric: str = Field(..., alias="fabric_name")
    switch_name: str
    vrfName: str = Field(..., alias="vrf_name")


class VrfDetachConfigValidator(BaseModel):
    """Validator for VRF detach configuration."""

    config: list[VrfDetachConfig]
