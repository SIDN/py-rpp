from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDateTime, XmlDuration

__NAMESPACE__ = "urn:ietf:params:xml:ns:epp-1.0"


@dataclass
class DcpAccessType:
    class Meta:
        name = "dcpAccessType"

    all: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    none: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    null: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    other: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    personal: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    personal_and_other: Optional[object] = field(
        default=None,
        metadata={
            "name": "personalAndOther",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class DcpExpiryType:
    class Meta:
        name = "dcpExpiryType"

    absolute: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    relative: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class DcpOursType:
    class Meta:
        name = "dcpOursType"

    rec_desc: Optional[str] = field(
        default=None,
        metadata={
            "name": "recDesc",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_length": 1,
            "max_length": 255,
        },
    )


@dataclass
class DcpPurposeType:
    class Meta:
        name = "dcpPurposeType"

    admin: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    contact: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    other: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    prov: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class DcpRetentionType:
    class Meta:
        name = "dcpRetentionType"

    business: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    indefinite: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    legal: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    none: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    stated: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class ErrValueType:
    class Meta:
        name = "errValueType"

    any_attributes: dict[str, str] = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##any",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ExtAnyType:
    class Meta:
        name = "extAnyType"

    other_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        },
    )


@dataclass
class ExtUritype:
    class Meta:
        name = "extURIType"

    ext_uri: list[str] = field(
        default_factory=list,
        metadata={
            "name": "extURI",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class MixedMsgType:
    class Meta:
        name = "mixedMsgType"

    lang: str = field(
        default="en",
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class MsgType:
    class Meta:
        name = "msgType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    lang: str = field(
        default="en",
        metadata={
            "type": "Attribute",
        },
    )


class PollOpType(Enum):
    ACK = "ack"
    REQ = "req"


@dataclass
class ReadWriteType:
    class Meta:
        name = "readWriteType"

    other_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        },
    )


class ResultCodeType(Enum):
    VALUE_1000 = 1000
    VALUE_1001 = 1001
    VALUE_1300 = 1300
    VALUE_1301 = 1301
    VALUE_1500 = 1500
    VALUE_2000 = 2000
    VALUE_2001 = 2001
    VALUE_2002 = 2002
    VALUE_2003 = 2003
    VALUE_2004 = 2004
    VALUE_2005 = 2005
    VALUE_2100 = 2100
    VALUE_2101 = 2101
    VALUE_2102 = 2102
    VALUE_2103 = 2103
    VALUE_2104 = 2104
    VALUE_2105 = 2105
    VALUE_2106 = 2106
    VALUE_2200 = 2200
    VALUE_2201 = 2201
    VALUE_2202 = 2202
    VALUE_2300 = 2300
    VALUE_2301 = 2301
    VALUE_2302 = 2302
    VALUE_2303 = 2303
    VALUE_2304 = 2304
    VALUE_2305 = 2305
    VALUE_2306 = 2306
    VALUE_2307 = 2307
    VALUE_2308 = 2308
    VALUE_2400 = 2400
    VALUE_2500 = 2500
    VALUE_2501 = 2501
    VALUE_2502 = 2502


@dataclass
class TrIdtype:
    class Meta:
        name = "trIDType"

    cl_trid: Optional[str] = field(
        default=None,
        metadata={
            "name": "clTRID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_length": 3,
            "max_length": 64,
        },
    )
    sv_trid: Optional[str] = field(
        default=None,
        metadata={
            "name": "svTRID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 64,
        },
    )


class TransferOpType(Enum):
    APPROVE = "approve"
    CANCEL = "cancel"
    QUERY = "query"
    REJECT = "reject"
    REQUEST = "request"


class VersionType(Enum):
    VALUE_1_0 = "1.0"


@dataclass
class CredsOptionsType:
    class Meta:
        name = "credsOptionsType"

    version: Optional[VersionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )


