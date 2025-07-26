import logging
from typing import Annotated, Optional
from fastapi import HTTPException, Response
from fastapi.params import Header
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.rpp.common import AuthInfoModel
from rpp.model.rpp.common_converter import get_status_from_response, is_ok_code

logger = logging.getLogger('uvicorn.error')

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

def update_response(response: Response, epp_response: Epp, default_http_status_code: int = None):
    status_code = get_status_from_response(epp_response)
    update_response_from_code(response, status_code, default_http_status_code)
    add_transaction_headers(response, epp_response)

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
    response.headers["Rpp-Code"] = str(status_code)

def epp_to_rpp_code(code: int) -> int:
    """
    Set the HTTP status code on the response based on the result code(s) in BaseResponseModel.
    """
    if code >= 1000 and code < 2000:
        # no error
        return 200
    elif code == 2303:
        # object not found
        return 404
    elif (code >= 2200 and code < 2300) or code == 2501:
        # authentication errors
        return 401
    elif (code >= 2000 and code < 2200) or (code >= 2300 and code < 2400):
        # client errors
        return 400
    elif code in (2400, 2500):
        # server errors
        return 500
    elif code == 2502:
        # session rate limit exceeded
        return 429
    else:
        # unknown error
        return 500

def add_check_status(response: Response, epp_status: int, avail: bool, reason: Optional[str] = None):
    if is_ok_code(epp_status):
        if avail == True:
            # available
            response.status_code = 200
        else:
            response.status_code = 404
            if reason:
                pass
                #TODO: add reason to response
    else:
        response.status_code = epp_to_rpp_code(epp_status)

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
        if not parts or parts[0].lower() != "authinfo":
            raise ValueError(f"Invalid authorization scheme: {parts[0]}")

        # Split by comma, then by '='
        kv = {}
        for item in parts[1].split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                k = k.strip().lower()  # keys are case-insensitive
                v = v.strip()          # values preserve case
                kv[k] = v

        if not kv.get("value"):
            raise ValueError("Missing 'value' in rpp_authorization header")

        return AuthInfoModel(
                    value=kv.get("value"),
                    roid=kv.get("roid")
                )
   
   return None
