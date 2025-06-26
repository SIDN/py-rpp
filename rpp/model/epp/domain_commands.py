from rpp.model.epp.epp_1_0 import CommandType, Epp, ReadWriteType, ExtAnyType
from rpp.model.epp.domain_1_0 import AuthInfoType, ContactAttrType, ContactType, Create, Info, InfoNameType, NsType, PUnitType, PeriodType
from rpp.model.epp.eppcom_1_0 import PwAuthInfoType
from rpp.model.epp.sec_dns_1_1 import KeyDataType, Create as SecdnsCreateType
from rpp.model.rpp.domain import DomainCreateRequest
from rpp.model.epp.helpers import random_str, random_tr_id

def domain_create(req: DomainCreateRequest) -> Epp:
    # Period
    period = None
    if req.period:
        period = PeriodType(
            value=int(req.period.text),
            unit=PUnitType(req.period.unit)
        )
    # NS
    ns = None
    if req.ns:
        ns = NsType(
            host_obj=[n.value for n in req.ns if n.type == "host"],
            host_attr=[]
        )
    # Contacts
    contacts = []
    for c in req.contact or []:
        contacts.append(ContactType(
            value=c.value,
            type_value=ContactAttrType(c.type) if c.type else None
        ))
    # AuthInfo
    auth_info = None
    if req.authInfo:
        auth_info = AuthInfoType(
            pw=PwAuthInfoType(value=req.authInfo)
        )

    # secDNS_keyData
    secdns_create = None
    if req.secDNS_keyData:
        key_data = KeyDataType(
            flags=int(req.secDNS_keyData.flags),
            protocol=int(req.secDNS_keyData.protocol),
            alg=int(req.secDNS_keyData.alg),
            pub_key=req.secDNS_keyData.pubKey
        )
        secdns_create = SecdnsCreateType(
            key_data=[key_data]
        )

    return Epp(
        command=CommandType(
            create=ReadWriteType(
                other_element=Create(
                    name=req.name,
                    period=period,
                    ns=ns,
                    registrant=req.registrant,
                    contact=contacts,
                    auth_info=auth_info
                )
            ),
            extension=ExtAnyType(
                other_element=[secdns_create] if secdns_create else []
            ),
            cl_trid=req.clTRID or random_tr_id(8)
        )
    )


def domain_info(domain: str) -> Epp:
    """
    Create a domain info request object for the given domain.

    :param domain: The domain name to create the DomainInfoType for.
    :return: An Epp object with the specified domain.
    """

    epp_request = Epp(
        command=CommandType(
            info=ReadWriteType(
                other_element=Info(name=InfoNameType(value=domain))
            )
        )
    )

    return epp_request
