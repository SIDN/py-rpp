
from rpp.model.epp.epp_1_0 import (
    CommandType,
    Epp,
    PollOpType,
    PollType
)
from rpp.model.epp.helpers import random_tr_id


def get_messages(clTRID: str) -> Epp:
    epp_request = Epp(
        command=CommandType(
            poll=PollType(op=PollOpType.REQ),
            cl_trid=clTRID or random_tr_id(),
        )
    )

    return epp_request

def ack_message(clTRID: str, msg_id: int) -> Epp:
    epp_request = Epp(
        command=CommandType(
            poll=PollType(op=PollOpType.ACK, msg_id=msg_id),
            cl_trid=clTRID or random_tr_id(),
        )
    )

    return epp_request