import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Header, Request, Response
from rpp.common import RPP_CODE_HEADERS, RPP_PROBLEM_REPORT_SCHEMA, add_check_status, epp_auth_info_from_header, update_response
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient

from rpp.model.epp.contact_converter import contact_check, contact_create, contact_delete, contact_info, contact_transfer, contact_transfer_query, contact_update
from rpp.model.epp.epp_1_0 import TransferOpType
from rpp.model.rpp.common import AuthInfoModel, ProblemModel
from rpp.model.rpp.entity import EntityCreateRequest, EntityCreateResponseModel, EntityInfoResponse, EntityTransferResponse, EntityUpdateRequest
from rpp.model.rpp.entity_converter import do_entity_check, to_entity_create, to_entity_delete, to_entity_info, to_entity_transfer, to_entity_update


logger = logging.getLogger('uvicorn.error')

router = APIRouter()

@router.post("/", description="Create a new entity", summary="Create Entity",
             response_model_exclude_none=True,
             status_code=201,
             responses={201: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_create(request: Request, 
              response: Response,
              createRequest: EntityCreateRequest,
              rpp_cl_trid: Annotated[str | None, Header()] = None,
              conn: EppClient = Depends(get_connection)) -> EntityCreateResponseModel | ProblemModel:
    
    logger.info(f"Create new entity: {createRequest.card.name}")

    epp_request = contact_create(createRequest, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)
    
    rpp_response = to_entity_create(epp_response)
    location = f"{request.url}/{rpp_response.id}" if isinstance(rpp_response, EntityCreateResponseModel) else None
    return update_response(response, epp_response, 201, location, rpp_response)  # 201 Created



@router.get("/{entity_id}", response_model_exclude_none=True, summary="Get Entity Info",
            status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_info(entity_id: str, response: Response,
            conn: EppClient = Depends(get_connection),
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> EntityInfoResponse | ProblemModel:
    logger.info(f"Fetching info for entity: {entity_id}")

    epp_request = contact_info(entity_id, rpp_cl_trid, epp_authorization)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_entity_info(epp_response)
    return update_response(response, epp_response, 200, None, rpp_response)


@router.head("/{entity_id}/availability", summary="Check Entity Availability",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_check_head(entity_id: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None | ProblemModel:

    logger.info(f"Check for entity: {entity_id}")

    epp_request = contact_check(entity_id, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = do_entity_check(epp_response)
    update_response(response, epp_response)
    # no response body, update http status
    add_check_status(response, rpp_response)

# @router.get("/{entity_id}/availability", summary="Check Entity Existence")
# async def do_check_get(entity_id: str, 
#             response: Response,
#             conn: EppClient = Depends(get_connection),
#             rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

#     logger.info(f"Check for entity: {entity_id}")

@router.delete("/{entity_id}", response_model_exclude_none=True, summary="Delete Entity",
             responses={204: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_delete(entity_id: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None | ProblemModel:

    logger.info(f"Delete entity: {entity_id}")

    epp_request = contact_delete(entity_id, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_entity_delete(epp_response)
    return update_response(response, epp_response, 204, None, rpp_response)  # 204 No Content
    # delete has no response body, so we just set the status code
    #to_entity_delete(epp_response, response)

@router.patch("/{entity_id}", response_model_exclude_none=True, summary="Update Entity",
              status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_update(entity_id: str,
            update_request: EntityUpdateRequest,
            response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> None | ProblemModel:

    logger.info(f"Update contact: {entity_id}")

    epp_request = contact_update(entity_id, update_request, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)
    rpp_response = to_entity_update(epp_response)
    return update_response(response, epp_response)
    #return to_entity_update(epp_response, response)

@router.post("/{entity_id}/processes/transfers", response_model_exclude_none=True, summary="Start Entity Transfer",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_start_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            conn: EppClient = Depends(get_connection)) -> EntityTransferResponse | ProblemModel:
    logger.info(f"Start transfer for entity: {entity_id}")

    epp_request = contact_transfer(entity_id, rpp_cl_trid, epp_authorization, op=TransferOpType.REQUEST)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_entity_transfer(epp_response, response)

@router.get("/{entity_id}/processes/transfers", summary="Query Transfer Status",
            status_code=200,
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_query_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            conn: EppClient = Depends(get_connection)) -> EntityTransferResponse | ProblemModel:

    logger.info(f"Query transfer for entity: {entity_id}")

    epp_request = contact_transfer_query(entity_id, rpp_cl_trid, epp_authorization)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_entity_transfer(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_response)
 

@router.put("/{entity_id}/processes/transfers/rejection", summary="Reject Entity Transfer",
            status_code=200,
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_reject_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            conn: EppClient = Depends(get_connection)) -> EntityTransferResponse | ProblemModel:

    logger.info(f"Reject transfer for entity: {entity_id}")

    return await do_stop_transfer(TransferOpType.REJECT, 
                                  response,
                                  conn,
                                  entity_id, rpp_cl_trid, epp_authorization)

@router.put("/{entity_id}/processes/transfers/cancellation", summary="Cancel Entity Transfer",
            status_code=200,
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_cancel_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            conn: EppClient = Depends(get_connection)) -> EntityTransferResponse | ProblemModel:

    logger.info(f"Cancel transfer for entity: {entity_id}")

    return await do_stop_transfer(TransferOpType.CANCEL, 
                                  response,
                                  conn,
                                  entity_id, rpp_cl_trid, epp_authorization)

@router.put("/{entity_id}/processes/transfers/approval", summary="Approve Entity Transfer",
            status_code=200,
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_approve_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            conn: EppClient = Depends(get_connection)) -> EntityTransferResponse | ProblemModel:

    logger.info(f"Approve transfer for entity: {entity_id}")

    return await do_stop_transfer(TransferOpType.APPROVE, 
                                  response,
                                  conn,
                                  entity_id, rpp_cl_trid, epp_authorization)



async def do_stop_transfer(op: TransferOpType,
                            response: Response,
                            conn: EppClient,
                            entity_id: str,
                            rpp_cl_trid: str,
                            rpp_authorization: str
                            ) -> EntityTransferResponse | ProblemModel:

    logger.info(f"Stop transfer for entity: {entity_id} with operation: {op}")

    epp_request = contact_transfer(entity_id, rpp_cl_trid, rpp_authorization, op)
    
    epp_response = await conn.send_command(epp_request)
    
    rpp_result = to_entity_transfer(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_result)

@router.get("/{entity_id}/processes/{proc_name}/{proc_id}", summary="List Processes",
            status_code=200,
            responses={200: RPP_CODE_HEADERS,
                       422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_list_processes(entity_id: str,
                                proc_name: str,
                                proc_id: str,
                                response: Response,
                                rpp_cl_trid: Annotated[str | None, Header()] = None,
                                conn: EppClient = Depends(get_connection)):

    logger.info(f"List {proc_name}/{proc_id} processes for entity: {entity_id}")
