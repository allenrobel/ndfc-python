from pydantic import BaseModel


class DeviceInfoConfig(BaseModel):
    """
    # Summary

    Base validator for DeviceInfo arguments
    """

    fabric_name: str
    switch_name: str


class DeviceInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of DeviceInfoConfig
    """

    config: list[DeviceInfoConfig]
