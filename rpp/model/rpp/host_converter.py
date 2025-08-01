from fastapi import Response
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.epp.host_1_0 import CheckType, ChkDataType, CreDataType, InfData
from rpp.model.rpp.common import ProblemModel
from rpp.model.rpp.common_converter import is_ok_response, to_error_response
from rpp.model.rpp.host import HostCheckResponse, HostCreateResponse, HostInfoResponse, HostEventModel, HostAddr
from typing import Dict

def to_host_create(epp_response: Epp) -> HostCreateResponse | ProblemModel:
    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
         return to_error_response(epp_response)

    epp_host_res: CreDataType = epp_response.response.res_data.other_element[0];
    return HostCreateResponse(name=epp_host_res.name,
            createDate=str(epp_host_res.cr_date) if epp_host_res.cr_date else None)
    # return BaseResponseModel(
    #     type_="Host",
    #     trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
    #     svTRID=epp_response.response.tr_id.sv_trid),
    #     result=to_result_list(epp_response),
    #     resData=HostCreateResponse(name=epp_host_res.name,
    #         createDate=str(epp_host_res.cr_date) if epp_host_res.cr_date else None)
    #)

def to_host_delete(epp_response: Epp) -> None | ProblemModel:
    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
        return to_error_response(epp_response)

    return None

def to_host_info(epp_response) -> HostInfoResponse | ProblemModel:

    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
        return to_error_response(epp_response)
    
    res_data: InfData = epp_response.response.res_data.other_element[0]

    # Status
    status = [s.s for s in getattr(res_data, "status", [])]

    # Events (e.g. create, update, etc.)
    events: Dict[str, HostEventModel] = {}
    if hasattr(res_data, "cr_id") and res_data.cr_id is not None:
        events["Create"] = HostEventModel(name=res_data.cr_id, date=str(res_data.cr_date))

    if hasattr(res_data, "up_id") and res_data.up_id is not None:
        events["Update"] = HostEventModel(name=res_data.up_id, date=str(res_data.up_date))

    # Addresses
    #ips = { "v4": [], "v6": [] }
    addresses = []
    if hasattr(res_data, "addr"):
        for addr in res_data.addr:
            if addr.ip.value == "v4":
                addresses.append(HostAddr(address=addr.value, family="v4"))
            elif addr.ip.value == "v6":
                addresses.append(HostAddr(address=addr.value, family="v6"))

    # addresses = HostAddr(
    #     v4=ips["v4"] if ips["v4"] else [],
    #     v6=ips["v6"] if ips["v6"] else []
    # )

    return HostInfoResponse(
        name=res_data.name,
        roid=res_data.roid,
        status=status,
        registrar=getattr(res_data, "cl_id", ""),
        events=events,
        addr=addresses if addresses else None
    )

    # return BaseResponseModel(
    #     type_="Host",
    #     trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
    #     svTRID=epp_response.response.tr_id.sv_trid),
    #     result=to_result_list(epp_response),
    #     resData=infData
    # )

def to_host_check(epp_response: Epp) -> HostCheckResponse | ProblemModel:

    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
         return None, epp_status, message
    
    check_data: ChkDataType = epp_response.response.res_data.other_element[0]
    cd: CheckType = check_data.cd[0]

    return HostCheckResponse(name=cd.name.value, avail=cd.name.avail, reason=cd.reason.value if cd.reason else None)

def to_host_update(epp_response: Epp) -> None | ProblemModel:
    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
        return to_error_response(epp_response)

    return None