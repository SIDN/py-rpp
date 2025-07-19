import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.params import Body, Header
from rpp.common import add_check_status, auth_info_from_header, update_response
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from fastapi import APIRouter

from rpp.model.rpp.common import BaseResponseModel
from rpp.model.rpp.common_converter import is_ok_code
from fastapi.security import HTTPBasic

from rpp.model.rpp.organisation import OrganisationCheckRequest, OrganisationCreateRequest, OrganisationDeleteRequest, OrganisationInfoRequest, OrganisationUpdateRequest
from rpp.model.rpp.organisation_converter import to_organisation_check, to_organisation_create, to_organisation_delete, to_organisation_info, to_organisation_update

logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()
router = APIRouter(dependencies=[Depends(security)])


@router.post("/", response_model=BaseResponseModel, response_model_exclude_none=True, summary="Create Organisation")
async def do_create(create_request: OrganisationCreateRequest,
              response: Response,
              conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    logger.info(f"Create organisation: {create_request.id}")

    epp_request = None  # Replace with actual EPP request for organisation creation
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response, 201)  # 201 Created
    return to_organisation_create(epp_response)


@router.get("/{organisation}", response_model_exclude_none=True, summary="Get Organisation Info")
async def do_info(organisation: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_authorization: Annotated[str | None, Header()] = None,
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:

    logger.info(f"Info for organisation: {organisation}")

    auth_info = auth_info_from_header(rpp_authorization)
    rpp_request = OrganisationInfoRequest(id=organisation, clTRID=rpp_cl_trid, authInfo=auth_info)
    epp_request = None  # Replace with actual EPP request for organisation info
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_organisation_info(epp_response)

@router.head("/{organisation}/availability", summary="Check Organisation Existence")
async def do_check_head(organisation: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Check for organisation: {organisation}")

    rpp_request = OrganisationCheckRequest(id=organisation, clTRID=rpp_cl_trid)
    epp_request = None  # Replace with actual EPP request for organisation info
    epp_response = await conn.send_command(epp_request)

    avail, epp_status, reason = to_organisation_check(epp_response)

    add_check_status(response, epp_status, avail, reason)

@router.head("/{organisation}/availability", summary="Check Organisation Existence")
async def do_check_get(organisation: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Check for organisation: {organisation}")

@router.delete("/{organisation}", response_model_exclude_none=True, status_code=204, summary="Delete Organisation")
async def do_delete(organisation: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None,) -> None:

    logger.info(f"Delete organisation: {organisation}")

    rpp_request = OrganisationDeleteRequest(id=organisation, clTRID=rpp_cl_trid)
    epp_request = None  # Replace with actual EPP request for organisation deletion
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response, 204) # 204 No Content
    # delete has no response body, so we just set the status code
    to_organisation_delete(epp_response)

@router.patch("/{organisation}", response_model=BaseResponseModel, response_model_exclude_none=True, summary="Update Organisation")
async def do_update(organisation: str,
            response: Response,
            request: OrganisationUpdateRequest,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Update organisation: {organisation}")
    logger.info(f"Update request: {request}")

    epp_request = None # Replace with actual EPP request for organisation update
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_organisation_update(epp_response)

