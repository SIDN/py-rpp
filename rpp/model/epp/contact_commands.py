from rpp.model.epp.contact_1_0 import (
    AddrType,
    AuthIdtype,
    AuthInfoType,
    Check,
    Create,
    Delete,
    E164Type,
    Info,
    PostalInfoType,
)
from rpp.model.epp.epp_1_0 import CommandType, Epp, ExtAnyType, ReadWriteType
from rpp.model.epp.eppcom_1_0 import PwAuthInfoType
from rpp.model.epp.helpers import random_str, random_tr_id
from rpp.model.epp.sidn_ext_epp_1_0 import ContactType, CreateType, Ext
from rpp.model.rpp.entity import Card, ContactCheckRequest, ContactCreateRequest, ContactDeleteRequest, ContactInfoRequest


def get_value_by_kind(components: list[dict], kind: str) -> str | None:
    for comp in components:
        if comp.kind == kind:
            return comp.value
    return None


def contact_create(request: ContactCreateRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            create=ReadWriteType(
                other_element=Create(
                    id=request.card.id,
                    postal_info=[
                        PostalInfoType(
                            type_value="loc",
                            name=request.card.name.full,
                            org=request.card.organizations["org"].name,
                            addr=AddrType(
                                street=get_value_by_kind(
                                    request.card.addresses.root[
                                        "addr"
                                    ].components,
                                    "name",
                                ),
                                city=get_value_by_kind(
                                    request.card.addresses.root[
                                        "addr"
                                    ].components,
                                    "locality",
                                ),
                                sp=get_value_by_kind(
                                    request.card.addresses.root[
                                        "addr"
                                    ].components,
                                    "region",
                                ),
                                pc=get_value_by_kind(
                                    request.card.addresses.root[
                                        "addr"
                                    ].components,
                                    "postcode",
                                ),
                                cc=request.card.addresses.root[
                                    "addr"
                                ].countryCode,
                            ),
                        )
                    ],
                    email=request.card.emails.root["email"].address,
                    voice=E164Type(
                        value=request.card.phones.root["voice"].number
                    ),
                    auth_info=AuthInfoType(
                        pw=PwAuthInfoType(value=random_str(8))
                    ),
                )
            ),
            cl_trid=request.clTRID or random_tr_id(),
            extension=ExtAnyType(
                other_element=[
                    Ext(
                        create=CreateType(
                            contact=ContactType(legal_form="PERSOON")
                        )
                    )
                ]
            ),
        )
    )

    return epp_request


def contact_info(request: ContactInfoRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            info=ReadWriteType(other_element=Info(id=request.id)),
            cl_trid=request.clTRID or random_tr_id()
        )
    )

    return epp_request


def contact_check(request: ContactCheckRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            check=ReadWriteType(
                other_element=Check(id=[request.name])
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request

def contact_delete(request: ContactDeleteRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            delete=ReadWriteType(
                other_element=Delete(id=request.name)
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request