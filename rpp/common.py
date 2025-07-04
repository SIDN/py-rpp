
from typing import Optional
from fastapi import HTTPException, Response
from pydantic import BaseModel
from rpp.model.epp.epp_1_0 import Epp

def add_status_header(response: Response, status_code: int):
    response.headers["RPP-Code"] = str(status_code)


def add_check_header(response: Response, avail: bool, reason: Optional[str] = None):
    if avail == True:
        response.headers["RPP-Check-Avail"] = "true"
    else:
      response.headers["RPP-Check-Avail"] = "false"
      if reason:
        response.headers["RPP-Check-Reason"] = reason


class EppException(HTTPException):
    def __init__(self, status_code: int = 500, epp_response: Epp = None):
        #self.status_code = status_code
        self.epp_response = epp_response
        super().__init__(status_code=status_code)