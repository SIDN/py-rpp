import logging
from fastapi import APIRouter, Depends, Request, Cookie, Cookie, Response
from rpp.common import add_status_header
from rpp.epp_connection_pool import get_connection
from rpp.model.config import Config
from rpp.epp_client import EppClient

from rpp.model.epp.domain_commands import domain_info
from rpp.model.epp.contact_commands import contact_create, contact_info
from rpp.model.rpp.entity import ContactCreateRequest, ContactInfoResponse
from rpp.model.rpp.entity_converter import to_contact_info

logger = logging.getLogger('uvicorn.error')
from fastapi import APIRouter

router = APIRouter()

@router.post("/", description="Create a new entity", summary="Create Entity")
def do_create(request: Request, createRequest: ContactCreateRequest, conn: EppClient = Depends(get_connection)):
    logger.info(f"Create new contact: {createRequest.model_dump_json()}")

    epp_request = contact_create(createRequest)
    epp_response = conn.send_command(epp_request)
 
    logger.info(f"Contact create response: {epp_response}")
    return epp_response


@router.get("/{entity_id}", response_model=ContactInfoResponse, response_model_exclude_none=True)
def do_info(entity_id: str, response: Response, conn: EppClient = Depends(get_connection)):
    logger.info(f"Fetching info for contact: {entity_id}")

    epp_request = contact_info(contact_handle=entity_id)
    epp_response = conn.send_command(epp_request)

    rpp_response = to_contact_info(epp_response)
    add_status_header(response, epp_response)
    return rpp_response