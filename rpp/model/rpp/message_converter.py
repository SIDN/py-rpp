
import logging
from rpp.model.epp.domain_1_0 import TrnData as DomainTrnData
from rpp.model.epp.contact_1_0 import TrnData
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.epp.sidn_ext_epp_1_0 import PollData
from rpp.model.rpp.common import BaseResponseModel, MessageQueueModel, TrIDModel
from rpp.model.rpp.common_converter import is_ok_response, to_base_response, to_result_list
from rpp.model.rpp.domain import TransferResponse

logger = logging.getLogger('uvicorn.error')

def to_messages(epp_response: Epp) -> BaseResponseModel:

    ok, epp_status, message = is_ok_response(epp_response)
    if not ok:
         return to_base_response(epp_response)

    #TODO: convert the EPP resData to RPP model
    resData = None
    message_queue = None
    if hasattr(epp_response.response, 'msg_q') and epp_response.response.msg_q is not None:
        message_queue = MessageQueueModel(
            count=epp_response.response.msg_q.count,
            id=epp_response.response.msg_q.id,
            qDate=epp_response.response.msg_q.q_date.to_datetime() if epp_response.response.msg_q.q_date else None,
            message=", ".join(str(item) for item in epp_response.response.msg_q.msg.content) if epp_response.response.msg_q.msg else None
        )

    if hasattr(epp_response.response, 'res_data') and epp_response.response.res_data is not None:
        # found object specific response data
        if epp_response.response.res_data.other_element and isinstance(epp_response.response.res_data.other_element[0], PollData):
            # found SIDN PollData extension
            logger.info(f"SIDN Polldata extension found")

            poll_data: PollData = epp_response.response.res_data.other_element[0]
            
            if poll_data.data.res_data.other_element and isinstance(poll_data.data.res_data.other_element[0], DomainTrnData):
                logger.info(f"Domain transfer data found in PollData")
                resData: DomainTrnData = poll_data.data.res_data.other_element[0]

                resData = TransferResponse(
                    name=resData.name,
                    trStatus=resData.tr_status,
                    reId=resData.re_id,
                    reDate=resData.re_date.to_datetime() if hasattr(resData, "re_date") and resData.re_date is not None else None,
                    acID=resData.ac_id,
                    acDate=resData.ac_date.to_datetime() if hasattr(resData, "ac_date") and resData.ac_date is not None else None,
                    exDate=resData.ex_date.to_datetime() if hasattr(resData, "ex_date") and resData.ex_date is not None else None
                )


    return BaseResponseModel(
        trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
        svTRID=epp_response.response.tr_id.sv_trid),
        result=to_result_list(epp_response),
        resData=resData,
        messages=message_queue
    )

def to_ack_response(epp_response: Epp) -> BaseResponseModel:
    return to_base_response(epp_response)
