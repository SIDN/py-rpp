import logging
from fastapi import APIRouter, Depends
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from rpp.model.epp.host_commands import host_create, host_info
from fastapi import APIRouter

from rpp.model.rpp.host import HostCreateRequest, HostModel
from rpp.model.rpp.host_converter import to_host_info
logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.post("/")
def do_create(host: HostCreateRequest, conn: EppClient = Depends(get_connection)):
    logger.info(f"Create new host: {host}")

    epp_request = host_create(host)
    return conn.send_command(epp_request)

@router.get("/{host}", response_model=HostModel, response_model_exclude_none=True)
def do_info(host: str, conn: EppClient = Depends(get_connection)):
    logger.info(f"Fetching info for host: {host}")

    epp_request = host_info(host=host)
    epp_response = conn.send_command(epp_request)

    return to_host_info(epp_response)