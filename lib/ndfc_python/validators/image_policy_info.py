from typing import List

from pydantic import BaseModel


class ImagePolicyInfoConfig(BaseModel):
    """
    # Summary

    Base validator for ImagePolicyInfo arguments
    """

    name: str


class ImagePolicyInfoConfigValidator(BaseModel):
    """
    # Summary

    config is a list of ImagePolicyInfoConfig
    """

    config: List[ImagePolicyInfoConfig]
