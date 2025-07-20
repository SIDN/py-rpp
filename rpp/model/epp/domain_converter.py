from xsdata.models.datatype import XmlDate

from rpp.model.epp.domain_1_0 import (
    AddRemType,
    AuthInfoChgType,
    AuthInfoType,
    Check,
    ChgType,
    ContactAttrType,
    ContactType,
    Create,
    Delete,
    Info,
    InfoNameType,
    NsType,
    PeriodType,
    PUnitType,
    Renew,
    StatusType,
    StatusValueType,
    Transfer,
    Update,
)
from rpp.model.epp.epp_1_0 import (
    CommandType,
    Epp,
    ExtAnyType,
    ReadWriteType,
    TransferOpType,
    TransferType,
)
from rpp.model.epp.eppcom_1_0 import PwAuthInfoType
from rpp.model.epp.helpers import random_str, random_tr_id
from rpp.model.epp.sec_dns_1_1 import Create as SecdnsCreateType
from rpp.model.epp.sec_dns_1_1 import KeyDataType
from rpp.model.rpp.common import AuthInfoModel
from rpp.model.rpp.domain import (
    DomainCheckRequest,
    DomainCreateRequest,
    DomainInfoRequest,
    DomainRenewRequest,
    DomainStartTransferRequest,
    DomainTransferRequest,
    DomainUpdateRequest,
)


def domain_create(req: DomainCreateRequest, rpp_cl_trid: str) -> Epp:
    # Period
    period = None
    if req.period:
        period = PeriodType(
            value=int(req.period.value), unit=PUnitType(req.period.unit)
        )
    # NS
    ns = None
    if req.ns:
        ns = NsType(
            host_obj=[n.value for n in req.ns if n.type == "host"],
            host_attr=[],
        )
    # Contacts
    contacts = []
    for c in req.contact or []:
        contacts.append(
            ContactType(
                value=c.value,
                type_value=ContactAttrType(c.type) if c.type else None,
            )
        )
    # AuthInfo
    auth_info = None
    if req.authInfo:
        auth_info = AuthInfoType(
            pw=PwAuthInfoType(value=req.authInfo.value, roid=req.authInfo.roid)
        )

    # dnssec.keyData
    secdns_create = None
    if req.dnssec and req.dnssec.keyData:
        secdns_create = []
        for key in req.dnssec.keyData:
            key_data = KeyDataType(
                flags=int(key.flags),
                protocol=int(key.protocol),
                alg=int(key.alg),
                pub_key=key.pubKey,
            )

        secdns_create = SecdnsCreateType(key_data=[key_data])

    return Epp(
        command=CommandType(
            create=ReadWriteType(
                other_element=Create(
                    name=req.name,
                    period=period,
                    ns=ns,
                    registrant=req.registrant,
                    contact=contacts,
                    auth_info=auth_info,
                )
            ),
            extension=ExtAnyType(other_element=[secdns_create])
            if secdns_create
            else None,
            cl_trid=rpp_cl_trid or random_tr_id(),
        )
    )


def domain_info(domainname: str, rpp_cl_trid: str, auth_info: AuthInfoModel) -> Epp:
    auth_inf_type = (
        AuthInfoType(pw=PwAuthInfoType(value=auth_info.value, roid=auth_info.roid))
        if auth_info else None
    )
    epp_request = Epp(
        command=CommandType(
            info=ReadWriteType(
                other_element=Info(
                    name=InfoNameType(value=domainname), auth_info=auth_inf_type
                )
            ),
            cl_trid=rpp_cl_trid or random_tr_id(),
        )
    )

    return epp_request


def domain_check(request: DomainCheckRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            check=ReadWriteType(other_element=Check(name=[request.name])),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request


def domain_delete(domain: str) -> Epp:
    """
    Create a domain delete request object for the given domain.

    :param domain: The domain name to create the DomainDeleteType for.
    :return: An Epp object with the specified domain.
    """

    epp_request = Epp(
        command=CommandType(
            delete=ReadWriteType(other_element=Delete(name=domain))
        )
    )

    return epp_request


def domain_update(domainname: str, request: DomainUpdateRequest, rpp_cl_trid: str) -> Epp:
    add = None
    rem = None
    chg = None

    if request.change:
        chg = ChgType(
            registrant=request.change.registrant,
            auth_info=AuthInfoChgType(
                pw=PwAuthInfoType(
                    value=request.change.authInfo.value,
                    roid=request.change.authInfo.roid,
                )
            )
            if request.change.authInfo
            else None,
        )

    if request.add is not None:
        add = AddRemType(
            ns=NsType(host_obj=[n for n in request.add.ns]) if request.add.ns else None,
            contact=[
                ContactType(
                    value=c.value,
                    type_value=ContactAttrType(c.type) if c.type else None,
                )
                for c in request.add.contact
            ]
            if request.add.contact
            else None,
            status=[
                StatusType(
                    value = s.value if s.value else None,
                    s = StatusValueType(s.s),
                    lang = s.lang if s.lang else None
                )
                for s in request.add.status
            ]
            if request.add.status
            else None
        )
    if request.remove is not None:
        rem = AddRemType(
            ns=NsType(host_obj=[n for n in request.remove.ns]) if request.remove.ns else None,
            contact=[
                ContactType(
                    value=c.value,
                    type_value=ContactAttrType(c.type) if c.type else None,
                )
                for c in request.remove.contact
            ]
            if request.remove.contact
            else None,
            status=[
                StatusType(
                    value = s.value if s.value else None,
                    s = StatusValueType(s.s),
                    lang = s.lang if s.lang else None
                )
                for s in request.remove.status
            ]
            if request.remove.status
            else None,
        )

    epp_request = Epp(
        command=CommandType(
            update=ReadWriteType(
                other_element=Update(
                    name=domainname, add=add, rem=rem, chg=chg
                )
            ),
            cl_trid=rpp_cl_trid or random_tr_id(),
        )
    )

    return epp_request


def domain_renew(domainname: str, request: DomainRenewRequest, rpp_cl_trid: str) -> Epp:
    period = None
    if request.period:
        period = PeriodType(
            value=request.period.value, unit=PUnitType(request.period.unit)
        )

    epp_request = Epp(
        command=CommandType(
            renew=ReadWriteType(
                other_element=Renew(
                    name=domainname,
                    cur_exp_date=XmlDate.from_date(request.currentExpiry),
                    period=period,
                )
            ),
            cl_trid=rpp_cl_trid or random_tr_id(),
        )
    )

    return epp_request


def domain_transfer(
    request: DomainStartTransferRequest, op: TransferOpType
) -> Epp:
    epp_request = Epp(
        command=CommandType(
            transfer=TransferType(
                op=op,
                other_element=Transfer(
                    name=request.name,
                    period=PeriodType(
                        value=request.period.value,
                        unit=PUnitType(request.period.unit),
                    )
                    if request.period
                    else None,
                    auth_info=AuthInfoType(
                        pw=PwAuthInfoType(
                            value=request.authInfo.value,
                            roid=request.authInfo.roid,
                        )
                    )
                    if request.authInfo
                    else None,
                ),
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request


def domain_transfer_query(request: DomainTransferRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            transfer=TransferType(
                op=TransferOpType.QUERY,
                other_element=Transfer(
                    name=request.name,
                    period=PeriodType(
                        value=request.period.value,
                        unit=PUnitType(request.period.unit),
                    )
                    if request.period
                    else None,
                    auth_info=AuthInfoType(
                        pw=PwAuthInfoType(
                            value=request.authInfo.value,
                            roid=request.authInfo.roid,
                        )
                    )
                    if request.authInfo
                    else None,
                ),
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request
