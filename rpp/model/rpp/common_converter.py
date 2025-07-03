
from typing import List
from rpp.model.epp.epp_1_0 import DcpStatementType, Epp, GreetingType
from rpp.model.rpp.common import BaseResponseModel, DcpModel, DcpStatementModel, GreetingModel, ResultModel, SvcMenuModel, TrIDModel


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
        versions=[version.value for version in greeting.svc_menu.version],
        languages=[lang for lang in greeting.svc_menu.lang],
        objects=[obj for obj in greeting.svc_menu.obj_uri],
        extensions=[ext for ext in greeting.svc_menu.svc_extension.ext_uri] if greeting.svc_menu.svc_extension else None
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

def to_base_response(epp_response: Epp) -> BaseResponseModel:
    
    results: List[ResultModel] = []
    for res in epp_response.response.result:
        results.append(ResultModel(code=res.code.value, message=res.msg.value,
                lang=res.msg.lang if res.msg.lang else None))

    return BaseResponseModel(
        trID=TrIDModel(clTRID=epp_response.response.tr_id.cl_trid,
        svTRID=epp_response.response.tr_id.sv_trid),
        result=results)


def is_ok_response(epp_response: Epp) -> tuple[bool, str, str]:

    for res in epp_response.response.result:
        if res.code.value == 1000:
            return True, res.code.value, res.msg.value
        else:
            return False, res.code.value, res.msg.value


def to_result_list(epp_response: Epp) -> List[ResultModel]:
    results: List[ResultModel] = []
    for res in epp_response.response.result:
        results.append(ResultModel(code=res.code.value, message=res.msg.value,
                lang=res.msg.lang if res.msg.lang else None))
    
    return results
    # first_result = epp_response.response.result[0]
    # result = ResultModel(code=first_result.code.value, message=first_result.msg.value,
    #             lang=first_result.msg.lang if first_result.msg.lang else None)

