from typing import List, Dict

from fastapi import Response
from rpp.model.epp.contact_1_0 import CheckType, ChkDataType, TrnDataType
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.rpp.common import AuthInfoModel, BaseResponseModel, TrIDModel
from rpp.model.rpp.common_converter import is_ok_response, to_base_response, to_result_list
from rpp.model.rpp.entity import Card, ContactCreateResponseModel, ContactInfoResponse, EventModel, Name, AddressComponent, Organization, Address, TransferResponse

def to_contact_info(epp_response) -> BaseResponseModel:

    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
        return to_base_response(epp_response)

    res_data = epp_response.response.res_data.other_element[0]

    # Use Name model for the name property
    name = None
    if hasattr(res_data, "postal_info"):
        pi = res_data.postal_info[0]  # Assuming there's only one postal_info

        # Build components as list of AddressComponent
        components: List[AddressComponent] = []
        if pi.addr:
            if pi.addr.street:
                for street in pi.addr.street:
                    components.append(AddressComponent(kind="street", value=street))
            if pi.addr.city:
                components.append(AddressComponent(kind="city", value=pi.addr.city))
            if pi.addr.sp:
                components.append(AddressComponent(kind="state", value=pi.addr.sp))
            if pi.addr.pc:
                components.append(AddressComponent(kind="postal_code", value=pi.addr.pc))
            if pi.addr.cc:
                components.append(AddressComponent(kind="country", value=pi.addr.cc))

        name = Name(
            full=pi.name
        )

        addresses = { "addr": Address(components=components) }

        organizations = None
        if pi.org:
           organizations = {"org": Organization(name=pi.org)} 

        events: Dict[str, EventModel] = {}
        if hasattr(res_data, "cr_id"):
            events["Create"] = EventModel(name=res_data.cr_id, date=str(res_data.cr_date))

        if hasattr(res_data, "up_id") and res_data.up_id is not None:
            events["Update"] = EventModel(name=res_data.up_id, date=str(res_data.up_date))

        if hasattr(res_data, "tr_id") and res_data.tr_id is not None:
            events["Transfer"] = EventModel(date=str(res_data.tr_date))
        
        authInfo = None
        if hasattr(res_data, "auth_info") and res_data.auth_info is not None:
            authInfo = AuthInfoModel(
                    value=res_data.auth_info.pw.value,
                    roid=res_data.auth_info.roid) 

    card = Card(
        id=res_data.id,
        roid=res_data.roid,
        name=name,
        organizations=organizations,
        addresses=addresses,
    )

    infData = ContactInfoResponse(
        card=card,
        status=[s.s.value for s in res_data.status],
        events=events,
        authInfo=authInfo
    )

    return BaseResponseModel(
        trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
        svTRID=epp_response.response.tr_id.sv_trid),
        result=to_result_list(epp_response),
        resData=infData
    )

def to_contact_check(epp_response: Epp) -> tuple[bool, int, str]:
    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
         return None, epp_status, message
    
    check_data: ChkDataType = epp_response.response.res_data.other_element[0]
    cd: CheckType = check_data.cd[0]

    return cd.id.avail, epp_status, cd.reason.value if cd.reason else None

def to_contact_create(epp_response) -> BaseResponseModel:
    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
        return to_base_response(epp_response)

    res_data = epp_response.response.res_data.other_element[0]

    resData = ContactCreateResponseModel(
        id=res_data.id,
        createDate=str(res_data.cr_date) if hasattr(res_data, "cr_date") else None)
    
    return BaseResponseModel(
        trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
                                svTRID=epp_response.response.tr_id.sv_trid),
        result=to_result_list(epp_response),
        resData=resData)

def to_contact_delete(epp_response: Epp, response: Response) -> BaseResponseModel:
    return to_base_response(epp_response)

def to_contact_update(epp_response: Epp, response: Response) -> BaseResponseModel:
    return to_base_response(epp_response)

def to_contact_transfer(epp_response: Epp, response: Response) -> BaseResponseModel:
    ok, epp_status, message = is_ok_response(epp_response)
    if not ok or not hasattr(epp_response.response.res_data, "other_element"):
        return to_base_response(epp_response)

    res_data: TrnDataType = epp_response.response.res_data.other_element[0]

    resData = TransferResponse(
        id=res_data.id,
        trStatus=res_data.tr_status,
        reId=res_data.re_id,
        reDate=res_data.re_date.to_datetime() if hasattr(res_data, "re_date") and res_data.re_date is not None else None,
        acID=res_data.ac_id,
        acDate=res_data.ac_date.to_datetime() if hasattr(res_data, "ac_date") and res_data.ac_date is not None else None,
        exDate=res_data.ex_date.to_datetime() if hasattr(res_data, "ex_date") and res_data.ex_date is not None else None
    )

    return BaseResponseModel(
        trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
                       svTRID=epp_response.response.tr_id.sv_trid),
        result=to_result_list(epp_response),
        resData=resData
    )