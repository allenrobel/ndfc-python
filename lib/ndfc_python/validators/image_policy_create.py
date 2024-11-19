from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import TypedDict


class ImagePolicyPackages(TypedDict):
    """
    # Summary

    Dictionary containing the following keys

    - install
        - List of packages to install
    - uninstall
        - List of packages to uninstall
    """

    install: Optional[List[str]]
    uninstall: Optional[List[str]]


class ImagePolicyCreateConfig(BaseModel):
    """
    # Summary

    Base validator for ImagePolicyCreate arguments
    """

    name: str
    agnostic: bool = False
    description: str = ""
    epld_image: str = ""
    packages: Optional[ImagePolicyPackages] = {}
    platform: str
    release: str
    type: Optional[str] = "PLATFORM"


class ImagePolicyCreateConfigValidator(BaseModel):
    """
    # Summary

    config is a list of ImagePolicyCreateConfig
    """

    config: List[ImagePolicyCreateConfig]
