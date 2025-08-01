import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response
from fastapi.params import Header
from rpp.common import RPP_CODE_HEADERS, RPP_PROBLEM_REPORT_SCHEMA, add_check_status, update_response
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from rpp.model.epp.host_commands import host_check, host_create, host_delete, host_info, host_update
from fastapi import APIRouter

from rpp.model.rpp.common import ProblemModel
from rpp.model.rpp.host import HostCreateRequest, HostCreateResponse, HostInfoResponse, HostUpdateRequest
from rpp.model.rpp.host_converter import to_host_check, to_host_create, to_host_delete, to_host_info, to_host_update

logger = logging.getLogger('uvicorn.error')
router = APIRouter()


@router.post("/", response_model_exclude_none=True, summary="Create Host", status_code=201,
             responses={201: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_create(create_request: HostCreateRequest,
              request: Request, 
              response: Response,
              rpp_cl_trid: Annotated[str | None, Header()] = None,
              conn: EppClient = Depends(get_connection)) -> HostCreateResponse | ProblemModel:
    logger.info(f"Create host: {create_request.name}")

    epp_request = host_create(create_request, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_host_create(epp_response)
    location = f"{request.url}/{rpp_response.name}" if isinstance(rpp_response, HostCreateResponse) else None
    return update_response(response, epp_response, 201, location, rpp_response)  # 201 Created


@router.get("/{host}", response_model_exclude_none=True, summary="Get Host Info",
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_info(host: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None
            ) -> HostInfoResponse | ProblemModel:

    logger.info(f"Info for host: {host}")

    epp_request = host_info(host, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_host_info(epp_response)
    return update_response(response, epp_response, 200, None, rpp_response)


@router.head("/{host}/availability", summary="Check Host Existence",
            status_code=200,
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_check_head(host: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None | ProblemModel:

    logger.info(f"Check for host: {host}")

    epp_request = host_check(host, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_host_check(epp_response)
    update_response(response, epp_response)
    # no response body, update http status
    add_check_status(response, rpp_response)

    # update_response(response, epp_response)
    # add_check_status(response, epp_status, avail, reason)

# @router.get("/{host}/availability", summary="Check Host Existence")
# async def do_check_get(host: str, 
#             response: Response,
#             conn: EppClient = Depends(get_connection),
#             rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

#     logger.info(f"Check for host: {host}")

@router.delete("/{host}", response_model_exclude_none=True, summary="Delete Host",
               status_code=204,
                responses={204: RPP_CODE_HEADERS,
                           422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_delete(host: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Delete host: {host}")

    epp_request = host_delete(host, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)
    rpp_response = to_host_delete(epp_response)
    return update_response(response, epp_response, 204, None, rpp_response)  # 204 No Content
    # delete has no response body, so we just set the status code
    #to_host_delete(epp_response)

@router.patch("/{host}", response_model_exclude_none=True, summary="Update Host",
                status_code=200,
                responses={200: RPP_CODE_HEADERS,
                           422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_update(host: str,
            response: Response,
            request: HostUpdateRequest,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> None | ProblemModel:

    logger.info(f"Update host: {host}")
    logger.info(f"Update request: {request}")

    epp_request = host_update(host, request, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_host_update(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_response)

@router.get("/{host}/processes/{proc_name}/{proc_id}", summary="List Processes",
            status_code=200,
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_list_processes(host: str,
                                proc_name: str,
                                proc_id: str,
                                response: Response,
                                rpp_cl_trid: Annotated[str | None, Header()] = None,
                                rpp_authorization: Annotated[str | None, Header()] = None,
                                conn: EppClient = Depends(get_connection)):

    logger.info(f"List {proc_name}/{proc_id} processes for host: {host}")

    #TODO: Implement the actual process listing logic