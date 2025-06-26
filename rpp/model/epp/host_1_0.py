from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from rpp.model.epp.epp_1_0 import TrIdtype
from rpp.model.epp.eppcom_1_0 import ReasonType

__NAMESPACE__ = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class CheckNameType:
    class Meta:
        name = "checkNameType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    avail: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ChgType:
    class Meta:
        name = "chgType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )


@dataclass
class CreDataType:
    class Meta:
        name = "creDataType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    cr_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "crDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
        },
    )


class IpType(Enum):
    V4 = "v4"
    V6 = "v6"


@dataclass
class MNameType:
    class Meta:
        name = "mNameType"

    name: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "min_occurs": 1,
            "min_length": 1,
            "max_length": 255,
        },
    )


@dataclass
class PaNameType:
    class Meta:
        name = "paNameType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    pa_result: Optional[bool] = field(
        default=None,
        metadata={
            "name": "paResult",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SNameType:
    class Meta:
        name = "sNameType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )


class StatusValueType(Enum):
    CLIENT_DELETE_PROHIBITED = "clientDeleteProhibited"
    CLIENT_UPDATE_PROHIBITED = "clientUpdateProhibited"
    LINKED = "linked"
    OK = "ok"
    PENDING_CREATE = "pendingCreate"
    PENDING_DELETE = "pendingDelete"
    PENDING_TRANSFER = "pendingTransfer"
    PENDING_UPDATE = "pendingUpdate"
    SERVER_DELETE_PROHIBITED = "serverDeleteProhibited"
    SERVER_UPDATE_PROHIBITED = "serverUpdateProhibited"


@dataclass
class AddrType:
    class Meta:
        name = "addrType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 3,
            "max_length": 45,
        },
    )
    ip: IpType = field(
        default=IpType.V4,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Check(MNameType):
    class Meta:
        name = "check"
        namespace = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class CheckType:
    class Meta:
        name = "checkType"

    name: Optional[CheckNameType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
        },
    )
    reason: Optional[ReasonType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )


@dataclass
class CreData(CreDataType):
    class Meta:
        name = "creData"
        namespace = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class Delete(SNameType):
    class Meta:
        name = "delete"
        namespace = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class Info(SNameType):
    class Meta:
        name = "info"
        namespace = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class PanDataType:
    class Meta:
        name = "panDataType"

    name: Optional[PaNameType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
        },
    )
    pa_trid: Optional[TrIdtype] = field(
        default=None,
        metadata={
            "name": "paTRID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
        },
    )
    pa_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "paDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
        },
    )


@dataclass
class StatusType:
    class Meta:
        name = "statusType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    s: Optional[StatusValueType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    lang: str = field(
        default="en",
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class AddRemType:
    class Meta:
        name = "addRemType"

    addr: list[AddrType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )
    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "max_occurs": 7,
        },
    )


@dataclass
class ChkDataType:
    class Meta:
        name = "chkDataType"

    cd: list[CheckType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class CreateType:
    class Meta:
        name = "createType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    addr: list[AddrType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )


@dataclass
class InfDataType:
    class Meta:
        name = "infDataType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    roid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "pattern": r"(\w|_){1,80}-\w{1,8}",
        },
    )
    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "min_occurs": 1,
            "max_occurs": 7,
        },
    )
    addr: list[AddrType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )
    cl_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "clID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    cr_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "crID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    cr_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "crDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
        },
    )
    up_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "upID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "min_length": 3,
            "max_length": 16,
        },
    )
    up_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "upDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )
    tr_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "trDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )


@dataclass
class PanData(PanDataType):
    class Meta:
        name = "panData"
        namespace = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class ChkData(ChkDataType):
    class Meta:
        name = "chkData"
        namespace = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class Create(CreateType):
    class Meta:
        name = "create"
        namespace = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class InfData(InfDataType):
    class Meta:
        name = "infData"
        namespace = "urn:ietf:params:xml:ns:host-1.0"


@dataclass
class UpdateType:
    class Meta:
        name = "updateType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    add: Optional[AddRemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )
    rem: Optional[AddRemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )
    chg: Optional[ChgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:host-1.0",
        },
    )


@dataclass
class Update(UpdateType):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:host-1.0"
