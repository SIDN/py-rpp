from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDateTime

from rpp.model.epp.epp_1_0 import TrIdtype
from rpp.model.epp.eppcom_1_0 import (
    ExtAuthInfoType,
    PwAuthInfoType,
    ReasonType,
    TrStatusType,
)

__NAMESPACE__ = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class AddrType:
    class Meta:
        name = "addrType"

    street: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_occurs": 3,
            "max_length": 255,
        },
    )
    city: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    sp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_length": 255,
        },
    )
    pc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_length": 16,
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "length": 2,
        },
    )


@dataclass
class CheckIdtype:
    class Meta:
        name = "checkIDType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 3,
            "max_length": 16,
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
class CreDataType:
    class Meta:
        name = "creDataType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )


@dataclass
class E164Type:
    class Meta:
        name = "e164Type"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 17,
            "pattern": r"(\+[0-9]{1,3}\.[0-9]{1,14})?",
        },
    )
    x: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class MIdtype:
    class Meta:
        name = "mIDType"

    id: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_occurs": 1,
            "min_length": 3,
            "max_length": 16,
        },
    )


@dataclass
class PaClidtype:
    class Meta:
        name = "paCLIDType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 3,
            "max_length": 16,
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


class PostalInfoEnumType(Enum):
    LOC = "loc"
    INT = "int"


@dataclass
class SIdtype:
    class Meta:
        name = "sIDType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )


class StatusValueType(Enum):
    CLIENT_DELETE_PROHIBITED = "clientDeleteProhibited"
    CLIENT_TRANSFER_PROHIBITED = "clientTransferProhibited"
    CLIENT_UPDATE_PROHIBITED = "clientUpdateProhibited"
    LINKED = "linked"
    OK = "ok"
    PENDING_CREATE = "pendingCreate"
    PENDING_DELETE = "pendingDelete"
    PENDING_TRANSFER = "pendingTransfer"
    PENDING_UPDATE = "pendingUpdate"
    SERVER_DELETE_PROHIBITED = "serverDeleteProhibited"
    SERVER_TRANSFER_PROHIBITED = "serverTransferProhibited"
    SERVER_UPDATE_PROHIBITED = "serverUpdateProhibited"


@dataclass
class AuthInfoType:
    class Meta:
        name = "authInfoType"

    pw: Optional[PwAuthInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    ext: Optional[ExtAuthInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )


@dataclass
class Check(MIdtype):
    class Meta:
        name = "check"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class CheckType:
    class Meta:
        name = "checkType"

    id: Optional[CheckIdtype] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )
    reason: Optional[ReasonType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )


@dataclass
class ChgPostalInfoType:
    class Meta:
        name = "chgPostalInfoType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_length": 1,
            "max_length": 255,
        },
    )
    org: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_length": 255,
        },
    )
    addr: Optional[AddrType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    type_value: Optional[PostalInfoEnumType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class CreData(CreDataType):
    class Meta:
        name = "creData"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class Delete(SIdtype):
    class Meta:
        name = "delete"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class IntLocType:
    class Meta:
        name = "intLocType"

    type_value: Optional[PostalInfoEnumType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PanDataType:
    class Meta:
        name = "panDataType"

    id: Optional[PaClidtype] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )
    pa_trid: Optional[TrIdtype] = field(
        default=None,
        metadata={
            "name": "paTRID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )
    pa_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "paDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )


@dataclass
class PostalInfoType:
    class Meta:
        name = "postalInfoType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    org: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_length": 255,
        },
    )
    addr: Optional[AddrType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )
    type_value: Optional[PostalInfoEnumType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
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
class TrnDataType:
    class Meta:
        name = "trnDataType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    tr_status: Optional[TrStatusType] = field(
        default=None,
        metadata={
            "name": "trStatus",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )
    re_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "reID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    re_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "reDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )
    ac_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "acID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    ac_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "acDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )


@dataclass
class AddRemType:
    class Meta:
        name = "addRemType"

    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_occurs": 1,
            "max_occurs": 7,
        },
    )


@dataclass
class AuthIdtype:
    class Meta:
        name = "authIDType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    auth_info: Optional[AuthInfoType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class DiscloseType:
    class Meta:
        name = "discloseType"

    name: list[IntLocType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_occurs": 2,
        },
    )
    org: list[IntLocType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_occurs": 2,
        },
    )
    addr: list[IntLocType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_occurs": 2,
        },
    )
    voice: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    fax: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    email: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    flag: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PanData(PanDataType):
    class Meta:
        name = "panData"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class TrnData(TrnDataType):
    class Meta:
        name = "trnData"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class ChgType:
    class Meta:
        name = "chgType"

    postal_info: list[ChgPostalInfoType] = field(
        default_factory=list,
        metadata={
            "name": "postalInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "max_occurs": 2,
        },
    )
    voice: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    fax: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_length": 1,
        },
    )
    auth_info: Optional[AuthInfoType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    disclose: Optional[DiscloseType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )


@dataclass
class ChkData(ChkDataType):
    class Meta:
        name = "chkData"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class CreateType:
    class Meta:
        name = "createType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    postal_info: list[PostalInfoType] = field(
        default_factory=list,
        metadata={
            "name": "postalInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_occurs": 1,
            "max_occurs": 2,
        },
    )
    voice: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    fax: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 1,
        },
    )
    auth_info: Optional[AuthInfoType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )
    disclose: Optional[DiscloseType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )


@dataclass
class InfDataType:
    class Meta:
        name = "infDataType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    roid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "pattern": r"(\w|_){1,80}-\w{1,8}",
        },
    )
    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_occurs": 1,
            "max_occurs": 7,
        },
    )
    postal_info: list[PostalInfoType] = field(
        default_factory=list,
        metadata={
            "name": "postalInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_occurs": 1,
            "max_occurs": 2,
        },
    )
    voice: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    fax: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 1,
        },
    )
    cl_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "clID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
        },
    )
    up_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "upID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "min_length": 3,
            "max_length": 16,
        },
    )
    up_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "upDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    tr_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "trDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    auth_info: Optional[AuthInfoType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    disclose: Optional[DiscloseType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )


@dataclass
class Info(AuthIdtype):
    class Meta:
        name = "info"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class Transfer(AuthIdtype):
    class Meta:
        name = "transfer"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class Create(CreateType):
    class Meta:
        name = "create"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class InfData(InfDataType):
    class Meta:
        name = "infData"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"


@dataclass
class UpdateType:
    class Meta:
        name = "updateType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    add: Optional[AddRemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    rem: Optional[AddRemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )
    chg: Optional[ChgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:contact-1.0",
        },
    )


@dataclass
class Update(UpdateType):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:contact-1.0"
