from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "urn:ietf:params:xml:ns:rgp-1.0"


@dataclass
class MixedType:
    class Meta:
        name = "mixedType"

    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ReportTextType:
    class Meta:
        name = "reportTextType"

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


class RgpOpType(Enum):
    REQUEST = "request"
    REPORT = "report"


class StatusValueType(Enum):
    ADD_PERIOD = "addPeriod"
    AUTO_RENEW_PERIOD = "autoRenewPeriod"
    RENEW_PERIOD = "renewPeriod"
    TRANSFER_PERIOD = "transferPeriod"
    PENDING_DELETE = "pendingDelete"
    PENDING_RESTORE = "pendingRestore"
    REDEMPTION_PERIOD = "redemptionPeriod"


@dataclass
class ReportType:
    class Meta:
        name = "reportType"

    pre_data: Optional[MixedType] = field(
        default=None,
        metadata={
            "name": "preData",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
            "required": True,
        },
    )
    post_data: Optional[MixedType] = field(
        default=None,
        metadata={
            "name": "postData",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
            "required": True,
        },
    )
    del_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "delTime",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
            "required": True,
        },
    )
    res_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "resTime",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
            "required": True,
        },
    )
    res_reason: Optional[ReportTextType] = field(
        default=None,
        metadata={
            "name": "resReason",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
            "required": True,
        },
    )
    statement: list[ReportTextType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
            "min_occurs": 1,
            "max_occurs": 2,
        },
    )
    other: Optional[MixedType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
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
class RespDataType:
    class Meta:
        name = "respDataType"

    rgp_status: list[StatusType] = field(
        default_factory=list,
        metadata={
            "name": "rgpStatus",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class RestoreType:
    class Meta:
        name = "restoreType"

    report: Optional[ReportType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
        },
    )
    op: Optional[RgpOpType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class InfData(RespDataType):
    class Meta:
        name = "infData"
        namespace = "urn:ietf:params:xml:ns:rgp-1.0"


@dataclass
class UpData(RespDataType):
    class Meta:
        name = "upData"
        namespace = "urn:ietf:params:xml:ns:rgp-1.0"


@dataclass
class UpdateType:
    class Meta:
        name = "updateType"

    restore: Optional[RestoreType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:rgp-1.0",
            "required": True,
        },
    )


@dataclass
class Update(UpdateType):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:rgp-1.0"
