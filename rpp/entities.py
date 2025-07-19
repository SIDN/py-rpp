import logging
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response
from fastapi.params import Body
from rpp.common import add_check_status, update_response, update_response_from_code
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient

from rpp.model.epp.contact_converter import contact_check, contact_create, contact_delete, contact_info, contact_transfer, contact_transfer_query, contact_update
from rpp.model.epp.epp_1_0 import TransferOpType
from rpp.model.rpp.common import AuthInfoModel, BaseResponseModel
from rpp.model.rpp.common_converter import is_ok_code
from rpp.model.rpp.entity import EntityCheckRequest, EntityCreateRequest, EntityDeleteRequest, EntityInfoRequest, EntityStartTransferRequest, EntityTransferRequest, EntityUpdateRequest
from rpp.model.rpp.entity_converter import to_entity_check, to_entity_create, to_entity_delete, to_entity_info, to_entity_transfer, to_entity_update
from fastapi.security import HTTPBasic

logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()

router = APIRouter(dependencies=[Depends(security)])

@router.post("/", description="Create a new entity", summary="Create Entity",
             response_model=BaseResponseModel, response_model_exclude_none=True)
async def do_create(request: Request, 
              response: Response,
              createRequest: EntityCreateRequest,
              conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    
    logger.info(f"Create new entity: {createRequest.card.name}")

    epp_request = contact_create(createRequest)
    epp_response = await conn.send_command(epp_request)
    update_response(response, epp_response, 201)  # 201 Created
    return to_entity_create(epp_response)


@router.get("/{entity_id}", response_model_exclude_none=True, summary="Get Entity Info")
async def do_info(entity_id: str, response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:
    logger.info(f"Fetching info for entity: {entity_id}")

    epp_request = contact_info(EntityInfoRequest(id=entity_id, clTRID=rpp_cl_trid))
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_entity_info(epp_response)

@router.post("/{entity_id}", response_model_exclude_none=True, summary="Get Entity Info (message body)")
async def do_info_with_body(entity_id: str, response: Response,
             conn: EppClient = Depends(get_connection),
             info_request: EntityInfoRequest = Body(EntityInfoRequest)) -> BaseResponseModel:

    logger.info(f"Fetching info for entity: {entity_id}")

    epp_request = contact_info(info_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_entity_info(epp_response)

@router.head("/{entity_id}/availability", summary="Check Entity Existence")
async def do_check(entity_id: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Check for entity: {entity_id}")

    rpp_request = EntityCheckRequest(name=entity_id, clTRID=rpp_cl_trid)
    epp_request = contact_check(rpp_request)
    epp_response = await conn.send_command(epp_request)

    avail, epp_status, reason = to_entity_check(epp_response)

    add_check_status(response, epp_status, avail, reason)

@router.delete("/{entity_id}", response_model_exclude_none=True, status_code=204, summary="Delete Entity")
async def do_delete(entity_id: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Delete entity: {entity_id}")

    rpp_request = EntityDeleteRequest(name=entity_id, clTRID=rpp_cl_trid)
    epp_request = contact_delete(rpp_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response, 204)  # 204 No Content
    # delete has no response body, so we just set the status code
    to_entity_delete(epp_response, response)

@router.patch("/{entity_id}", response_model_exclude_none=True, summary="Update Entity")
async def do_update(update_request: EntityUpdateRequest,
            response: Response,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Update contact: {update_request.id}")

    epp_request = contact_update(update_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_entity_update(epp_response, response)

@router.post("/{entity_id}/renewal", status_code=501, summary="Renew Entity (Not Implemented)")
async def do_renew(entity_id: str, response: Response) -> None:

    logger.info(f"Renew entity: {entity_id}")
    update_response_from_code(response, 2101) # Not implemented

@router.post("/{entity_id}/transfer", response_model_exclude_none=True, summary="Start Entity Transfer")
async def do_start_transfer(entity_id: str, response: Response,
            transfer_request: Optional[EntityTransferRequest]= Body(default=None),
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    logger.info(f"Start transfer for entity: {entity_id}")

    rpp_request = transfer_request
    if rpp_request is None:
        # No body was provided
        if not rpp_auth_info:
            logger.error("rpp_auth_info required when no transfer request body is provided")
            raise HTTPException(status_code=400, detail="rpp_auth_info required when no transfer request body is provided")
        logger.info("No transfer request body provided")
        rpp_request = EntityStartTransferRequest(id=entity_id, clTRID=rpp_cl_trid,
                                            authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None)

    epp_request = contact_transfer(rpp_request, op=TransferOpType.REQUEST)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_entity_transfer(epp_response, response)

@router.get("/{entity_id}/transfer", summary="Query Transfer Status",)
async def do_query_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Query transfer for entity: {entity_id}")
    epp_request = contact_transfer_query(EntityTransferRequest(id=entity_id,
                                                                clTRID=rpp_cl_trid,
                                                                authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None)
                                        )
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_entity_transfer(epp_response, response)

@router.post("/{entity_id}/transfer/rejection", summary="Reject Entity Transfer")
async def do_reject_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Reject transfer for entity: {entity_id}")
    return await do_stop_transfer(TransferOpType.REJECT, entity_id, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

@router.post("/{entity_id}/transfer/cancellation", summary="Cancel Entity Transfer")
async def do_cancel_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Cancel transfer for entity: {entity_id}")
    return await do_stop_transfer(TransferOpType.CANCEL, entity_id, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

@router.post("/{entity_id}/transfer/approval", summary="Approve Entity Transfer")
async def do_approve_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)):

    logger.info(f"Approve transfer for entity: {entity_id}")

    return await do_stop_transfer(TransferOpType.APPROVE, entity_id, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

async def do_stop_transfer(op: TransferOpType,
                    entity_id: str, response: Response,
                    conn: EppClient = None,
                    rpp_cl_trid: Annotated[str | None, Header()] = None,
                    rpp_auth_info: Annotated[str | None, Header()] = None,
                    ) -> BaseResponseModel:

    logger.info(f"Stop transfer for entity: {entity_id} with operation: {op}")

    epp_request = contact_transfer(EntityTransferRequest(id=entity_id,
                            clTRID=rpp_cl_trid,
                            authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None
                            ), op=op)
    epp_response = await conn.send_command(epp_request)
    
    update_response(response, epp_response)
    return to_entity_transfer(epp_response, response)
