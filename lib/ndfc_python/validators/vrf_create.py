from typing import List

from pydantic import BaseModel


class VrfCreateConfig(BaseModel):
    """
    # Summary

    Base validator for VrfCreate arguments
    """

    fabric_name: str
    vrf_display_name: str
    vrf_id: int
    vrf_name: str
    vrf_vlan_id: int


class VrfCreateConfigValidator(BaseModel):
    """
    # Summary

    config is a list of VrfCreateConfig
    """

    config: List[VrfCreateConfig]
