from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

__NAMESPACE__ = "urn:ietf:params:xml:ns:epp:ttl-1.0"


@dataclass
class Info:
    class Meta:
        name = "info"
        namespace = "urn:ietf:params:xml:ns:epp:ttl-1.0"

    policy: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


class RrType(Enum):
    NS = "NS"
    DS = "DS"
    DNAME = "DNAME"
    A = "A"
    AAAA = "AAAA"
    CUSTOM = "custom"


@dataclass
class CommandTtltype:
    class Meta:
        name = "commandTTLType"

    value: Union[str, int] = field(
        default="",
        metadata={
            "min_inclusive": 0,
            "max_inclusive": 2147483647,
            "length": 0,
        },
    )
    for_value: Optional[RrType] = field(
        default=None,
        metadata={
            "name": "for",
            "type": "Attribute",
            "required": True,
        },
    )
    custom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"A|[A-Z][A-Z0-9\-]*[A-Z0-9]",
        },
    )


@dataclass
class ResponseTtltype:
    class Meta:
        name = "responseTTLType"

    value: Union[str, int] = field(
        default="",
        metadata={
            "min_inclusive": 0,
            "max_inclusive": 2147483647,
            "length": 0,
        },
    )
    for_value: Optional[RrType] = field(
        default=None,
        metadata={
            "name": "for",
            "type": "Attribute",
            "required": True,
        },
    )
    custom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"A|[A-Z][A-Z0-9\-]*[A-Z0-9]",
        },
    )
    min: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 2147483647,
        },
    )
    default: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 2147483647,
        },
    )
    max: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_inclusive": 0,
            "max_inclusive": 2147483647,
        },
    )


@dataclass
class CommandContainer:
    class Meta:
        name = "commandContainer"

    ttl: list[CommandTtltype] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:ttl-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class ResponseContainer:
    class Meta:
        name = "responseContainer"

    ttl: list[ResponseTtltype] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:ttl-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class Create(CommandContainer):
    class Meta:
        name = "create"
        namespace = "urn:ietf:params:xml:ns:epp:ttl-1.0"


@dataclass
class InfData(ResponseContainer):
    class Meta:
        name = "infData"
        namespace = "urn:ietf:params:xml:ns:epp:ttl-1.0"


@dataclass
class Update(CommandContainer):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:epp:ttl-1.0"
