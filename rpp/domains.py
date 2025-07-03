import logging
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, Header, Response
from fastapi.params import Body
from rpp.common import add_check_header, add_status_header
from rpp.epp_connection_pool import get_connection
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.model.epp.domain_commands import domain_check, domain_delete, domain_info, domain_create
from rpp.model.rpp.entity import Card
from fastapi import APIRouter

from rpp.model.rpp.domain import DomainCheckRequest, DomainCreateRequest, DomainInfoRequest, DomainInfoResponse, NameserverModel, ContactModel
from rpp.model.rpp.domain_converter import to_domain_check, to_domain_delete, to_domain_info


logger = logging.getLogger('uvicorn.error')
router = APIRouter()

@router.post("/")
def do_create(domain: DomainCreateRequest, conn: EppClient = Depends(get_connection)):
    logger.info(f"Create new domain: {domain}")

    epp_request = domain_create(domain)
    return conn.send_command(epp_request)

@router.get("/{domain_name}", response_model_exclude_none=True)
def do_info(domain_name: str, response: Response,
             conn: EppClient = Depends(get_connection),
             optional_body: Optional[DomainInfoRequest] = Body(None)):
    
    logger.info(f"Fetching info for domain: {domain_name}")

    if optional_body is None:
        # No body was provided
        logger.info("No body")
    else:
        # Body was provided
        logger.info(f"Body received: {optional_body}")

    epp_request = domain_info(domain=domain_name)
    epp_response = conn.send_command(epp_request)

    return to_domain_info(epp_response, response)

@router.post("/{domain_name}", response_model_exclude_none=True)
def do_info(domain_name: str, response: Response,
             conn: EppClient = Depends(get_connection),
             body: DomainInfoRequest = Body(DomainInfoRequest)):
    
    logger.info(f"Fetching info for domain: {domain_name}")

    if body is None:
        # No body was provided
        logger.info("No body")
    else:
        # Body was provided
        logger.info(f"Body received: {body}")

    epp_request = domain_info(domain_name, body.authInfo)
    epp_response = conn.send_command(epp_request)

    return epp_response

@router.head("/{domain_name}")
def do_check(domain_name: str, response: Response,
             rpp_cl_trid: Annotated[str | None, Header()] = None,
             conn: EppClient = Depends(get_connection)):
    
    logger.info(f"Check domain: {domain_name}")
    
    epp_request = domain_check(DomainCheckRequest(name=domain_name, clTRID=rpp_cl_trid))
    epp_response = conn.send_command(epp_request)

    #return to_domain_check(epp_response, response)
    epp_status, avail, reason = to_domain_check(epp_response)

    add_status_header(response, str(epp_status))
    add_check_header(response, str(epp_status), avail, reason)

@router.delete("/{domain_name}", status_code=204)
def do_delete(domain_name: str, response: Response, conn: EppClient = Depends(get_connection)):
    logger.info(f"Delete domain: {domain_name}")
    
    epp_request = domain_delete(domain=domain_name)
    epp_response = conn.send_command(epp_request)

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




# Registry lock