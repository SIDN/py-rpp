
from typing import List
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.rpp.common import DcpModel, DcpStatementModel, GreetingModel, SvcMenuModel
from rpp.model.rpp.message import MessageModel



def to_messages(message: Epp) -> MessageModel:

    code = message.response.result[0].code.value
    if code == 1000:
        return MessageModel(
            code=code,
            count= message.response.msg_q.count,
            clientId=message.response.tr_id.cl_trid,
            serverId=message.response.tr_id.sv_trid,
            data=str(message.response.res_data.other_element[0] if message.response.res_data.other_element else None),
        )

    return MessageModel(
            code=code,
            serverId=message.response.tr_id.sv_trid
        )