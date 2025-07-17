from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class AddrType:
    class Meta:
        name = "addrType"

    street: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_occurs": 3,
            "max_length": 255,
        },
    )
    city: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    sp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_length": 255,
        },
    )
    pc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_length": 16,
        },
    )
    cc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
            "length": 2,
        },
    )


@dataclass
class CheckIdtype:
    class Meta:
        name = "checkIDType"

    avail: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class ContactAttrType(Enum):
    ADMIN = "admin"
    BILLING = "billing"
    TECH = "tech"
    ABUSE = "abuse"
    CUSTOM = "custom"


@dataclass
class CreDataType:
    class Meta:
        name = "creDataType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    cr_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "crDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
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
class InfoType:
    class Meta:
        name = "infoType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
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
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class PaClidtype:
    class Meta:
        name = "paCLIDType"

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


class RoleStatusType(Enum):
    OK = "ok"
    CLIENT_LINK_PROHIBITED = "clientLinkProhibited"
    LINKED = "linked"
    SERVER_LINK_PROHIBITED = "serverLinkProhibited"


@dataclass
class SIdtype:
    class Meta:
        name = "sIDType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )


class StatusType(Enum):
    OK = "ok"
    HOLD = "hold"
    TERMINATED = "terminated"
    CLIENT_DELETE_PROHIBITED = "clientDeleteProhibited"
    CLIENT_UPDATE_PROHIBITED = "clientUpdateProhibited"
    CLIENT_LINK_PROHIBITED = "clientLinkProhibited"
    LINKED = "linked"
    PENDING_CREATE = "pendingCreate"
    PENDING_UPDATE = "pendingUpdate"
    PENDING_DELETE = "pendingDelete"
    SERVER_DELETE_PROHIBITED = "serverDeleteProhibited"
    SERVER_UPDATE_PROHIBITED = "serverUpdateProhibited"
    SERVER_LINK_PROHIBITED = "serverLinkProhibited"


@dataclass
class Check(MIdtype):
    class Meta:
        name = "check"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class CheckType:
    class Meta:
        name = "checkType"

    id: Optional[CheckIdtype] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "min_length": 1,
            "max_length": 255,
        },
    )
    addr: Optional[AddrType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
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
class ContactType:
    class Meta:
        name = "contactType"

    type_value: Optional[ContactAttrType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        },
    )
    type_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "typeName",
            "type": "Attribute",
        },
    )


@dataclass
class CreData(CreDataType):
    class Meta:
        name = "creData"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class Delete(SIdtype):
    class Meta:
        name = "delete"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class Info(InfoType):
    class Meta:
        name = "info"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class PanDataType:
    class Meta:
        name = "panDataType"

    id: Optional[PaClidtype] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    pa_trid: Optional[str] = field(
        default=None,
        metadata={
            "name": "paTRID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    pa_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "paDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    addr: Optional[AddrType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
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
class RoleType:
    class Meta:
        name = "roleType"

    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    status: list[RoleStatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_occurs": 3,
        },
    )
    role_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "roleID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )


@dataclass
class AddRemType:
    class Meta:
        name = "addRemType"

    contact: list[ContactType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    role: list[RoleType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_occurs": 9,
        },
    )


@dataclass
class ChgType:
    class Meta:
        name = "chgType"

    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentId",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    postal_info: list[ChgPostalInfoType] = field(
        default_factory=list,
        metadata={
            "name": "postalInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_occurs": 2,
        },
    )
    voice: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    fax: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class CreateType:
    class Meta:
        name = "createType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    role: list[RoleType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "min_occurs": 1,
        },
    )
    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_occurs": 4,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentId",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    postal_info: list[PostalInfoType] = field(
        default_factory=list,
        metadata={
            "name": "postalInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_occurs": 2,
        },
    )
    voice: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    fax: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    contact: list[ContactType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    roid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    role: list[RoleType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "min_occurs": 1,
        },
    )
    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "min_occurs": 1,
            "max_occurs": 9,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentId",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    postal_info: list[PostalInfoType] = field(
        default_factory=list,
        metadata={
            "name": "postalInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "max_occurs": 2,
        },
    )
    voice: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    fax: Optional[E164Type] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    contact: list[ContactType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    cl_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "clID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    cr_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "crID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    cr_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "crDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    up_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "upID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    up_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "upDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )


@dataclass
class PanData(PanDataType):
    class Meta:
        name = "panData"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class ChkData(ChkDataType):
    class Meta:
        name = "chkData"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class Create(CreateType):
    class Meta:
        name = "create"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class InfData(InfDataType):
    class Meta:
        name = "infData"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"


@dataclass
class UpdateType:
    class Meta:
        name = "updateType"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
            "required": True,
        },
    )
    add: Optional[AddRemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    rem: Optional[AddRemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )
    chg: Optional[ChgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:org-1.0",
        },
    )


@dataclass
class Update(UpdateType):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:epp:org-1.0"
