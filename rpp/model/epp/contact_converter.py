from rpp.model.epp.contact_1_0 import (
    AddRemType,
    AddrType,
    AuthInfoType,
    Check,
    ChgPostalInfoType,
    ChgType,
    Create,
    Delete,
    E164Type,
    Info,
    PostalInfoType,
    StatusType,
    StatusValueType,
    Transfer,
    Update,
)
from rpp.model.epp.epp_1_0 import CommandType, Epp, ExtAnyType, ReadWriteType, TransferOpType, TransferType
from rpp.model.epp.eppcom_1_0 import PwAuthInfoType
from rpp.model.epp.helpers import random_str, random_tr_id
from rpp.model.epp.sidn_ext_epp_1_0 import ContactType, CreateType, Ext
from rpp.model.rpp.entity import Card, ContactCheckRequest, ContactCreateRequest, ContactDeleteRequest, ContactInfoRequest, ContactTransferRequest, ContactUpdateRequest


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
                        card_to_postal_info(request.card)
                    ],
                    email=request.card.emails.root["email"].address,
                    voice=E164Type(
                        value=request.card.phones.root["voice"].number
                    ),
                    auth_info=AuthInfoType(
                        pw=PwAuthInfoType(value=request.authInfo.value, roid=request.authInfo.roid)) if request.authInfo else None
                )
            ),
            cl_trid=request.clTRID or random_tr_id(),
            extension=ExtAnyType(
                other_element=[
                    Ext(
                        create=CreateType(
                            contact=ContactType(legal_form=request.card.legalForm.name, legal_form_reg_no=request.card.legalForm.number)
                        )
                    )
                ]
            ) if request.card.legalForm else None,
        )
    )

    return epp_request

def card_to_postal_info(card : Card) -> PostalInfoType:
    return PostalInfoType(
            type_value="loc",
            name=card.name.full,
            org=card.organizations["org"].name,
            addr=AddrType(
                street=get_value_by_kind(
                    card.addresses.root[
                        "addr"
                    ].components,
                    "name",
                ),
                city=get_value_by_kind(
                    card.addresses.root[
                        "addr"
                    ].components,
                    "locality",
                ),
                sp=get_value_by_kind(
                    card.addresses.root[
                        "addr"
                    ].components,
                    "region",
                ),
                pc=get_value_by_kind(
                    card.addresses.root[
                        "addr"
                    ].components,
                    "postcode",
                ),
                cc=card.addresses.root[
                    "addr"
                ].countryCode,
            ),
        )


def contact_info(request: ContactInfoRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            info=ReadWriteType(other_element=Info(id=request.id, auth_info=AuthInfoType(
                pw=PwAuthInfoType(value=request.authInfo.value, roid=request.authInfo.roid)) if request.authInfo else None )),
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

def card_to_chg_postal_info(card: Card) -> ChgPostalInfoType:
    return ChgPostalInfoType(
        type_value="int" if card.int_ else "loc",
        name=card.name.full,
        org=card.organizations["org"].name if "org" in card.organizations else None,
        addr=AddrType(
            street=get_value_by_kind(
                card.addresses.root["addr"].components, "name"
            ),
            city=get_value_by_kind(
                card.addresses.root["addr"].components, "locality"
            ),
            sp=get_value_by_kind(
                card.addresses.root["addr"].components, "region"
            ),
            pc=get_value_by_kind(
                card.addresses.root["addr"].components, "postcode"
            ),
            cc=card.addresses.root["addr"].countryCode,
        ),
    )

def get_email_from_contact_change(request: ContactUpdateRequest) -> str:

    for card in request.change.contact:
        if hasattr(card, "emails") and "email" in card.emails.root:
            return card.emails.root["email"].address

def get_voice_from_contact_change(request: ContactUpdateRequest) -> str:

    for card in request.change.contact:
        if hasattr(card, "phones") and "voice" in card.phones.root:
            return card.phones.root["voice"].number


def contact_update(request: ContactUpdateRequest) -> Epp:
    add = None
    rem = None
    chg = None

    if request.change is not None:
        chg = ChgType(postal_info=[card_to_chg_postal_info(c) for c in request.change.contact],
                        voice=E164Type(value=get_voice_from_contact_change(request)),
                        email=get_email_from_contact_change(request),
                        auth_info=AuthInfoType(
                            pw=PwAuthInfoType(value=request.change.authInfo.value, roid=request.change.authInfo.roid)
                        ) if request.change.authInfo else None
        )
     

    if request.add is not None:
      add = AddRemType(
                status=[StatusType(s=StatusValueType(c)) for c in request.add.status]
            )
      
    if request.remove is not None:
      rem = AddRemType(
                status=[StatusType(s=StatusValueType(c)) for c in request.remove.status]
            )


    epp_request = Epp(
        command=CommandType(
            update=ReadWriteType(
                other_element=Update(
                    id=request.id,
                    add=add,
                    rem=rem,
                    chg=chg
                )
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request

def contact_transfer(request: ContactTransferRequest, op: str) -> Epp:
    epp_request = Epp(
        command=CommandType(
            transfer=TransferType(
                op=op,
                other_element=Transfer(
                    id=request.id,
                    auth_info=AuthInfoType(pw=PwAuthInfoType(value=request.authInfo.value, roid=request.authInfo.roid)) if request.authInfo else None,
                )
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request

def contact_transfer_query(request: ContactTransferRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            transfer=TransferType(
                op=TransferOpType.QUERY,
                other_element=Transfer(
                    id=request.id,
                    auth_info=AuthInfoType(pw=PwAuthInfoType(value=request.authInfo.value, roid=request.authInfo.roid)) if request.authInfo else None,
                )
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request