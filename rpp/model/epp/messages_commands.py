
from rpp.model.epp.epp_1_0 import (
    CommandType,
    Epp,
    PollOpType,
    PollType
)


def get_messages()-> Epp:
    epp_request = Epp(
        command=CommandType(
            poll=PollType(op=PollOpType.REQ)
        )
    )

    return epp_request
