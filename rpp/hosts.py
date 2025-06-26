import logging
from fastapi import APIRouter, Depends
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from rpp.model.epp.host_commands import host_create
from fastapi import APIRouter

from rpp.model.rpp.host import Host
logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.post("/")
def do_create(host: Host, conn: EppClient = Depends(get_connection)):
    logger.info(f"Create new host: {host}")

    epp_request = host_create(host)
    return conn.send_command(epp_request)
