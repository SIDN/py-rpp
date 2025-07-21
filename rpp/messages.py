import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Header, Response
from fastapi.security import HTTPBasic
from rpp.common import RPP_CODE_HEADERS, update_response
from rpp.epp_client import EppClient
from rpp.epp_connection_pool import get_connection
from rpp.model.epp.messages_converter import ack_message, get_messages
from rpp.model.rpp.common import BaseResponseModel
from rpp.model.rpp.message_converter import to_ack_response, to_messages


logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()
router = APIRouter(dependencies=[Depends(security)])

@router.get("/", response_model_exclude_none=True, summary="Get Messages",
                status_code=200,
                responses={200: RPP_CODE_HEADERS})
def do_get_messages(response: Response, 
                    conn: EppClient = Depends(get_connection),
                    rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:
    logger.info("Fetch message")

    epp_request = get_messages(rpp_cl_trid)
    epp_response = conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_messages(epp_response)


@router.delete("/{message_id}", response_model_exclude_none=True, summary="Delete Message",
                status_code=204,
                responses={204: RPP_CODE_HEADERS})
def do_delete_message(message_id: int, 
                      response: Response, 
                      conn: EppClient = Depends(get_connection),
                      rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:
    logger.info(f"Deleting message with ID: {message_id}")

    epp_request = ack_message(rpp_cl_trid, message_id)
    epp_response = conn.send_command(epp_request)

    update_response(response, epp_response)
    # delete has no response body, so we just set the status code
    to_ack_response(epp_response)
