
from rpp.model.epp.epp_1_0 import (
    CommandType,
    Epp,
    PollOpType,
    PollType
)
from rpp.model.rpp.message import MessageRequest


def get_messages(request: MessageRequest)-> Epp:
    epp_request = Epp(
        command=CommandType(
            poll=PollType(op=PollOpType.REQ),
            cl_trid=request.clTRID if request.clTRID else None
        )
    )

    return epp_request

def ack_message(request: MessageRequest)-> Epp:
    epp_request = Epp(
        command=CommandType(
            poll=PollType(op=PollOpType.ACK, msg_id=request.id),
            cl_trid=request.clTRID
        )
    )

    return epp_request