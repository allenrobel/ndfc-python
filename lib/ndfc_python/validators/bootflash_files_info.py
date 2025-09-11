from enum import Enum

from pydantic import BaseModel
from typing_extensions import TypedDict


class SupervisorEnum(str, Enum):
    """
    # Summary

    Choices for Target.supervisor
    """

    active = "active"
    standby = "standby"


class Target(BaseModel):
    """
    # Summary

    Dictionary containing the following keys

    - filepath
        - A filepath specification, for example "/*.txt"
    - supervisor
        - The supervisor module containing the filepath
            - choices
                - active
                - standby
    """

    filepath: str
    supervisor: SupervisorEnum


class SwitchSpec(TypedDict):
    """
    # Summary

    Dictionary containing the following keys

    - fabric_name
        - The switch's hosting fabric_name
    - switch_name
        - The name of the switch
    """

    fabric_name: str
    switch_name: str


class BootflashFilesInfoConfigValidator(BaseModel):
    """
    # Summary

    Base validator for BootflashFilesInfo and ImagePolicyReplace arguments
    """

    targets: list[Target]
    switches: list[SwitchSpec]
