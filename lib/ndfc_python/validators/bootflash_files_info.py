from enum import Enum
from ipaddress import IPv4Address
from typing import List

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


class Switch(TypedDict):
    """
    # Summary

    Dictionary containing the following keys

    - ip_address
        - The ipv4 address for a switch
    - targets
        - An optional list of Target()
    """

    ip_address: IPv4Address
    # targets: Optional[List[Target]] = []


class BootflashFilesInfoConfig(BaseModel):
    """
    # Summary

    Base validator for BootflashFilesInfo and ImagePolicyReplace arguments
    """

    targets: List[Target]
    switches: List[Switch]


class BootflashFilesInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a dict containing BootflashFilesInfoConfig
    """

    config: BootflashFilesInfoConfig
