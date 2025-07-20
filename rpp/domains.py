import logging
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, Response
from fastapi.params import Body
from rpp.common import add_check_status, auth_info_from_header, update_response, update_response_from_code
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from rpp.model.epp.domain_converter import domain_check, domain_delete, domain_info, domain_create, domain_renew, domain_transfer, domain_transfer_query, domain_update
from rpp.model.epp.epp_1_0 import Epp, TransferOpType
from rpp.model.rpp.common import AuthInfoModel, BaseResponseModel
from fastapi.security import HTTPBasic

from rpp.model.rpp.domain import DomainCheckRequest, DomainCreateRequest, DomainDeleteRequest, DomainInfoRequest, DomainRenewRequest, DomainStartTransferRequest, DomainTransferRequest, DomainUpdateRequest
from rpp.model.rpp.domain_converter import do_domain_check, to_domain_check_response, to_domain_create, to_domain_delete, to_domain_info, to_domain_renew, to_domain_transfer, to_domain_update

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

@router.get("/{domainname}", response_model_exclude_none=True, summary="Get Domain Info")
async def do_info(domainname: str, response: Response,
             conn: EppClient = Depends(get_connection),
             rpp_authorization: Annotated[str | None, Header()] = None,
             rpp_cl_trid: Annotated[str | None, Header()] = None) -> BaseResponseModel:

    logger.info(f"Fetching info for domain: {domainname}")

    auth_info = auth_info_from_header(rpp_authorization)

    epp_request = domain_info(DomainInfoRequest(
        name=domainname,
        clTRID=rpp_cl_trid,
        authInfo=auth_info
    ))
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_domain_info(epp_response, response)

@router.head("/{domainname}/availability", summary="Check Domain Existence")
async def do_check_head(domainname: str, response: Response,
             rpp_cl_trid: Annotated[str | None, Header()] = None,
             conn: EppClient = Depends(get_connection)):

    logger.info(f"Check domain: {domainname}")

    epp_request = domain_check(DomainCheckRequest(name=domainname, clTRID=rpp_cl_trid))
    epp_response = await conn.send_command(epp_request)

    avail, epp_status, reason = do_domain_check(epp_response)

    add_check_status(response, epp_status, avail, reason)

@router.get("/{domainname}/availability", summary="Check Domain Existence")
async def do_check_get(domainname: str, response: Response,
             rpp_cl_trid: Annotated[str | None, Header()] = None,
             conn: EppClient = Depends(get_connection)):
    logger.info(f"Check domain: {domainname}")

    epp_request = domain_check(DomainCheckRequest(name=domainname, clTRID=rpp_cl_trid))
    epp_response = await conn.send_command(epp_request)

    avail, epp_status, reason = do_domain_check(epp_response)
    update_response(response, epp_response)
    add_check_status(response, epp_status, avail, reason)
    return to_domain_check_response(epp_response)

@router.delete("/{domainname}", status_code=204, summary="Delete Domain")
async def do_delete(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)):
    logger.info(f"Delete domain: {domainname}")
    
    epp_request = domain_delete(DomainDeleteRequest(name=domainname, clTRID=rpp_cl_trid))
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response, 204)  # 204 No Content
    to_domain_delete(epp_response, response)

# TODO: Use RGP domain cancel delete command when implemented

# @router.delete("/{domainname}/deletion", status_code=204, summary="Delete Domain")
# async def do_cancel_delete(domainname: str, response: Response,
#             rpp_cl_trid: Annotated[str | None, Header()] = None,
#             conn: EppClient = Depends(get_connection)):
#     logger.info(f"Cancel delete domain: {domainname}")

#     epp_request = domain_cancel_delete(DomainCancelDeleteRequest(name=domainname, clTRID=rpp_cl_trid))
#     epp_response = await conn.send_command(epp_request)

#     update_response(response, epp_response, 204)  # 204 No Content
#     to_domain_cancel_delete(epp_response, response)

