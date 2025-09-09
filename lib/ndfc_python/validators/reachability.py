from ipaddress import IPv4Address

from pydantic import BaseModel


class ReachabilityConfig(BaseModel):
    """
    # Summary

    Base validator for Reachability arguments
    """

    fabric_name: str
    seed_ip: IPv4Address


class ReachabilityConfigValidator(BaseModel):
    """
    # Summary

    config is a list of ReachabilityConfig
    """

    config: list[ReachabilityConfig]
