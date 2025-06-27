import logging
from fastapi import APIRouter, Depends, Request, Cookie, Cookie, Response
from rpp.epp_connection_pool import get_connection
from rpp.model.config import Config
from rpp.epp_client import EppClient

from rpp.model.epp.domain_commands import domain_info
from rpp.model.epp.contact_commands import contact_create, contact_info
from rpp.model.rpp.contact import Card
from rpp.model.rpp.contact_converter import to_contact_info

logger = logging.getLogger('uvicorn.error')
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def do_create(request: Request, card: Card, conn: EppClient = Depends(get_connection)):
    logger.info(f"Create new contact: {card.model_dump_json()}")

    epp_request = contact_create(card)
    epp_response = conn.send_command(epp_request)
 
    logger.info(f"Contact create response: {epp_response}")
    return epp_response


@router.get("/{contact_handle}", response_model=Card, response_model_exclude_none=True)
def do_info(contact_handle: str, conn: EppClient = Depends(get_connection)):
    logger.info(f"Fetching info for contact: {contact_handle}")

    epp_request = contact_info(contact_handle=contact_handle)
    epp_response = conn.send_command(epp_request)

    return to_contact_info(epp_response)