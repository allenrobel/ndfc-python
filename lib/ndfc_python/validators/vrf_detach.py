from pydantic import BaseModel, Field, StrictBool


class VrfDetachConfig(BaseModel):
    """Base validator for VrfDetach parameters."""

    deployment: StrictBool = Field(default=True)

    fabric_name: str
    switch_name: str
    vrf_name: str


class VrfDetachConfigValidator(BaseModel):
    """Validator for VRF detach configuration."""

    config: list[VrfDetachConfig]
