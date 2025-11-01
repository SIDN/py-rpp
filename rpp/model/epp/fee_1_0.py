from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDuration

__NAMESPACE__ = "urn:ietf:params:xml:ns:epp:fee-1.0"


class CommandEnum(Enum):
    CREATE = "create"
    DELETE = "delete"
    RENEW = "renew"
    UPDATE = "update"
    TRANSFER = "transfer"
    RESTORE = "restore"
    CUSTOM = "custom"


@dataclass
class CreditType:
    class Meta:
        name = "creditType"

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "required": True,
            "max_inclusive": Decimal("0"),
        },
    )
    description: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: str = field(
        default="en",
        metadata={
            "type": "Attribute",
        },
    )


class FeeTypeApplied(Enum):
    IMMEDIATE = "immediate"
    DELAYED = "delayed"


@dataclass
class ObjectIdentifierType:
    class Meta:
        name = "objectIdentifierType"

    element: str = field(
        default="name",
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class ReasonType:
    class Meta:
        name = "reasonType"

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


@dataclass
class CommandType:
    class Meta:
        name = "commandType"

    period: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    name: Optional[CommandEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    custom_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "customName",
            "type": "Attribute",
        },
    )
    phase: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    subphase: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class FeeType:
    class Meta:
        name = "feeType"

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "required": True,
            "min_inclusive": Decimal("0"),
        },
    )
    description: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: str = field(
        default="en",
        metadata={
            "type": "Attribute",
        },
    )
    refundable: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    grace_period: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "grace-period",
            "type": "Attribute",
        },
    )
    applied: Optional[FeeTypeApplied] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class CheckType:
    class Meta:
        name = "checkType"

    currency: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
            "pattern": r"[A-Z]{3}",
        },
    )
    command: list[CommandType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class CommandDataType(CommandType):
    class Meta:
        name = "commandDataType"

    fee: list[FeeType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    credit: list[CreditType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    reason: Optional[ReasonType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    standard: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class TransformCommandType:
    class Meta:
        name = "transformCommandType"

    currency: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
            "pattern": r"[A-Z]{3}",
        },
    )
    fee: list[FeeType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
            "min_occurs": 1,
        },
    )
    credit: list[CreditType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )


@dataclass
class TransformResultType:
    class Meta:
        name = "transformResultType"

    currency: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
            "pattern": r"[A-Z]{3}",
        },
    )
    period: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    fee: list[FeeType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    credit: list[CreditType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    balance: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    credit_limit: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "creditLimit",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )


@dataclass
class Check(CheckType):
    class Meta:
        name = "check"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class CreData(TransformResultType):
    class Meta:
        name = "creData"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class Create(TransformCommandType):
    class Meta:
        name = "create"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class DelData(TransformResultType):
    class Meta:
        name = "delData"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class ObjectCdtype:
    class Meta:
        name = "objectCDType"

    obj_id: Optional[ObjectIdentifierType] = field(
        default=None,
        metadata={
            "name": "objID",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
            "required": True,
        },
    )
    class_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    command: list[CommandDataType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    reason: Optional[ReasonType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
        },
    )
    avail: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class RenData(TransformResultType):
    class Meta:
        name = "renData"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class Renew(TransformCommandType):
    class Meta:
        name = "renew"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class Transfer(TransformCommandType):
    class Meta:
        name = "transfer"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class TrnData(TransformResultType):
    class Meta:
        name = "trnData"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class UpdData(TransformResultType):
    class Meta:
        name = "updData"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class Update(TransformCommandType):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"


@dataclass
class ChkDataType:
    class Meta:
        name = "chkDataType"

    currency: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
            "required": True,
            "pattern": r"[A-Z]{3}",
        },
    )
    cd: list[ObjectCdtype] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:fee-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class ChkData(ChkDataType):
    class Meta:
        name = "chkData"
        namespace = "urn:ietf:params:xml:ns:epp:fee-1.0"
