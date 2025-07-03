
from typing import Optional
from fastapi import Response
from rpp.model.epp.epp_1_0 import Epp

def add_status_header(response: Response, status_code: str):
    response.headers["RPP-Code"] = status_code


def add_check_header(response: Response, code: str, avail: bool, reason: Optional[str] = None):
    if avail == True:
        response.headers["RPP-Check-Avail"] = "true"
    else:
      response.headers["RPP-Check-Avail"] = "false"
      if reason:
        response.headers["RPP-Check-Reason"] = reason
