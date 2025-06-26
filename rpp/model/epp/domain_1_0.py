from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from rpp.model.epp.epp_1_0 import TrIdtype
from rpp.model.epp.eppcom_1_0 import (
    ExtAuthInfoType,
    PwAuthInfoType,
    ReasonType,
    TrStatusType,
)
from rpp.model.epp.host_1_0 import AddrType

__NAMESPACE__ = "urn:ietf:params:xml:ns:domain-1.0"


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


class ContactAttrType(Enum):
    ADMIN = "admin"
    BILLING = "billing"
    TECH = "tech"


@dataclass
class CreDataType:
    class Meta:
        name = "creDataType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )
    ex_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "exDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


class HostsType(Enum):
    ALL = "all"
    DEL = "del"
    NONE = "none"
    SUB = "sub"


@dataclass
class MNameType:
    class Meta:
        name = "mNameType"

    name: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_occurs": 1,
            "min_length": 1,
            "max_length": 255,
        },
    )


class PUnitType(Enum):
    Y = "y"
    M = "m"


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
class RenDataType:
    class Meta:
        name = "renDataType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    ex_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "exDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )


class StatusValueType(Enum):
    CLIENT_DELETE_PROHIBITED = "clientDeleteProhibited"
    CLIENT_HOLD = "clientHold"
    CLIENT_RENEW_PROHIBITED = "clientRenewProhibited"
    CLIENT_TRANSFER_PROHIBITED = "clientTransferProhibited"
    CLIENT_UPDATE_PROHIBITED = "clientUpdateProhibited"
    INACTIVE = "inactive"
    OK = "ok"
    PENDING_CREATE = "pendingCreate"
    PENDING_DELETE = "pendingDelete"
    PENDING_RENEW = "pendingRenew"
    PENDING_TRANSFER = "pendingTransfer"
    PENDING_UPDATE = "pendingUpdate"
    SERVER_DELETE_PROHIBITED = "serverDeleteProhibited"
    SERVER_HOLD = "serverHold"
    SERVER_RENEW_PROHIBITED = "serverRenewProhibited"
    SERVER_TRANSFER_PROHIBITED = "serverTransferProhibited"
    SERVER_UPDATE_PROHIBITED = "serverUpdateProhibited"


@dataclass
class AuthInfoChgType:
    class Meta:
        name = "authInfoChgType"

    pw: Optional[PwAuthInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    ext: Optional[ExtAuthInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    null: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class AuthInfoType:
    class Meta:
        name = "authInfoType"

    pw: Optional[PwAuthInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    ext: Optional[ExtAuthInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class Check(MNameType):
    class Meta:
        name = "check"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class CheckType:
    class Meta:
        name = "checkType"

    name: Optional[CheckNameType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )
    reason: Optional[ReasonType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class ContactType:
    class Meta:
        name = "contactType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    type_value: Optional[ContactAttrType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass
class CreData(CreDataType):
    class Meta:
        name = "creData"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class Delete(SNameType):
    class Meta:
        name = "delete"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class HostAttrType:
    class Meta:
        name = "hostAttrType"

    host_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "hostName",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    host_addr: list[AddrType] = field(
        default_factory=list,
        metadata={
            "name": "hostAddr",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class InfoNameType:
    class Meta:
        name = "infoNameType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    hosts: HostsType = field(
        default=HostsType.ALL,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class PanDataType:
    class Meta:
        name = "panDataType"

    name: Optional[PaNameType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )
    pa_trid: Optional[TrIdtype] = field(
        default=None,
        metadata={
            "name": "paTRID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )
    pa_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "paDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )


@dataclass
class PeriodType:
    class Meta:
        name = "periodType"

    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 99,
        },
    )
    unit: Optional[PUnitType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class RenData(RenDataType):
    class Meta:
        name = "renData"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


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

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    tr_status: Optional[TrStatusType] = field(
        default=None,
        metadata={
            "name": "trStatus",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )
    re_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "reID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )
    ac_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "acID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_length": 3,
            "max_length": 16,
        },
    )
    ac_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "acDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    ex_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "exDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class ChgType:
    class Meta:
        name = "chgType"

    registrant: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_length": 0,
            "max_length": 16,
        },
    )
    auth_info: Optional[AuthInfoChgType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class InfoType:
    class Meta:
        name = "infoType"

    name: Optional[InfoNameType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )
    auth_info: Optional[AuthInfoType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class NsType:
    class Meta:
        name = "nsType"

    host_obj: list[str] = field(
        default_factory=list,
        metadata={
            "name": "hostObj",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_length": 1,
            "max_length": 255,
        },
    )
    host_attr: list[HostAttrType] = field(
        default_factory=list,
        metadata={
            "name": "hostAttr",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class PanData(PanDataType):
    class Meta:
        name = "panData"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class RenewType:
    class Meta:
        name = "renewType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    cur_exp_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "curExpDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
        },
    )
    period: Optional[PeriodType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class TransferType:
    class Meta:
        name = "transferType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    period: Optional[PeriodType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    auth_info: Optional[AuthInfoType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class TrnData(TrnDataType):
    class Meta:
        name = "trnData"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class AddRemType:
    class Meta:
        name = "addRemType"

    ns: Optional[NsType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    contact: list[ContactType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "max_occurs": 11,
        },
    )


@dataclass
class ChkData(ChkDataType):
    class Meta:
        name = "chkData"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class CreateType:
    class Meta:
        name = "createType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    period: Optional[PeriodType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    ns: Optional[NsType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    registrant: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_length": 3,
            "max_length": 16,
        },
    )
    contact: list[ContactType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    auth_info: Optional[AuthInfoType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
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
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    roid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "pattern": r"(\w|_){1,80}-\w{1,8}",
        },
    )
    status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "max_occurs": 11,
        },
    )
    registrant: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_length": 3,
            "max_length": 16,
        },
    )
    contact: list[ContactType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    ns: Optional[NsType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    host: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_length": 1,
            "max_length": 255,
        },
    )
    cl_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "clID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
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
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_length": 3,
            "max_length": 16,
        },
    )
    cr_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "crDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    up_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "upID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "min_length": 3,
            "max_length": 16,
        },
    )
    up_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "upDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    ex_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "exDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    tr_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "trDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    auth_info: Optional[AuthInfoType] = field(
        default=None,
        metadata={
            "name": "authInfo",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class Info(InfoType):
    class Meta:
        name = "info"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class Renew(RenewType):
    class Meta:
        name = "renew"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class Transfer(TransferType):
    class Meta:
        name = "transfer"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class Create(CreateType):
    class Meta:
        name = "create"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class InfData(InfDataType):
    class Meta:
        name = "infData"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"


@dataclass
class UpdateType:
    class Meta:
        name = "updateType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    add: Optional[AddRemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    rem: Optional[AddRemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )
    chg: Optional[ChgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:domain-1.0",
        },
    )


@dataclass
class Update(UpdateType):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:domain-1.0"
