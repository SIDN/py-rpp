from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from rpp.model.epp.domain_1_0 import PeriodType
from rpp.model.epp.epp_1_0 import ResponseType as Epp10ResponseType
from rpp.model.epp.eppcom_1_0 import PwAuthInfoType

__NAMESPACE__ = "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0"


@dataclass
class ContactType:
    class Meta:
        name = "contactType"

    legal_form: Optional[str] = field(
        default=None,
        metadata={
            "name": "legalForm",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    legal_form_reg_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "legalFormRegNo",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    limited: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )


@dataclass
class HostType:
    class Meta:
        name = "hostType"

    limited: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
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
    code: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    field_value: Optional[object] = field(
        default=None,
        metadata={
            "name": "field",
            "type": "Attribute",
        },
    )


@dataclass
class DomainCancelDeleteType:
    class Meta:
        name = "domainCancelDeleteType"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
            "required": True,
            "min_length": 1,
            "max_length": 255,
        },
    )
    period: Optional[PeriodType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )


@dataclass
class DomainType:
    class Meta:
        name = "domainType"

    opt_out: Optional[bool] = field(
        default=None,
        metadata={
            "name": "optOut",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
            "required": True,
        },
    )
    limited: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    period: Optional[PeriodType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    scheduled_delete_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "scheduledDeleteDate",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
            "nillable": True,
        },
    )


@dataclass
class PollDataType:
    class Meta:
        name = "pollDataType"

    command: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
            "required": True,
        },
    )
    data: Optional[Epp10ResponseType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
            "required": True,
        },
    )


@dataclass
class ResponseType:
    class Meta:
        name = "responseType"

    msg: list[MsgType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )


@dataclass
class TransferType:
    class Meta:
        name = "transferType"

    pw: Optional[PwAuthInfoType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    domainname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
            "min_length": 1,
            "max_length": 255,
        },
    )
    requestor: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    request_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "requestDate",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    supply_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "supplyDate",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )


@dataclass
class CommandType:
    class Meta:
        name = "commandType"

    domain_cancel_delete: Optional[DomainCancelDeleteType] = field(
        default=None,
        metadata={
            "name": "domainCancelDelete",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
            "required": True,
        },
    )
    cl_trid: Optional[str] = field(
        default=None,
        metadata={
            "name": "clTRID",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
            "min_length": 3,
            "max_length": 64,
        },
    )


@dataclass
class CreateType:
    class Meta:
        name = "createType"

    contact: Optional[ContactType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    domain: Optional[DomainType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    host: Optional[HostType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )


@dataclass
class PollData(PollDataType):
    class Meta:
        name = "pollData"
        namespace = "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0"


@dataclass
class UpdateType:
    class Meta:
        name = "updateType"

    contact: Optional[ContactType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    domain: Optional[DomainType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )


@dataclass
class Command(CommandType):
    class Meta:
        name = "command"
        namespace = "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0"


@dataclass
class ExtType:
    class Meta:
        name = "extType"

    create: Optional[CreateType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    update: Optional[UpdateType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    inf_data: Optional[CreateType] = field(
        default=None,
        metadata={
            "name": "infData",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    trn_data: Optional[TransferType] = field(
        default=None,
        metadata={
            "name": "trnData",
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )
    response: Optional[ResponseType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0",
        },
    )


@dataclass
class Ext(ExtType):
    class Meta:
        name = "ext"
        namespace = "http://rxsd.domain-registry.nl/sidn-ext-epp-1.0"
