import logging
from fastapi import APIRouter, Depends, Response
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.epp_connection_pool import get_connection
from rpp.model.epp.messages_commands import get_messages
from rpp.model.rpp.message import MessageModel
from rpp.model.rpp.message_converter import to_messages


logger = logging.getLogger('uvicorn.error')
router = APIRouter()

@router.get("/", response_model=MessageModel, response_model_exclude_none=True)
def do_get_messages(response: Response, conn: EppClient = Depends(get_connection)) -> MessageModel:
    logger.info("Fetch message")

    epp_request = get_messages()
    epp_response = conn.send_command(epp_request)
    return to_messages(epp_response)


@router.delete("/{message_id}", response_model=MessageModel, response_model_exclude_none=True)
def do_delete_message(message_id: str, response: Response, conn: EppClient = Depends(get_connection)) -> MessageModel:
    logger.info(f"Deleting message with ID: {message_id}")

    epp_request = get_messages()
    epp_response = conn.send_command(epp_request)
    return to_messages(epp_response)
