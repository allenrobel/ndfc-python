from typing import Optional

from pydantic import BaseModel
from typing_extensions import TypedDict


class ImagePolicyPackages(TypedDict):
    """
    # Summary

    Dictionary containing the following keys

    - install
        - list of packages to install
    - uninstall
        - list of packages to uninstall
    """

    install: Optional[list[str]]
    uninstall: Optional[list[str]]


class ImagePolicyCreateConfig(BaseModel):
    """
    # Summary

    Base validator for ImagePolicyCreate and ImagePolicyReplace arguments
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

    config: list[ImagePolicyCreateConfig]
