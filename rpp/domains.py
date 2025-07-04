import logging
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, Header, Response
from fastapi.params import Body
from rpp.common import add_check_header, add_status_header
from rpp.epp_connection_pool import get_connection
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.model.epp.domain_commands import domain_check, domain_delete, domain_info, domain_create
from rpp.model.rpp.common import BaseResponseModel
from rpp.model.rpp.common_converter import get_status_from_response, is_ok_code
from rpp.model.rpp.entity import Card
from fastapi import APIRouter

from rpp.model.rpp.domain import DomainCheckRequest, DomainCreateRequest, DomainInfoRequest, DomainInfoResponse, NameserverModel, ContactModel
from rpp.model.rpp.domain_converter import to_domain_check, to_domain_create, to_domain_delete, to_domain_info
from fastapi import APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials

logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()

router = APIRouter(dependencies=[Depends(security)])


@router.post("/", description="Create a new domain", summary="Create Domain",
             response_model=BaseResponseModel, response_model_exclude_none=True)
def do_create(create_request: DomainCreateRequest, 
              response: Response,
              conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    logger.info(f"Create new domain: {create_request.name}")

    epp_request = domain_create(create_request)
    epp_response = conn.send_command(epp_request)
    add_status_header(response, get_status_from_response(epp_response))
    return to_domain_create(epp_response)

@router.get("/{domain_name}", response_model_exclude_none=True)
def do_info(domain_name: str, response: Response,
             conn: EppClient = Depends(get_connection),
             rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:
    
    logger.info(f"Fetching info for domain: {domain_name}")

    epp_request = domain_info(DomainInfoRequest(name=domain_name, clTRID=rpp_cl_trid))
    epp_response = conn.send_command(epp_request)

    add_status_header(response, get_status_from_response(epp_response))
    return to_domain_info(epp_response, response)

@router.post("/{domain_name}", response_model_exclude_none=True)
def do_info(domain_name: str, response: Response,
             conn: EppClient = Depends(get_connection),
             body: DomainInfoRequest = Body(DomainInfoRequest)) -> BaseResponseModel:
    
    logger.info(f"Fetching info for domain: {domain_name}")

    if body is None:
        # No body was provided
        logger.info("No body")
    else:
        # Body was provided
        logger.info(f"Body received: {body}")

    epp_request = domain_info(domain_name, body.authInfo)
    epp_response = conn.send_command(epp_request)

    add_status_header(response, get_status_from_response(epp_response))
    return epp_response

@router.head("/{domain_name}")
def do_check(domain_name: str, response: Response,
             rpp_cl_trid: Annotated[str | None, Header()] = None,
             conn: EppClient = Depends(get_connection)):
    
    logger.info(f"Check domain: {domain_name}")
    
    epp_request = domain_check(DomainCheckRequest(name=domain_name, clTRID=rpp_cl_trid))
    epp_response = conn.send_command(epp_request)

    #return to_domain_check(epp_response, response)
    avail, epp_status, reason = to_domain_check(epp_response)

    add_status_header(response, epp_status)
    if is_ok_code(epp_status):
        add_check_header(response, avail, reason)

@router.delete("/{domain_name}", status_code=204)
def do_delete(domain_name: str, response: Response, conn: EppClient = Depends(get_connection)):
    logger.info(f"Delete domain: {domain_name}")
    
    epp_request = domain_delete(domain=domain_name)
    epp_response = conn.send_command(epp_request)

    add_status_header(response, get_status_from_response(epp_response))
    # delete has no response body, so we just set the status code
    to_domain_delete(epp_response, response)


@router.patch("/{domain_name}")
def do_update(domain_name: str, response: Response, conn: EppClient = Depends(get_connection)):
    pass


@router.post("/{domain_name}/renewals")
def do_renew(domain_name: str, response: Response, conn: EppClient = Depends(get_connection)):
    pass

@router.post("/{domain_name}/transfers")
def do_start_transfer(domain_name: str, response: Response, conn: EppClient = Depends(get_connection)):
    pass

@router.get("/{domain_name}/transfers")
def do_query_transfer(domain_name: str, response: Response, conn: EppClient = Depends(get_connection)):
    pass

@router.delete("/{domain_name}/transfers")
def do_stop_transfer(domain_name: str, response: Response, conn: EppClient = Depends(get_connection)):
    """Stop a transfer for the specified domain.
    Do reject transfer request when the requestor is the current sponsoring registrar.
    Do cancel transfer request when the requestor is not the new sponsoring registrar.
    """
    pass

@router.put("/{domain_name}/transfers")
def do_approve_transfer(domain_name: str, response: Response, conn: EppClient = Depends(get_connection)):
    pass




# TODO: add support for Registry lock