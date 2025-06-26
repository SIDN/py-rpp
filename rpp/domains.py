import logging
from fastapi import APIRouter, Depends, Response
from rpp.epp_connection_pool import get_connection
from rpp.model.config import Config
from rpp.epp_client import EppClient
from rpp.model.epp.domain_commands import domain_info, domain_create
from rpp.model.rpp.contact import Card
from fastapi import APIRouter

from rpp.model.rpp.domain import DomainCreateRequest, DomainInfoResponse, NameserverModel, ContactModel
from rpp.model.rpp.domain_converter import to_domain_info


logger = logging.getLogger('uvicorn.error')
router = APIRouter()

@router.post("/")
def do_create(domain: DomainCreateRequest, conn: EppClient = Depends(get_connection)):
    logger.info(f"Create new domain: {domain}")

    epp_request = domain_create(domain)
    return conn.send_command(epp_request)

@router.get("/{domain_name}", response_model=DomainInfoResponse, response_model_exclude_none=True)
def do_domain_info(domain_name: str, conn: EppClient = Depends(get_connection)):
    logger.info(f"Fetching info for domain: {domain_name}")

    epp_request = domain_info(domain=domain_name)
    epp_response = conn.send_command(epp_request)

    return to_domain_info(epp_response)
