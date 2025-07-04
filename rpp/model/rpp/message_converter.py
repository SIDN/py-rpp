
from typing import List
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.rpp.common import BaseResponseModel, DcpModel, DcpStatementModel, GreetingModel, SvcMenuModel, TrIDModel
from rpp.model.rpp.common_converter import is_ok_response, to_base_response, to_result_list



def to_messages(epp_response: Epp) -> BaseResponseModel:

    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
         return to_base_response(epp_response)

    #TODO: convert the EPP resData to RPP model
    resData = None

    # = MessageModel(
    #         code=code,
    #         count= message.response.msg_q.count,
    #         clientId=message.response.tr_id.cl_trid,
    #         serverId=message.response.tr_id.sv_trid,
    #         data=str(message.response.res_data.other_element[0] if message.response.res_data.other_element else None),
    #     )

    # return MessageModel(
    #         code=code,
    #         serverId=message.response.tr_id.sv_trid
    #     )

    return BaseResponseModel(
        trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
        svTRID=epp_response.response.tr_id.sv_trid),
        result=to_result_list(epp_response),
        resData=resData
    )

def to_ack_response(epp_response: Epp) -> BaseResponseModel:
    return to_base_response(epp_response)
