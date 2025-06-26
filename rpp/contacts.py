import logging
from fastapi import APIRouter, Depends, Request, Cookie, Cookie, Response
from rpp.epp_connection_pool import get_connection
from rpp.model.config import Config
from rpp.epp_client import EppClient

from rpp.model.epp.domain_commands import domain_info
from rpp.model.epp.contact_commands import contact_create
from rpp.model.rpp.contact import Card

logger = logging.getLogger('uvicorn.error')
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def do_contact_create(request: Request, card: Card, conn: EppClient = Depends(get_connection)):
    logger.info(f"Create new contact: {card.model_dump_json()}")

    epp_request = contact_create(card)
    epp_response = conn.send_command(epp_request)
 
    logger.info(f"Contact create response: {epp_response}")
    return epp_response