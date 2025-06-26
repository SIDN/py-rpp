from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "urn:ietf:params:xml:ns:eppcom-1.0"


@dataclass
class ExtAuthInfoType:
    class Meta:
        name = "extAuthInfoType"

    other_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        },
    )


@dataclass
class PwAuthInfoType:
    class Meta:
        name = "pwAuthInfoType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    roid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"(\w|_){1,80}-\w{1,8}",
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
            "min_length": 1,
            "max_length": 32,
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


class TrStatusType(Enum):
    CLIENT_APPROVED = "clientApproved"
    CLIENT_CANCELLED = "clientCancelled"
    CLIENT_REJECTED = "clientRejected"
    PENDING = "pending"
    SERVER_APPROVED = "serverApproved"
    SERVER_CANCELLED = "serverCancelled"
