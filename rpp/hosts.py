import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.params import Header
from rpp.common import add_check_header, add_status_header
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from rpp.model.epp.host_commands import host_check, host_create, host_delete, host_info, host_update
from fastapi import APIRouter

from rpp.model.rpp.common import BaseResponseModel
from rpp.model.rpp.common_converter import get_status_from_response, is_ok_code
from rpp.model.rpp.host import HostCheckRequest, HostCheckResModel, HostCreateRequest, HostDeleteRequest, HostInfoRequest, HostInfoResponseModel, HostUpdateRequest
from rpp.model.rpp.host_converter import to_host_check, to_host_create, to_host_delete, to_host_info, to_host_update
logger = logging.getLogger('uvicorn.error')
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

router = APIRouter(dependencies=[Depends(security)])


@router.post("/", response_model=BaseResponseModel, response_model_exclude_none=True)
def do_create(create_request: HostCreateRequest,
              response: Response,
              conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    logger.info(f"Create host: {create_request.name}")

    epp_request = host_create(create_request)
    epp_response = conn.send_command(epp_request)

    add_status_header(response, get_status_from_response(epp_response))
    return to_host_create(epp_response)


@router.get("/{host}", response_model_exclude_none=True)
def do_info(host: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:

    logger.info(f"Info for host: {host}")

    rpp_request = HostInfoRequest(name=host, clTRID=rpp_cl_trid)
    epp_request = host_info(rpp_request)
    epp_response = conn.send_command(epp_request)

    add_status_header(response, get_status_from_response(epp_response))
    return to_host_info(epp_response)

@router.head("/{host}")
def do_info(host: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Check for host: {host}")

    rpp_request = HostCheckRequest(name=host, clTRID=rpp_cl_trid)
    epp_request = host_check(rpp_request)
    epp_response = conn.send_command(epp_request)

    avail, epp_status, reason = to_host_check(epp_response)

    add_status_header(response, epp_status)
    if is_ok_code(epp_status):
         add_check_header(response, avail, reason)

@router.delete("/{host}", response_model_exclude_none=True, status_code=204)
def do_delete(host: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Delete host: {host}")

    rpp_request = HostDeleteRequest(name=host, clTRID=rpp_cl_trid)
    epp_request = host_delete(rpp_request)
    epp_response = conn.send_command(epp_request)

    add_status_header(response, get_status_from_response(epp_response))
    # delete has no response body, so we just set the status code
    to_host_delete(epp_response)

@router.put("/{host}", response_model=BaseResponseModel, response_model_exclude_none=True)
def do_update(host: str,
            response: Response,
            request: HostUpdateRequest,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Update host: {host}")
    logger.info(f"Update request: {request}")

    epp_request = host_update(request)
    epp_response = conn.send_command(epp_request)

    add_status_header(response, get_status_from_response(epp_response))
    return to_host_update(epp_response)