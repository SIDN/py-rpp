
from typing import List

from fastapi import Response
from rpp.model.epp.epp_1_0 import Epp, GreetingType
from rpp.model.epp.sidn_ext_epp_1_0 import Ext, ResponseType
from rpp.model.rpp.common import BaseResponseModel, DcpModel, DcpStatementModel, ErrorModel, ProblemModel, GreetingModel, ResultModel, SvcMenuModel, TrIDModel
from rpp.model.rpp.sidn_ext import Msg, SIDNExtMessageModel


def epp_to_rpp_code(code: int) -> int:

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

def get_set_properties_of_dcp_statement(item_to_check, name: str) -> list[str]:
    set_props = []

    item_to_check = getattr(item_to_check, name, None)
    if item_to_check is not None:
        for key in list(item_to_check.__dataclass_fields__.keys()):
            if getattr(item_to_check, key, None) is not None:
                set_props.append(key)

    return set_props

def to_greeting_model(greeting: GreetingType) -> GreetingModel:

    services = SvcMenuModel(
        versions=[version.value for version in greeting.svc_menu.version] if greeting.svc_menu else None,
        languages=[lang for lang in greeting.svc_menu.lang] if greeting.svc_menu else None,
        objects=[obj for obj in greeting.svc_menu.obj_uri] if greeting.svc_menu else None,
        extensions=[ext for ext in greeting.svc_menu.svc_extension.ext_uri] if greeting.svc_menu and greeting.svc_menu.svc_extension else None
    )

    

    statements: List[DcpStatementModel] = []
    for stmt in greeting.dcp.statement:
        statements.append(
            DcpStatementModel(
                purpose=get_set_properties_of_dcp_statement(stmt, "purpose"),
                recipient=get_set_properties_of_dcp_statement(stmt, "recipient"),
                retention=get_set_properties_of_dcp_statement(stmt, "retention")[0]
            )
        )


    dcp = DcpModel(
        access=get_set_properties_of_dcp_statement(greeting.dcp, "access"),
        statement=statements
    )

    return GreetingModel(
        server=greeting.sv_id,
        serverDateTime=str(greeting.sv_date.to_datetime()),
        services=services,
        dcp=dcp
    )

def to_error_response(epp_response: Epp) -> ProblemModel:
    
    errors: List[ErrorModel] = []
    for res in epp_response.response.result:
        errors.append(ErrorModel(code=str(res.code.value), message=res.msg.value,
                lang=res.msg.lang if res.msg.lang else None))
        
    epp_status: int = get_status_from_response(epp_response)
    return ProblemModel(
        #type=f"urn:ietf:params:rpp:code:{get_status_from_response(epp_response)}",
        status=epp_to_rpp_code(epp_status) if epp_status else 500,
        title="EPP Error",
        errors=errors
    )

    # rpp_response: BaseResponseModel = BaseResponseModel(
    #     trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
    #     svTRID=epp_response.response.tr_id.sv_trid),
    #     result=results)

    # if epp_response.response.extension and epp_response.response.extension.other_element:
    #     # If the response has an SIDN extension, we can assume it is a ResponseType
    #     response_ext: List[Ext] = epp_response.response.extension.other_element
    #     msgs: List[Msg] = []
    #     for ext in response_ext:
    #         if ext.response is not None:
    #             # If the extension has a response, we can assume it is a SIDNExtMessageModel
    #             for msg in ext.response.msg:
    #                 msgs.append(Msg(value=msg.value, code=msg.code, field=msg.field_value))

    #     rpp_response.extension = SIDNExtMessageModel(
    #         sidn_messages=msgs
    #     )

    #return rpp_response

def to_base_response(epp_response: Epp) -> BaseResponseModel:
    
    results: List[ResultModel] = []
    for res in epp_response.response.result:
        results.append(ResultModel(code=res.code.value, message=res.msg.value,
                lang=res.msg.lang if res.msg.lang else None))
        
    rpp_response: BaseResponseModel = BaseResponseModel(
        trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
        svTRID=epp_response.response.tr_id.sv_trid),
        result=results)

    if epp_response.response.extension and epp_response.response.extension.other_element:
        # If the response has an SIDN extension, we can assume it is a ResponseType
        response_ext: List[Ext] = epp_response.response.extension.other_element
        msgs: List[Msg] = []
        for ext in response_ext:
            if ext.response is not None:
                # If the extension has a response, we can assume it is a SIDNExtMessageModel
                for msg in ext.response.msg:
                    msgs.append(Msg(value=msg.value, code=msg.code, field=msg.field_value))

        rpp_response.extension = SIDNExtMessageModel(
            sidn_messages=msgs
        )

    return rpp_response

def get_status_from_response(epp_response: Epp) -> int | None:
    # Check if the response has a result and return the first result code
    if len(epp_response.response.result) > 0:
        return epp_response.response.result[0].code.value

    return None


def is_ok_response(epp_response: Epp) -> tuple[bool, int, str]:

    for res in epp_response.response.result:
        if is_ok_code(res.code.value ):
            return True, res.code.value, res.msg.value
        else:
            return False, res.code.value, res.msg.value

def is_ok_code(code: int) -> bool:
    return code >= 1000 and code < 2000

def to_result_list(epp_response: Epp) -> List[ResultModel]:
    results: List[ResultModel] = []
    for res in epp_response.response.result:
        results.append(ResultModel(code=res.code.value, message=res.msg.value,
                lang=res.msg.lang if res.msg.lang else None))
    
    return results
