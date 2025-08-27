from pydantic import field_validator, field_serializer, BaseModel, Field, PositiveInt, StrictBool

from ..common.models.ipv4_cidr_host import IPv4CidrHostModel
from ..common.models.ipv4_host import IPv4HostModel
from ..common.models.ipv6_host import IPv6HostModel
from ..common.models.ipv6_cidr_host import IPv6CidrHostModel


class ExtensionValues(BaseModel):
    """Model for extension values in VRF attach requests."""

    AUTO_VRF_LITE_FLAG: StrictBool = Field(alias="auto_vrf_lite_flag", default=True)
    DOT1Q_ID: int | str = Field(alias="dot1q_id", default="")
    IF_NAME: str = Field(alias="if_name", default="")
    IP_MASK: str | int = Field(alias="ip_mask", default="")
    IPV6_MASK: str | int = Field(alias="ipv6_mask", default="")
    IPV6_NEIGHBOR: str = Field(alias="ipv6_neighbor", default="")
    NEIGHBOR_ASN: str = Field(alias="neighbor_asn", default="")
    NEIGHBOR_IP: str = Field(alias="neighbor_ip", default="")
    PEER_VRF_NAME: str = Field(alias="peer_vrf_name", default="")
    VRF_LITE_JYTHON_TEMPLATE: str = Field(alias="vrf_lite_jython_template", default="Ext_VRF_Lite_Jython")

    @field_validator("IP_MASK", mode="before")
    @classmethod
    def validate_ip_mask(cls, value: str) -> str:
        """
        Validate IP_MASK to ensure it is a valid IPv4 CIDR host address.
        """
        if value == "":
            return value
        try:
            return IPv4CidrHostModel(ipv4_cidr_host=value).ipv4_cidr_host
        except ValueError as error:
            msg = f"Invalid IP_MASK: {value}. detail: {error}"
            raise ValueError(msg) from error

    @field_validator("IPV6_MASK", mode="before")
    @classmethod
    def validate_ipv6_mask(cls, value: str) -> str:
        """
        Validate IPV6_MASK to ensure it is a valid IPv6 CIDR host address.
        """
        if value == "":
            return value
        try:
            return IPv6CidrHostModel(ipv6_cidr_host=value).ipv6_cidr_host
        except ValueError as error:
            msg = f"Invalid IPV6_MASK: {value}. detail: {error}"
            raise ValueError(msg) from error

    @field_validator("IPV6_NEIGHBOR", mode="before")
    @classmethod
    def validate_ipv6_neighbor(cls, value: str) -> str:
        """
        Validate IPV6_NEIGHBOR to ensure it is a valid IPv6 host address.
        """
        if value == "":
            return value
        try:
            return IPv6HostModel(ipv6_host=value).ipv6_host
        except ValueError as error:
            msg = f"Invalid IPV6_NEIGHBOR: {value}. detail: {error}"
            raise ValueError(msg) from error

    @field_validator("NEIGHBOR_IP", mode="before")
    @classmethod
    def validate_neighbor_ip(cls, value: str) -> str:
        """
        Validate NEIGHBOR_IP to ensure it is a valid IPv4 host address without prefix length.
        """
        if value == "":
            return value
        try:
            return IPv4HostModel(ipv4_host=value).ipv4_host
        except ValueError as error:
            msg = f"Invalid neighbor IP address (NEIGHBOR_IP): {value}. detail: {error}"
            raise ValueError(msg) from error

    @field_serializer("AUTO_VRF_LITE_FLAG")
    def serialize_auto_vrf_lite_flag(self, value) -> str:
        """
        Serialize AUTO_VRF_LITE_FLAG to a string representation.
        """
        return str(value).lower()

class InstanceValues(BaseModel):
    """Model for instance values in VRF attach requests."""

    loopbackId: int | str = Field(alias="loopback_id", default="")
    loopbackIpAddress: str = Field(alias="loopback_ip_address", default="")
    loopbackIpV6Address: str = Field(alias="loopback_ip_v6_address", default="")
    switchRouteTargetImportEvpn: str = Field(alias="switch_route_target_import_evpn", default="")
    switchRouteTargetExportEvpn: str = Field(alias="switch_route_target_export_evpn", default="")


class VrfAttachConfig(BaseModel):
    """Base validator for VrfAttach parameters."""

    deployment: StrictBool = Field(default=True)

    extensionValues: ExtensionValues = Field(alias="extension_values", default="")
    fabric: str = Field(..., alias="fabric_name")
    freeformConfig: list[str] = Field(alias="freeform_config", default=[])
    instanceValues: InstanceValues = Field(alias="instance_values", default=InstanceValues().model_dump())
    serialNumber: str = Field(..., alias="serial_number")
    vlan: PositiveInt | str = Field(default="")
    vrfName: str = Field(..., alias="vrf_name")


class VrfAttachConfigValidator(BaseModel):
    """Validator for VRF attach configuration."""

    config: list[VrfAttachConfig]
