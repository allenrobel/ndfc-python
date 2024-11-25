from typing import List

from pydantic import BaseModel


class VrfDeleteConfig(BaseModel):
    """
    # Summary

    Base validator for VrfDelete arguments
    """

    fabric_name: str
    vrf_names: List[str]


class VrfDeleteConfigValidator(BaseModel):
    """
    # Summary

    config is a list of VrfDeleteConfig
    """

    config: List[VrfDeleteConfig]
