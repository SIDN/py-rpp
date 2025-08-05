import logging
from typing import Annotated
from urllib import response
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response
from fastapi.params import Body
from rpp.common import RPP_CODE_HEADERS, RPP_PROBLEM_REPORT_SCHEMA, add_check_status, epp_auth_info_from_header, update_response, update_response_from_code
from rpp.epp_connection_pool import get_connection
from rpp.epp_client import EppClient
from rpp.model.epp.domain_converter import domain_check, domain_delete, domain_info, domain_create, domain_renew, domain_transfer, domain_transfer_query, domain_update
from rpp.model.epp.epp_1_0 import TransferOpType
from rpp.model.rpp.common import AuthInfoModel, ProblemModel

from rpp.model.rpp.domain import DomainCheckResponse, DomainCreateRequest, DomainCreateResponse, DomainInfoResponse, DomainRenewRequest, DomainRenewResponse, DomainTransferRequest, DomainTransferResponse, DomainUpdateRequest, DomainUpdateResponse
from rpp.model.rpp.domain_converter import to_domain_check_response, to_domain_create, to_domain_delete, to_domain_info, to_domain_renew, to_domain_transfer, to_domain_update

logger = logging.getLogger('uvicorn.error')
router = APIRouter()


@router.post("/", description="Create a new domain", summary="Create Domain",
             status_code=201,
             responses={201: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA}, response_model_exclude_none=True)
