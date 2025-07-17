from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "urn:ietf:params:xml:ns:epp:orgext-1.0"


@dataclass
class OrgIdType:
    class Meta:
        name = "orgIdType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AddRemChgType:
    class Meta:
        name = "addRemChgType"

    id: list[OrgIdType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:orgext-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class CreateType:
    class Meta:
        name = "createType"

    id: list[OrgIdType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:orgext-1.0",
            "min_occurs": 1,
        },
    )


@dataclass
class InfDataType:
    class Meta:
        name = "infDataType"

    id: list[OrgIdType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:orgext-1.0",
        },
    )


@dataclass
class Create(CreateType):
    class Meta:
        name = "create"
        namespace = "urn:ietf:params:xml:ns:epp:orgext-1.0"


@dataclass
class InfData(InfDataType):
    class Meta:
        name = "infData"
        namespace = "urn:ietf:params:xml:ns:epp:orgext-1.0"


@dataclass
class UpdateType:
    class Meta:
        name = "updateType"

    add: Optional[AddRemChgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:orgext-1.0",
        },
    )
    rem: Optional[AddRemChgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:orgext-1.0",
        },
    )
    chg: Optional[AddRemChgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:epp:orgext-1.0",
        },
    )


@dataclass
class Update(UpdateType):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:epp:orgext-1.0"
