import logging
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response
from fastapi.params import Body
from rpp.common import add_check_header, update_response, update_response_from_code
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient

from rpp.model.epp.contact_commands import contact_check, contact_create, contact_delete, contact_info, contact_transfer, contact_transfer_query, contact_update
from rpp.model.epp.epp_1_0 import TransferOpType
from rpp.model.rpp.common import AuthInfoModel, BaseResponseModel
from rpp.model.rpp.common_converter import is_ok_code
from rpp.model.rpp.entity import ContactCheckRequest, ContactCreateRequest, ContactDeleteRequest, ContactInfoRequest, ContactStartTransferRequest, ContactTransferRequest, ContactUpdateRequest
from rpp.model.rpp.entity_converter import to_contact_check, to_contact_create, to_contact_delete, to_contact_info, to_contact_transfer, to_contact_update
from fastapi import APIRouter
from fastapi.security import HTTPBasic

logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()

router = APIRouter(dependencies=[Depends(security)])

@router.post("/", description="Create a new entity", summary="Create Entity",
             response_model=BaseResponseModel, response_model_exclude_none=True)
def do_create(request: Request, 
              response: Response,
              createRequest: ContactCreateRequest,
              conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    
    logger.info(f"Create new entity: {createRequest.card.name}")

    epp_request = contact_create(createRequest)
    epp_response = conn.send_command(epp_request)
    update_response(response, epp_response, 201)  # 201 Created
    return to_contact_create(epp_response)


@router.get("/{entity_id}", response_model_exclude_none=True, summary="Get Entity Info")
def do_info(entity_id: str, response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:
    logger.info(f"Fetching info for entity: {entity_id}")

    epp_request = contact_info(ContactInfoRequest(id=entity_id, clTRID=rpp_cl_trid))
    epp_response = conn.send_command(epp_request)

    rpp_response = to_contact_info(epp_response)
    update_response(response, epp_response)
    return rpp_response

@router.post("/{entity_id}", response_model_exclude_none=True, summary="Get Entity Info (message body)")
def do_info_with_body(entity_id: str, response: Response,
             conn: EppClient = Depends(get_connection),
             info_request: ContactInfoRequest = Body(ContactInfoRequest)) -> BaseResponseModel:

    logger.info(f"Fetching info for entity: {entity_id}")

    epp_request = contact_info(info_request)
    epp_response = conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_contact_info(epp_response)

@router.head("/{entity_id}", summary="Check Entity Existence")
def do_check(entity_id: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Check for entity: {entity_id}")

    rpp_request = ContactCheckRequest(name=entity_id, clTRID=rpp_cl_trid)
    epp_request = contact_check(rpp_request)
    epp_response = conn.send_command(epp_request)

    avail, epp_status, reason = to_contact_check(epp_response)

    update_response(response, epp_response)
    if is_ok_code(epp_status):
        add_check_header(response, avail, reason)

@router.delete("/{entity_id}", response_model_exclude_none=True, status_code=204, summary="Delete Entity")
def do_delete(entity_id: str, 
            response: Response,
            conn: EppClient = Depends(get_connection),
            rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Delete entity: {entity_id}")

    rpp_request = ContactDeleteRequest(name=entity_id, clTRID=rpp_cl_trid)
    epp_request = contact_delete(rpp_request)
    epp_response = conn.send_command(epp_request)

    update_response(response, epp_response, 204)  # 204 No Content
    # delete has no response body, so we just set the status code
    to_contact_delete(epp_response, response)

@router.patch("/{entity_id}", response_model_exclude_none=True, summary="Update Entity")
def do_update(update_request: ContactUpdateRequest,
            response: Response,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Update contact: {update_request.id}")

    epp_request = contact_update(update_request)
    epp_response = conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_contact_update(epp_response, response)

@router.post("/{entity_id}/renewal", status_code=501, summary="Renew Entity (Not Implemented)")
def do_renew(entity_id: str, response: Response) -> None:

    logger.info(f"Renew entity: {entity_id}")
    update_response_from_code(response, 2101) # Not implemented

@router.post("/{entity_id}/transfer", response_model_exclude_none=True, summary="Start Entity Transfer")
def do_start_transfer(entity_id: str, response: Response,
            transfer_request: Optional[ContactTransferRequest]= Body(default=None),
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
        rpp_request = ContactStartTransferRequest(id=entity_id, clTRID=rpp_cl_trid,
                                            authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None)

    epp_request = contact_transfer(rpp_request, op=TransferOpType.REQUEST)
    epp_response = conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_contact_transfer(epp_response, response)

@router.get("/{entity_id}/transfer", summary="Query Transfer Status",)
def do_query_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Query transfer for entity: {entity_id}")
    epp_request = contact_transfer_query(ContactTransferRequest(id=entity_id,
                                                                clTRID=rpp_cl_trid,
                                                                authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None)
                                        )
    epp_response = conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_contact_transfer(epp_response, response)

@router.post("/{entity_id}/transfer/rejection", summary="Reject Entity Transfer")
def do_reject_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Reject transfer for entity: {entity_id}")
    return do_stop_transfer(TransferOpType.REJECT, entity_id, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

@router.post("/{entity_id}/transfer/cancellation", summary="Cancel Entity Transfer")
def do_cancel_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Cancel transfer for entity: {entity_id}")
    return do_stop_transfer(TransferOpType.CANCEL, entity_id, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

@router.post("/{entity_id}/transfer/approval", summary="Approve Entity Transfer")
def do_approve_transfer(entity_id: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)):

    logger.info(f"Approve transfer for entity: {entity_id}")

    return do_stop_transfer(TransferOpType.APPROVE, entity_id, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

def do_stop_transfer(op: TransferOpType,
                    entity_id: str, response: Response,
                    conn: EppClient = None,
                    rpp_cl_trid: Annotated[str | None, Header()] = None,
                    rpp_auth_info: Annotated[str | None, Header()] = None,
                    ) -> BaseResponseModel:

    logger.info(f"Stop transfer for entity: {entity_id} with operation: {op}")

    epp_request = contact_transfer(ContactTransferRequest(id=entity_id,
                            clTRID=rpp_cl_trid,
                            authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None
                            ), op=op)
    epp_response = conn.send_command(epp_request)
    
    update_response(response, epp_response)
    return to_contact_transfer(epp_response, response)
