import base64

from fastapi import Response
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.epp.domain_1_0 import CheckType, ChkData, ChkDataType
from rpp.model.rpp.common import ErrorModel
from rpp.model.rpp.common_converter import is_ok_response
from rpp.model.rpp.domain import (
    DomainInfoResponse,
    EventModel,
    NameserverModel,
    ContactModel,
    DNSSECModel,
    DSDataModel,
    SecDNSKeyDataModel,
    DsOrKeyType
)


def to_domain_info(epp_response: Epp, response: Response) -> DomainInfoResponse | ErrorModel:
    if epp_response.response.result[0].code.value == 2303:
        response.status_code = 404
        return ErrorModel(code=2303, message="Domain not found")

    res_data = epp_response.response.res_data.other_element[0]

    nameservers = []
    if hasattr(res_data, "ns"):
        for ns in res_data.ns.host_obj:
            nameservers.append(NameserverModel(name=ns, linked=True))

    if hasattr(res_data, "host"):
        for ns in res_data.host:
            nameservers.append(NameserverModel(name=ns, linked=False))

    contacts = []
    for contact in res_data.contact:
        contacts.append(ContactModel(type=contact.type_value, value=contact.value))

    # DNSSEC data extraction
    dnssec = None
    if hasattr(epp_response.response, "extension") and epp_response.response.extension:
        for ext in epp_response.response.extension.other_element:
            # Check for secDNS infData
            if hasattr(ext, "key_data"):
                # KeyData present
                key_data_list = []
                for kd in getattr(ext, "key_data", []):
                    key_data_list.append(SecDNSKeyDataModel(
                        flags=kd.flags,
                        protocol=kd.protocol,
                        alg=kd.alg,
                        pubKey=base64.b64encode(kd.pub_key).decode("ascii")
                    ))
                if key_data_list:
                    dnssec = DsOrKeyType(keyData=key_data_list)
            if hasattr(ext, "ds_data"):
                # DSData present
                ds_data_list = []
                for ds in getattr(ext, "ds_data", []):
                    ds_data_list.append(DSDataModel(
                        keyTag=ds.key_tag,
                        algorithm=ds.alg,
                        digestType=ds.digest_type,
                        digest=ds.digest
                    ))
                if ds_data_list:
                    dnssec = DsOrKeyType(dsData=ds_data_list)


    events = {}
    events["Create"] = EventModel(name=res_data.cr_id, date=str(res_data.cr_date))
    if hasattr(res_data, "up_id") and res_data.up_id is not None:
        events["Update"] = EventModel(name=res_data.up_id, date=str(res_data.up_date))
    if hasattr(res_data, "tr_date") and res_data.tr_date is not None:
        events["Transfer"] = EventModel(date=str(res_data.tr_date))

    expires = None
    if hasattr(res_data, "ex_date") and res_data.ex_date is not None:
        expires = str(res_data.ex_date)

    authInfo = None
    if hasattr(res_data, "auth_info") and res_data.auth_info is not None:
        authInfo = res_data.auth_info.pw.value

    domain_info_response = DomainInfoResponse(
        name=res_data.name,
        registrant=res_data.registrant,
        contacts=contacts,
        nameservers=nameservers,
        dnssec=dnssec,
        roid=res_data.roid,
        status=[s.s for s in getattr(res_data, "status", [])],
        registrar=res_data.cl_id,
        events=events,
        expires=expires,
        authInfo=authInfo
    )
    return domain_info_response


def to_domain_check(epp_response: Epp):

    ok, epp_status, message = is_ok_response(epp_response)

    if not ok:
         return False, epp_status, message
    
    check_data: ChkDataType = epp_response.response.res_data.other_element[0]
    cd: CheckType = check_data.cd[0]
    
    return epp_status, cd.name.avail, cd.reason.value if cd.reason else None


    if epp_response.response.result[0].code.value == 1000:
        check_data: ChkData = epp_response.response.res_data.other_element[0]
        for check in check_data.cd:
            if check.name.avail == True:
                response.headers["RPP-Check-Avail"] = "true"
            else:
                response.headers["RPP-Check-Avail"] = "false"

        response.status_code = 200

    else:
        response.status_code = 500


def to_domain_delete(epp_response: Epp, response: Response):
    if epp_response.response.result[0].code.value == 2303:
         response.status_code = 404
    elif epp_response.response.result[0].code.value != 1000:
         response.status_code = 400