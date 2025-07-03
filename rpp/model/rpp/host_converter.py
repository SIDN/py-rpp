from fastapi import Response
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.epp.host_1_0 import CheckType, ChkData, ChkDataType, CreDataType
from rpp.model.rpp.common import BaseResponseModel, ResultModel, TrIDModel
from rpp.model.rpp.common_converter import is_ok_response, to_base_response, to_result_list
from rpp.model.rpp.host import HostCheckResModel, HostCreateResDataModel, HostInfoResponseModel, HostEventModel, HostAddr
from typing import Dict

def to_host_create(epp_response: Epp) -> BaseResponseModel:
    
    # first_result = epp_response.response.result[0]
    # result = ResultModel(code=first_result.code.value, message=first_result.msg.value,
    #             lang=first_result.msg.lang if first_result.msg.lang else None)
    
    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
         return to_base_response(epp_response)
    
    # if first_result.code.value != 1000:
    #     return to_base_response(epp_response)
        # return BaseResponseModel(
        #     trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
        #     svTRID=epp_response.response.tr_id.sv_trid),
        #     result=[result])

    epp_host_res: CreDataType = epp_response.response.res_data.other_element[0];
   
    return BaseResponseModel(
        trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
        svTRID=epp_response.response.tr_id.sv_trid),
        result=to_result_list(epp_response),
        resData=HostCreateResDataModel(name=epp_host_res.name,
            createDate=str(epp_host_res.cr_date) if epp_host_res.cr_date else None)
    )

def to_host_delete(epp_response: Epp) -> BaseResponseModel:
    return to_base_response(epp_response)
    # results: List[ResultModel] = []
    # for res in epp_response.response.result:
    #     results.append(ResultModel(code=res.code.value, message=res.msg.value,
    #             lang=res.msg.lang if res.msg.lang else None))

    # return BaseResponseModel(
    #     trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
    #     svTRID=epp_response.response.tr_id.sv_trid),
    #     result=results)


def to_host_info(epp_response):

    epp_status = epp_response.response.result[0].code.value
    if epp_status != 1000:
        return to_base_response(epp_response)
    
    res_data = epp_response.response.res_data.other_element[0]

    # Status
    status = [s.s for s in getattr(res_data, "status", [])]

    # Events (e.g. create, update, etc.)
    events: Dict[str, HostEventModel] = {}
    if hasattr(res_data, "cr_id") and res_data.cr_id is not None:
        events["Create"] = HostEventModel(name=res_data.cr_id, date=str(res_data.cr_date))

    if hasattr(res_data, "up_id") and res_data.up_id is not None:
        events["Update"] = HostEventModel(name=res_data.up_id, date=str(res_data.up_date))

    # Addresses
    v4 = []
    v6 = []
    if hasattr(res_data, "addr"):
        for addr in res_data.addr:
            if addr.ip.value == "v4":
                v4.append(addr.value)
            elif addr.ip.value == "v6":
                v6.append(addr.value)
    addresses = HostAddr(
        v4=v4 if v4 else None,
        v6=v6 if v6 else None
    )

    return HostInfoResponseModel(
        name=res_data.name,
        roid=res_data.roid,
        status=status,
        registrar=getattr(res_data, "cl_id", ""),
        events=events,
        addresses=addresses
    )

def to_host_check(epp_response: Epp) -> tuple[bool, int, str]:

    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
         return None, epp_status, message
    
    check_data: ChkDataType = epp_response.response.res_data.other_element[0]
    cd: CheckType = check_data.cd[0]

    return cd.name.avail, epp_status, cd.reason.value if cd.reason else None

    # checkResponse = HostCheckResModel(
    #     name=cd.name.value,
    #     available=cd.name.avail,
    #     reason=cd.reason.value if cd.reason else None,
    #     lang=cd.reason.lang if cd.reason else None
    # )

    # return BaseResponseModel(
    #     trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
    #     svTRID=epp_response.response.tr_id.sv_trid),
    #     result=to_result_list(epp_response),
    #     resData=checkResponse
    # )

def to_host_update(epp_response: Epp) -> BaseResponseModel:
    return to_base_response(epp_response)