import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.params import Body, Header
from rpp.common import add_check_status, auth_info_from_header, update_response, update_response_from_code
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from rpp.model.epp.host_commands import host_check, host_create, host_delete, host_info, host_update
from fastapi import APIRouter

from rpp.model.rpp.common import BaseResponseModel
from rpp.model.rpp.host import HostCheckRequest, HostCreateRequest, HostDeleteRequest, HostInfoRequest, HostUpdateRequest
from rpp.model.rpp.host_converter import do_host_check, to_host_create, to_host_delete, to_host_info, to_host_update
from fastapi.security import HTTPBasic

logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()
router = APIRouter(dependencies=[Depends(security)])


@router.post("/", response_model=BaseResponseModel, response_model_exclude_none=True, summary="Create Host")
async def do_create(create_request: HostCreateRequest,
              response: Response,
              conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    logger.info(f"Create host: {create_request.name}")

    epp_request = host_create(create_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response, 201)  # 201 Created
    return to_host_create(epp_response)


@router.get("/{host}", response_model_exclude_none=True, summary="Get Host Info")
async def do_info(host: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:

    logger.info(f"Info for host: {host}")

    rpp_request = HostInfoRequest(name=host, clTRID=rpp_cl_trid)
    epp_request = host_info(rpp_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_host_info(epp_response)

@router.head("/{host}/availability", summary="Check Host Existence")
async def do_check_head(host: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Check for host: {host}")

    rpp_request = HostCheckRequest(name=host, clTRID=rpp_cl_trid)
    epp_request = host_check(rpp_request)
    epp_response = await conn.send_command(epp_request)

    avail, epp_status, reason = do_host_check(epp_response)

    add_check_status(response, epp_status, avail, reason)

@router.get("/{host}/availability", summary="Check Host Existence")
async def do_check_get(host: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Check for host: {host}")

@router.delete("/{host}", response_model_exclude_none=True, status_code=204, summary="Delete Host")
async def do_delete(host: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None,) -> None:

    logger.info(f"Delete host: {host}")

    rpp_request = HostDeleteRequest(name=host, clTRID=rpp_cl_trid)
    epp_request = host_delete(rpp_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response, 204) # 204 No Content
    # delete has no response body, so we just set the status code
    to_host_delete(epp_response)

@router.patch("/{host}", response_model=BaseResponseModel, response_model_exclude_none=True, summary="Update Host")
async def do_update(host: str,
            response: Response,
            request: HostUpdateRequest,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Update host: {host}")
    logger.info(f"Update request: {request}")

    epp_request = host_update(request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_host_update(epp_response)

@router.post("/{host}/renewal", status_code=501, summary="Renew Host (Not Implemented)")
async def do_renew(host: str, response: Response) -> None:

    logger.info(f"Renew host: {host}")
    update_response_from_code(response, 2101) # Not implemented