async def do_create(create_request: DomainCreateRequest, 
              request: Request,
              response: Response,
              rpp_cl_trid: Annotated[str | None, Header()] = None,
              conn: EppClient = Depends(get_connection)) -> DomainCreateResponse | ProblemModel:
    logger.info(f"Create new domain: {create_request.name}")

    epp_request = domain_create(create_request, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_domain_create(epp_response)
    location = f"{request.url}/{rpp_response.name}" if isinstance(rpp_response, DomainCreateResponse) else None
    return update_response(response, epp_response, 201, location, rpp_response)  # 201 Created

@router.get("/{domainname}", response_model_exclude_none=True, summary="Get Domain Info",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_info(domainname: str, response: Response,
             conn: EppClient = Depends(get_connection),
             epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
             rpp_cl_trid: Annotated[str | None, Header()] = None,
             filter: str = "all") -> DomainInfoResponse | ProblemModel:

    logger.info(f"Fetching info for domain: {domainname}")

    epp_request = domain_info(domainname, filter, rpp_cl_trid, epp_authorization)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_domain_info(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_response)

@router.head("/{domainname}/availability", summary="Check Domain Availability",
             responses={204: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_check_head(domainname: str, response: Response,     
             rpp_cl_trid: Annotated[str | None, Header()] = None,
             conn: EppClient = Depends(get_connection)) -> None:

    logger.info(f"Check domain: {domainname}")

    epp_request = domain_check(domainname, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_domain_check_response(epp_response)

    update_response(response, epp_response)
    # no response body, update http status
    add_check_status(response, rpp_response)

@router.get("/{domainname}/availability", response_model_exclude_none=True, summary="Check Domain Availability",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_check_get(domainname: str, response: Response,
             rpp_cl_trid: Annotated[str | None, Header()] = None,
             conn: EppClient = Depends(get_connection)) -> DomainCheckResponse | ProblemModel:
    logger.info(f"Check domain: {domainname}")

    epp_request = domain_check(domainname, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    #avail, epp_status, reason = do_domain_check(epp_response)
    rpp_response = to_domain_check_response(epp_response)
    update_response(response, epp_response, rpp_response=rpp_response)
    # there is a response body, update http status
    add_check_status(response, rpp_response)
    return rpp_response

@router.delete("/{domainname}", summary="Delete Domain",
                status_code=204,
                response_model_exclude_none=True,
               responses={204: RPP_CODE_HEADERS,
                          422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_delete(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> None:
    logger.info(f"Delete domain: {domainname}")
    
    epp_request = domain_delete(domainname, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_domain_delete(epp_response)
    return update_response(response, epp_response, 204, rpp_response=rpp_response)  # 204 No Content

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

@router.patch("/{domainname}", response_model_exclude_none=True, summary="Update Domain",
                status_code=200,
                responses={200: RPP_CODE_HEADERS,
                           422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_update(domainname: str,
            update_request: DomainUpdateRequest,
            response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            conn: EppClient = Depends(get_connection)) -> DomainUpdateResponse | ProblemModel:

    logger.info(f"Update domain: {domainname}")

    epp_request = domain_update(domainname, update_request, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_domain_update(epp_response, response)
    return update_response(response, epp_response, rpp_response=rpp_response)
    #return to_domain_update(epp_response, response)

@router.post("/{domainname}/processes/renewals", summary="Renew Domain",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_renew(domainname: str,
                   response: Response,
                   renew_request: DomainRenewRequest,
                   rpp_cl_trid: Annotated[str | None, Header()] = None,
                   conn: EppClient = Depends(get_connection)) -> DomainRenewResponse | ProblemModel:

    logger.info(f"Renew domain: {domainname}")

    epp_request = domain_renew(domainname, renew_request, rpp_cl_trid)
    epp_response = await conn.send_command(epp_request)
    rpp_response = to_domain_renew(epp_response)

    return update_response(response, epp_response, rpp_response=rpp_response) 

@router.post("/{domainname}/processes/transfers", response_model_exclude_none=True, summary="Start Domain Transfer",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_start_transfer(domainname: str,
                            response: Response,
                            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
                            request: DomainTransferRequest = Body(None),
                            rpp_cl_trid: Annotated[str | None, Header()] = None,
                            conn: EppClient = Depends(get_connection)) -> DomainTransferResponse | ProblemModel:
    logger.info(f"Start transfer for domain: {domainname}")


    if not epp_authorization:
        raise HTTPException(status_code=400, detail="epp_authorization required")

    epp_request = domain_transfer(domainname, request, rpp_cl_trid, epp_authorization, op=TransferOpType.REQUEST)
    epp_response = await conn.send_command(epp_request)

    rpp_response = to_domain_transfer(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_response)

@router.get("/{domainname}/processes/transfers/latest", summary="Query Transfer Status",
                status_code=200,
                responses={200: RPP_CODE_HEADERS,
                           422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_query_transfer(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            conn: EppClient = Depends(get_connection)) -> DomainTransferResponse | ProblemModel:
   
    logger.info(f"Query transfer for domain: {domainname}")

    epp_request = domain_transfer_query(domainname, rpp_cl_trid, epp_authorization)

    epp_response = await conn.send_command(epp_request)
    
    rpp_response = to_domain_transfer(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_response)

@router.put("/{domainname}/processes/transfers/latest/rejection", summary="Reject Domain Transfer",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_reject_transfer(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            conn: EppClient = Depends(get_connection)) -> DomainTransferResponse | ProblemModel:
    
    logger.info(f"Reject transfer for domain: {domainname}")

    return await do_stop_transfer(TransferOpType.REJECT, domainname, response,
            conn, rpp_cl_trid, epp_authorization)

@router.put("/{domainname}/processes/transfers/latest/cancellation", summary="Cancel Domain Transfer",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_cancel_transfer(domainname: str, response: Response,
            rpp_cl_trid: Annotated[str | None, Header()] = None,
            epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
            conn: EppClient = Depends(get_connection)) -> DomainTransferResponse | ProblemModel:
    
    logger.info(f"Cancel transfer for domain: {domainname}")

    return await do_stop_transfer(TransferOpType.CANCEL, domainname, response,
            conn, rpp_cl_trid, epp_authorization)

@router.put("/{domainname}/processes/transfers/latest/approval", summary="Approve Domain Transfer",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_approve_transfer(domainname: str, response: Response,
                                epp_authorization: AuthInfoModel | None = Depends(epp_auth_info_from_header),
                                rpp_cl_trid: Annotated[str | None, Header()] = None,
                                conn: EppClient = Depends(get_connection)):

    logger.info(f"Approve transfer for domain: {domainname}")

    return await do_stop_transfer(TransferOpType.APPROVE, domainname, response,
            conn, rpp_cl_trid, epp_authorization)

async def do_stop_transfer(op: TransferOpType,
                    domainname: str,
                    response: Response,
                    conn: EppClient,
                    rpp_cl_trid: str,
                    rpp_auth_info: AuthInfoModel | None = None,
                    ) -> DomainTransferResponse | ProblemModel:

    logger.info(f"Stop transfer for domain: {domainname} with operation: {op}")

    epp_request = domain_transfer(DomainTransferRequest(name=domainname,
                                                        clTRID=rpp_cl_trid,
                                                        authInfo=rpp_auth_info
                                                        ), op=op)
    epp_response = await conn.send_command(epp_request)
    
    rpp_response = to_domain_transfer(epp_response)
    return update_response(response, epp_response, rpp_response=rpp_response)


@router.post("/{domain}/processes/locks", summary="Lock Domain (Not Implemented)",
             status_code=200,
             responses={200: RPP_CODE_HEADERS,
                        422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_lock(domain: str, response: Response,
                  rpp_cl_trid: Annotated[str | None, Header()] = None) -> None:

    logger.info(f"Lock domain: {domain}")
    update_response_from_code(response, 2101) # Not implemented

    # TODO: add support for Registry lock

@router.get("/{domainname}/processes/{proc_name}/{proc_id}", summary="List Processes",
                status_code=200,
                responses={200: RPP_CODE_HEADERS,
                           422: RPP_PROBLEM_REPORT_SCHEMA})
async def do_list_processes(domainname: str,
                                proc_name: str,
                                proc_id: str,
                                response: Response,
                                rpp_cl_trid: Annotated[str | None, Header()] = None,
                                rpp_authorization: Annotated[str | None, Header()] = None,
                                conn: EppClient = Depends(get_connection)):

    logger.info(f"List {proc_name}/{proc_id} processes for domain: {domainname}")


