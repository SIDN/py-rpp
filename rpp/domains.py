import logging
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, Response
from fastapi.params import Body
from rpp.common import add_check_header, update_response, update_response_from_code
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from rpp.model.epp.domain_converter import domain_check, domain_delete, domain_info, domain_create, domain_renew, domain_transfer, domain_transfer_query, domain_update
from rpp.model.epp.epp_1_0 import TransferOpType
from rpp.model.rpp.common import AuthInfoModel, BaseResponseModel
from rpp.model.rpp.common_converter import is_ok_code
from fastapi.security import HTTPBasic

from rpp.model.rpp.domain import DomainCheckRequest, DomainCreateRequest, DomainDeleteRequest, DomainInfoRequest, DomainRenewRequest, DomainStartTransferRequest, DomainTransferRequest, DomainUpdateRequest
from rpp.model.rpp.domain_converter import to_domain_check, to_domain_create, to_domain_delete, to_domain_info, to_domain_renew, to_domain_transfer, to_domain_update

logger = logging.getLogger('uvicorn.error')
security = HTTPBasic()

router = APIRouter(dependencies=[Depends(security)])


@router.post("/", description="Create a new domain", summary="Create Domain",
             response_model=BaseResponseModel, response_model_exclude_none=True)
async def do_create(create_request: DomainCreateRequest, 
              response: Response,
              conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    logger.info(f"Create new domain: {create_request.name}")

    epp_request = domain_create(create_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response, 201)  # 201 Created
    return to_domain_create(epp_response)

@router.get("/{domain_name}", response_model_exclude_none=True, summary="Get Domain Info (no message body)")
async def do_info(domain_name: str, response: Response,
             conn: EppClient = Depends(get_connection),
             rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:
    
    logger.info(f"Fetching info for domain: {domain_name}")

    epp_request = domain_info(DomainInfoRequest(name=domain_name, clTRID=rpp_cl_trid))
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_domain_info(epp_response, response)

@router.post("/{domain_name}", response_model_exclude_none=True, summary="Get Domain Info (message body)")
async def do_info_with_body(domain_name: str, response: Response,
             conn: EppClient = Depends(get_connection),
             info_request: DomainInfoRequest = Body(DomainInfoRequest)) -> BaseResponseModel:
    
    logger.info(f"Fetching info for domain: {domain_name}")

    epp_request = domain_info(info_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return epp_response

@router.head("/{domain_name}", summary="Check Domain Existence")
async def do_check(domain_name: str, response: Response,
             rpp_cl_trid: Annotated[str | None, Header()] = None,
             conn: EppClient = Depends(get_connection)):
    
    logger.info(f"Check domain: {domain_name}")
    
    epp_request = domain_check(DomainCheckRequest(name=domain_name, clTRID=rpp_cl_trid))
    epp_response = await conn.send_command(epp_request)

    avail, epp_status, reason = to_domain_check(epp_response)

    update_response(response, epp_response)
    if is_ok_code(epp_status):
        add_check_header(response, avail, reason)

@router.delete("/{domain_name}", status_code=204, summary="Delete Domain")
async def do_delete(domain_name: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)):
    logger.info(f"Delete domain: {domain_name}")
    
    epp_request = domain_delete(DomainDeleteRequest(name=domain_name, clTRID=rpp_cl_trid))
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response, 204)  # 204 No Content
    to_domain_delete(epp_response, response)


@router.patch("/{domain_name}", response_model_exclude_none=True, summary="Update Domain")
async def do_update(update_request: DomainUpdateRequest,
            response: Response,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Update domain: {update_request.name}")

    epp_request = domain_update(update_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_domain_update(epp_response, response)

@router.post("/{domain_name}/renewal", summary="Renew Domain")
async def do_renew(renew_request: DomainRenewRequest, 
             response: Response, conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Renew domain: {renew_request.name}")

    epp_request = domain_renew(renew_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_domain_renew(epp_response, response)

@router.post("/{domain_name}/transfer", response_model_exclude_none=True, summary="Start Domain Transfer")
async def do_start_transfer(domain_name: str, response: Response,
            transfer_request: Optional[DomainStartTransferRequest]= Body(default=None),
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    logger.info(f"Start transfer for domain: {transfer_request.name if transfer_request else domain_name}")

    rpp_request = transfer_request
    if rpp_request is None:
        # No body was provided
        if not rpp_auth_info:
            logger.error("rpp_auth_info required when no transfer request body is provided")
            raise HTTPException(status_code=400, detail="rpp_auth_info required when no transfer request body is provided")
        logger.info("No transfer request body provided")
        rpp_request = DomainStartTransferRequest(name=domain_name, clTRID=rpp_cl_trid,
                                            authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None)

    epp_request = domain_transfer(rpp_request, op=TransferOpType.REQUEST)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_domain_transfer(epp_response, response)

@router.get("/{domain_name}/transfer", summary="Query Transfer Status")
async def do_query_transfer(domain_name: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    """Query a transfer for the specified domain.
    """
    logger.info(f"Query transfer for domain: {domain_name}")
    epp_request = domain_transfer_query(DomainTransferRequest(name=domain_name, 
                                                              clTRID=rpp_cl_trid, 
                                                              authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None)
                                        )
    epp_response = await conn.send_command(epp_request)
    
    update_response(response, epp_response)
    return to_domain_transfer(epp_response, response)

@router.post("/{domain_name}/transfer/rejection", summary="Reject Domain Transfer")
async def do_reject_transfer(domain_name: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    
    logger.info(f"Reject transfer for domain: {domain_name}")
    return await do_stop_transfer(TransferOpType.REJECT, domain_name, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

@router.post("/{domain_name}/transfer/cancellation", summary="Cancel Domain Transfer")
async def do_cancel_transfer(domain_name: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    
    logger.info(f"Cancel transfer for domain: {domain_name}")
    return await do_stop_transfer(TransferOpType.CANCEL, domain_name, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

@router.post("/{domain_name}/transfer/approval", summary="Approve Domain Transfer")
async def do_approve_transfer(domain_name: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)):

    logger.info(f"Approve transfer for domain: {domain_name}")

    return await do_stop_transfer(TransferOpType.APPROVE, domain_name, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

async def do_stop_transfer(op: TransferOpType,
                    domain_name: str, response: Response,
                    conn: EppClient = None,
                    rpp_cl_trid: Annotated[str | None, Header()] = None,
                    rpp_auth_info: Annotated[str | None, Header()] = None,
                    ) -> BaseResponseModel:

    logger.info(f"Stop transfer for domain: {domain_name} with operation: {op}")

    epp_request = domain_transfer(DomainTransferRequest(name=domain_name,
                            clTRID=rpp_cl_trid,
                            authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None
                            ), op=op)
    epp_response = await conn.send_command(epp_request)
    
    update_response(response, epp_response)
    return to_domain_transfer(epp_response, response)


@router.post("/{domain}/lock", status_code=501, summary="Lock Domain (Not Implemented)")
async def do_lock(domain: str, response: Response) -> None:

    logger.info(f"Lock domain: {domain}")
    update_response_from_code(response, 2101) # Not implemented

    # TODO: add support for Registry lock