@router.patch("/{domainname}", response_model_exclude_none=True, summary="Update Domain")
async def do_update(update_request: DomainUpdateRequest,
            response: Response,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Update domain: {update_request.name}")

    epp_request = domain_update(update_request)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_domain_update(epp_response, response)

@router.post("/{domainname}/processes/renewals", summary="Renew Domain")
async def do_renew(domainname: str,
                   response: Response,
                   renew_request: DomainRenewRequest,
                   rpp_cl_trid: Annotated[str | None, Header()] = None,
                   conn: EppClient = Depends(get_connection)) -> BaseResponseModel:

    logger.info(f"Renew domain: {domainname}")

    epp_request = domain_renew(domainname, renew_request, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_domain_renew(epp_response, response)

@router.post("/{domainname}/processes/transfers", response_model_exclude_none=True, summary="Start Domain Transfer")
async def do_start_transfer(domainname: str, response: Response,
            transfer_request: Optional[DomainStartTransferRequest]= Body(default=None),
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    logger.info(f"Start transfer for domain: {transfer_request.name if transfer_request else domainname}")

    rpp_request = transfer_request
    if rpp_request is None:
        # No body was provided
        if not rpp_auth_info:
            logger.error("rpp_auth_info required when no transfer request body is provided")
            raise HTTPException(status_code=400, detail="rpp_auth_info required when no transfer request body is provided")
        logger.info("No transfer request body provided")
        rpp_request = DomainStartTransferRequest(name=domainname, clTRID=rpp_cl_trid,
                                            authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None)

    epp_request = domain_transfer(rpp_request, op=TransferOpType.REQUEST)
    epp_response = await conn.send_command(epp_request)

    update_response(response, epp_response)
    return to_domain_transfer(epp_response, response)

@router.get("/{domainname}/processes/transfers/latest", summary="Query Transfer Status")
async def do_query_transfer(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    """Query a transfer for the specified domain.
    """
    logger.info(f"Query transfer for domain: {domainname}")
    epp_request = domain_transfer_query(DomainTransferRequest(name=domainname, 
                                                              clTRID=rpp_cl_trid, 
                                                              authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None)
                                        )
    epp_response = await conn.send_command(epp_request)
    
    update_response(response, epp_response)
    return to_domain_transfer(epp_response, response)

@router.post("/{domainname}/processes/transfers/latest/rejection", summary="Reject Domain Transfer")
async def do_reject_transfer(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    
    logger.info(f"Reject transfer for domain: {domainname}")
    return await do_stop_transfer(TransferOpType.REJECT, domainname, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

@router.post("/{domainname}/processes/transfers/latest/cancellation", summary="Cancel Domain Transfer")
async def do_cancel_transfer(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> BaseResponseModel:
    
    logger.info(f"Cancel transfer for domain: {domainname}")
    return await do_stop_transfer(TransferOpType.CANCEL, domainname, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

@router.post("/{domainname}/processes/transfers/latest/approval", summary="Approve Domain Transfer")
async def do_approve_transfer(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            rpp_auth_info: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)):

    logger.info(f"Approve transfer for domain: {domainname}")

    return await do_stop_transfer(TransferOpType.APPROVE, domainname, response,
            conn=conn, rpp_cl_trid=rpp_cl_trid, rpp_auth_info=rpp_auth_info)

async def do_stop_transfer(op: TransferOpType,
                    domainname: str, response: Response,
                    conn: EppClient = None,
                    rpp_cl_trid: Annotated[str | None, Header()] = None,
                    rpp_auth_info: Annotated[str | None, Header()] = None,
                    ) -> BaseResponseModel:

    logger.info(f"Stop transfer for domain: {domainname} with operation: {op}")

    epp_request = domain_transfer(DomainTransferRequest(name=domainname,
                            clTRID=rpp_cl_trid,
                            authInfo=AuthInfoModel(value=rpp_auth_info) if rpp_auth_info else None
                            ), op=op)
    epp_response = await conn.send_command(epp_request)
    
    update_response(response, epp_response)
    return to_domain_transfer(epp_response, response)


@router.post("/{domain}/processes/locks", status_code=501, summary="Lock Domain (Not Implemented)")
async def do_lock(domain: str, response: Response) -> None:

    logger.info(f"Lock domain: {domain}")
    update_response_from_code(response, 2101) # Not implemented

    # TODO: add support for Registry lock