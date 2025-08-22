from typing import List
from pydantic import BaseModel, Field, ConfigDict

class NvPairs(BaseModel):
    INTF_NAME: str
    SERIAL_NUMBER: str
    BPDUGUARD_ENABLED: str
    PORTTYPE_FAST_ENABLED: str
    MTU: str
    SPEED: str
    ACCESS_VLAN: str
    DESC: str
    CONF: str
    ADMIN_STATE: str
    PTP: str
    ENABLE_NETFLOW: str
    NETFLOW_MONITOR: str

class Interface(BaseModel):
    serialNumber: str = Field(..., alias="serialNumber")
    ifName: str = Field(..., alias="ifName")
    nvPairs: NvPairs

class InterfaceAccessModePayload(BaseModel):
    policy: str
    interfaceType: str
    interfaces: List[Interface]

    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True
    )
