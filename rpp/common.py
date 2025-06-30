
from fastapi import Response
from rpp.model.epp.epp_1_0 import Epp

def add_status_header(fa_response: Response, epp_response: Epp):
    fa_response.headers["RPP-STATUS-CODE"] = str(epp_response.response.result[0].code.value)
