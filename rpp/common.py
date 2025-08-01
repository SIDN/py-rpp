import logging
from typing import Annotated, Optional
from fastapi import HTTPException, Response
from fastapi.params import Header
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.rpp.common import AuthInfoModel, BaseCheckResponse, ProblemModel
from rpp.model.rpp.common_converter import epp_to_rpp_code, get_status_from_response, is_ok_code
from rpp.model.rpp.domain import DomainCheckResponse
from rpp.model.rpp.message import MessageAckModel

logger = logging.getLogger('uvicorn.error')

RPP_AUTH_INFO_HEADER_EPP_SCHEME = "authinfo"

RPP_CODE_HEADERS = {
    "headers": {
        "RPP-Code": {
            "description": "RPP result code",
            "schema": {"type": "string"}
        },
        "RPP-Cltrid": {
            "description": "RPP client transaction ID",
            "schema": {"type": "string"}
        },
        "RPP-Svtrid": {
            "description": "RPP server transaction ID",
            "schema": {"type": "string"}
        }
    }
}

RPP_PROBLEM_REPORT_SCHEMA = {
    #"model": ProblemModel,
    "description": "Validation Error",
    "content": {
                "application/problem+json": {
                    "schema": ProblemModel.model_json_schema()
                }
            }
}

def update_response(response: Response, epp_response: Epp,
                    default_http_status_code: int = None,
                    location: str = None,
                    rpp_response = None):
    
    status_code = get_status_from_response(epp_response)
    update_response_from_code(response, status_code, default_http_status_code)
    add_transaction_headers(response, epp_response)
    if location:
        response.headers["Location"] = location

    if isinstance(rpp_response, ProblemModel):
        response.headers["Content-Type"] = "application/problem+json"

    if isinstance(rpp_response, MessageAckModel):
        response.headers["RPP-Msg-Count"] = str(rpp_response.msg_count)
    return rpp_response

def add_transaction_headers(response: Response, epp_response: Epp):
    response.headers["RPP-Cltrid"] = epp_response.response.tr_id.cl_trid
    response.headers["RPP-Svtrid"] = epp_response.response.tr_id.sv_trid

def update_response_from_code(response: Response, status_code: int, default_http_status_code: int = None):
    set_response_status(response, status_code, default_http_status_code)
    add_status_header(response, status_code)
   

def set_response_status(response: Response, epp_code: int, default_http_status_code: int = None):
    # allow the status code to be overridden by the default_http_status_code
    # but only if the status code is 200
    http_status_code = epp_to_rpp_code(epp_code)
    response.status_code = http_status_code if http_status_code != 200 else default_http_status_code or 200

def add_status_header(response: Response, status_code: int):
    response.headers["Rpp-Code"] = f"0{status_code}"

def add_check_status(response: Response, rpp_response: BaseCheckResponse | ProblemModel):
    if isinstance(rpp_response, BaseCheckResponse):
        if rpp_response.avail:
                response.status_code = 404
        else:
            # host not exists
            response.status_code = 200

    else:
        # must be a problem report
        response.status_code = rpp_response.status
            
# def add_check_status__(response: Response, epp_status: int, avail: bool, reason: Optional[str] = None):
#     if is_ok_code(epp_status):
#         if avail:
#             # available, host does not exist
#             response.status_code = 404
#         else:
#             # host exists
#             response.status_code = 200
#             if reason:
#                 pass
#                 #TODO: add reason to response
#     else:
#         response.status_code = epp_to_rpp_code(epp_status)

class EppException(HTTPException):
    def __init__(self, status_code: int = 500, epp_response: Epp = None, headers: Optional[dict] = None):
        self.epp_response = epp_response
        super().__init__(status_code=status_code, headers=headers)


def epp_auth_info_from_header(rpp_authorization: Annotated[str, Header()] = None) -> AuthInfoModel:
   """
    Parse the structured header value into an AuthInfoModel.
    Example header value: "authinfo value=xxx, roid=yyy"
    Only the keys and 'authinfo' prefix are case-insensitive.
    """
   if rpp_authorization:
        # Split on whitespace, check prefix case-insensitively
        parts = rpp_authorization.strip().split(None, 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid rpp_authorization header value")
        if not parts or parts[0].lower() != RPP_AUTH_INFO_HEADER_EPP_SCHEME:
            raise ValueError(f"Invalid authorization scheme: {parts[0]}")

        # Split by comma, then by '='
        kv = {}
        for item in parts[1].split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                k = k.strip().lower()
                v = v.strip()
                kv[k] = v

        if not kv.get("value"):
            raise ValueError("Missing 'value' in rpp_authorization header")

        return AuthInfoModel(
                    value=kv.get("value"),
                    roid=kv.get("roid")
                )
   
   return None
