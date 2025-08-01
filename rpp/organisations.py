import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response
from fastapi.params import Body, Header
from rpp.common import RPP_CODE_HEADERS, RPP_PROBLEM_REPORT_SCHEMA, add_check_status, epp_auth_info_from_header, update_response
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from fastapi import APIRouter

from rpp.model.rpp.common import AuthInfoModel, ProblemModel

from rpp.model.rpp.organisation import OrganisationCheckRequest, OrganisationCreateRequest, OrganisationCreateResponse, OrganisationDeleteRequest, OrganisationInfoRequest, OrganisationInfoResponse, OrganisationUpdateRequest
from rpp.model.rpp.organisation_converter import to_organisation_check, to_organisation_create, to_organisation_delete, to_organisation_info, to_organisation_update

logger = logging.getLogger('uvicorn.error')
router = APIRouter()


@router.post("/", response_model_exclude_none=True, summary="Create Organisation",
             status_code=201,
             responses={201: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_create(create_request: OrganisationCreateRequest,
              response: Response,
              request: Request,
              rpp_cl_trid: Annotated[str | None, Header()] = None,
              conn: EppClient = Depends(get_connection)) -> None | ProblemModel:

    logger.info(f"Create organisation: {create_request.id}")

    epp_request = None  # Replace with actual EPP request for organisation creation
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_organisation_create(epp_response)
    location = f"{request.url}/{rpp_response.id}" if isinstance(rpp_response, OrganisationCreateResponse) else None
    return update_response(response, epp_response, 201, location, rpp_response)


@router.get("/{organisation}", response_model_exclude_none=True, summary="Get Organisation Info",
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_info(organisation: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> OrganisationInfoResponse | ProblemModel:

    logger.info(f"Info for organisation: {organisation}")

    rpp_request = OrganisationInfoRequest(id=organisation, clTRID=rpp_cl_trid, authInfo=epp_authorization)
    epp_request = None  # Replace with actual EPP request for organisation info
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_organisation_info(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_response)


@router.head("/{organisation}/availability", summary="Check Organisation Availability",
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_check_head(organisation: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None | ProblemModel:

    logger.info(f"Check for organisation: {organisation}")

    rpp_request = OrganisationCheckRequest(id=organisation, clTRID=rpp_cl_trid)
    epp_request = None  # Replace with actual EPP request for organisation info
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_organisation_check(epp_response)
    update_response(response, epp_response)
    # no response body, update http status
    add_check_status(response, rpp_response)

# @router.get("/{organisation}/availability", summary="Check Organisation Availability")
# async def do_check_get(organisation: str,
#             response: Response,
#             conn: EppClient = Depends(get_connection),
#             rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

#     logger.info(f"Check for organisation: {organisation}")

@router.delete("/{organisation}", response_model_exclude_none=True, summary="Delete Organisation",
               responses={204: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_delete(organisation: str,
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None,) -> None | ProblemModel:

    logger.info(f"Delete organisation: {organisation}")

    rpp_request = OrganisationDeleteRequest(id=organisation, clTRID=rpp_cl_trid)
    epp_request = None  # Replace with actual EPP request for organisation deletion
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_organisation_delete(epp_response)
    return update_response(response, epp_response, 204, rpp_response) # 204 No Content
    # delete has no response body, so we just set the status code
    

@router.patch("/{organisation}", response_model_exclude_none=True, summary="Update Organisation",
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_update(organisation: str,
            response: Response,
            request: OrganisationUpdateRequest,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> None | ProblemModel:

    logger.info(f"Update organisation: {organisation}")
    logger.info(f"Update request: {request}")

    epp_request = None # Replace with actual EPP request for organisation update
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_organisation_update(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_response)
