
import logging
from typing import Optional
from fastapi import HTTPException, Response
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.rpp.common import AuthInfoModel
from rpp.model.rpp.common_converter import get_status_from_response, is_ok_code

logger = logging.getLogger('uvicorn.error')

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


def auth_info_from_header(header_value: str) -> AuthInfoModel | None:
    """
    Parse the structured header value into a dictionary.
    Example header value: "AuthInfo=xxx:Roid=yyy"
    """

    if header_value:
        # Remove whitespace and parse key=value pairs separated by colon
        cleaned = header_value.replace(" ", "")
        parts = dict(item.split("=", 1) for item in cleaned.split(",") if "=" in item)
        return AuthInfoModel(
            value=parts.get("AuthInfo"),
            roid=parts.get("Roid")
        )
    
    return None