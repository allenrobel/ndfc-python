from typing import List

from pydantic import BaseModel


class ImagePolicyDeleteConfig(BaseModel):
    """
    # Summary

    Base validator for ImagePolicyDelete arguments
    """

    name: str


class ImagePolicyDeleteConfigValidator(BaseModel):
    """
    # Summary

    config is a list of ImagePolicyDeleteConfig
    """

    config: List[ImagePolicyDeleteConfig]
