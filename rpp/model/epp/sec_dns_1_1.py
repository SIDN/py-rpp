from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "urn:ietf:params:xml:ns:secDNS-1.1"


@dataclass
class ChgType:
    class Meta:
        name = "chgType"

    max_sig_life: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxSigLife",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "min_inclusive": 1,
        },
    )


@dataclass
class KeyDataType:
    class Meta:
        name = "keyDataType"

    flags: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "required": True,
        },
    )
    protocol: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "required": True,
        },
    )
    alg: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "required": True,
        },
    )
    pub_key: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "pubKey",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "required": True,
            "min_length": 1,
            "format": "base64",
        },
    )


@dataclass
class DsDataType:
    class Meta:
        name = "dsDataType"

    key_tag: Optional[int] = field(
        default=None,
        metadata={
            "name": "keyTag",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "required": True,
        },
    )
    alg: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "required": True,
        },
    )
    digest_type: Optional[int] = field(
        default=None,
        metadata={
            "name": "digestType",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "required": True,
        },
    )
    digest: Optional[bytes] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "required": True,
            "format": "base16",
        },
    )
    key_data: Optional[KeyDataType] = field(
        default=None,
        metadata={
            "name": "keyData",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )


@dataclass
class DsOrKeyType:
    class Meta:
        name = "dsOrKeyType"

    max_sig_life: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxSigLife",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
            "min_inclusive": 1,
        },
    )
    ds_data: list[DsDataType] = field(
        default_factory=list,
        metadata={
            "name": "dsData",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )
    key_data: list[KeyDataType] = field(
        default_factory=list,
        metadata={
            "name": "keyData",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )


@dataclass
class RemType:
    class Meta:
        name = "remType"

    all: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )
    ds_data: list[DsDataType] = field(
        default_factory=list,
        metadata={
            "name": "dsData",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )
    key_data: list[KeyDataType] = field(
        default_factory=list,
        metadata={
            "name": "keyData",
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )


@dataclass
class Create(DsOrKeyType):
    class Meta:
        name = "create"
        namespace = "urn:ietf:params:xml:ns:secDNS-1.1"


@dataclass
class InfData(DsOrKeyType):
    class Meta:
        name = "infData"
        namespace = "urn:ietf:params:xml:ns:secDNS-1.1"


@dataclass
class UpdateType:
    class Meta:
        name = "updateType"

    rem: Optional[RemType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )
    add: Optional[DsOrKeyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )
    chg: Optional[ChgType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "urn:ietf:params:xml:ns:secDNS-1.1",
        },
    )
    urgent: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Update(UpdateType):
    class Meta:
        name = "update"
        namespace = "urn:ietf:params:xml:ns:secDNS-1.1"