@dataclass
class DcpRecipientType:
    class Meta:
        name = "dcpRecipientType"

    other: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    ours: list[DcpOursType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    public: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    same: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    unrelated: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class ExtErrValueType:
    class Meta:
        name = "extErrValueType"

    value: Optional[ErrValueType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    reason: Optional[MsgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )


@dataclass
class LoginSvcType:
    class Meta:
        name = "loginSvcType"

    obj_uri: list[str] = field(
        default_factory=list,
        metadata={
            "name": "objURI",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_occurs": 1,
        },
    )
    svc_extension: Optional[ExtUritype] = field(
        default=None,
        metadata={
            "name": "svcExtension",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class MsgQtype:
    class Meta:
        name = "msgQType"

    q_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "qDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    msg: Optional[MixedMsgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
        },
    )


@dataclass
class PollType:
    class Meta:
        name = "pollType"

    op: Optional[PollOpType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    msg_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "msgID",
            "type": "Attribute",
        },
    )


@dataclass
class SvcMenuType:
    class Meta:
        name = "svcMenuType"

    version: list[VersionType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_occurs": 1,
        },
    )
    lang: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_occurs": 1,
        },
    )
    obj_uri: list[str] = field(
        default_factory=list,
        metadata={
            "name": "objURI",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_occurs": 1,
        },
    )
    svc_extension: Optional[ExtUritype] = field(
        default=None,
        metadata={
            "name": "svcExtension",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class TransferType:
    class Meta:
        name = "transferType"

    other_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        },
    )
    op: Optional[TransferOpType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DcpStatementType:
    class Meta:
        name = "dcpStatementType"

    purpose: Optional[DcpPurposeType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    recipient: Optional[DcpRecipientType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    retention: Optional[DcpRetentionType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )


@dataclass
class LoginType:
    class Meta:
        name = "loginType"

    cl_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "clID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 16,
        },
    )
    pw: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
            "min_length": 8,
            "max_length": 64,
        },
    )
    new_pw: Optional[str] = field(
        default=None,
        metadata={
            "name": "newPW",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_length": 8,
            "max_length": 64,
        },
    )
    options: Optional[CredsOptionsType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    svcs: Optional[LoginSvcType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )


@dataclass
class ResultType:
    class Meta:
        name = "resultType"

    msg: Optional[MsgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    value: list[ErrValueType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    ext_value: list[ExtErrValueType] = field(
        default_factory=list,
        metadata={
            "name": "extValue",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    code: Optional[ResultCodeType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class CommandType:
    class Meta:
        name = "commandType"

    check: Optional[ReadWriteType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    create: Optional[ReadWriteType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    delete: Optional[ReadWriteType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    info: Optional[ReadWriteType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    login: Optional[LoginType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    logout: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    poll: Optional[PollType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    renew: Optional[ReadWriteType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    transfer: Optional[TransferType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    update: Optional[ReadWriteType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    extension: Optional[ExtAnyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    cl_trid: Optional[str] = field(
        default=None,
        metadata={
            "name": "clTRID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_length": 3,
            "max_length": 64,
        },
    )


@dataclass
class DcpType:
    class Meta:
        name = "dcpType"

    access: Optional[DcpAccessType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    statement: list[DcpStatementType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_occurs": 1,
        },
    )
    expiry: Optional[DcpExpiryType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class ResponseType:
    class Meta:
        name = "responseType"

    result: list[ResultType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "min_occurs": 1,
        },
    )
    msg_q: Optional[MsgQtype] = field(
        default=None,
        metadata={
            "name": "msgQ",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    res_data: Optional[ExtAnyType] = field(
        default=None,
        metadata={
            "name": "resData",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    extension: Optional[ExtAnyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    tr_id: Optional[TrIdtype] = field(
        default=None,
        metadata={
            "name": "trID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )


@dataclass
class GreetingType:
    class Meta:
        name = "greetingType"

    sv_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "svID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
            "min_length": 3,
            "max_length": 64,
        },
    )
    sv_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "svDate",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    svc_menu: Optional[SvcMenuType] = field(
        default=None,
        metadata={
            "name": "svcMenu",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )
    dcp: Optional[DcpType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
            "required": True,
        },
    )


@dataclass
class EppType:
    class Meta:
        name = "eppType"

    greeting: Optional[GreetingType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    hello: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    command: Optional[CommandType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    response: Optional[ResponseType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )
    extension: Optional[ExtAnyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp-1.0",
        },
    )


@dataclass
class Epp(EppType):
    class Meta:
        name = "epp"
        namespace = "urn:ietf:params:xml:ns:epp-1.0"
