import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Header, Request, Cookie, Cookie, Response
from rpp.common import add_check_header, add_status_header
from rpp.epp_connection_pool import get_connection
from rpp.model.config import Config
from rpp.epp_client import EppClient

from rpp.model.epp.domain_commands import domain_info
from rpp.model.epp.contact_commands import contact_check, contact_create, contact_info
from rpp.model.rpp.common_converter import is_ok_code
from rpp.model.rpp.entity import ContactCheckRequest, ContactCreateRequest, ContactInfoResponse
from rpp.model.rpp.entity_converter import to_contact_check, to_contact_info
from fastapi import APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials

logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()

router = APIRouter(dependencies=[Depends(security)])

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

@router.head("/{entity_id}")
def do_check(entity_id: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Check for contact: {entity_id}")

    rpp_request = ContactCheckRequest(name=entity_id, clTRID=rpp_cl_trid)
    epp_request = contact_check(rpp_request)
    epp_response = conn.send_command(epp_request)

    avail, epp_status, reason = to_contact_check(epp_response)

    add_status_header(response, epp_status)
    if is_ok_code(epp_status):
        add_check_header(response, avail, reason)