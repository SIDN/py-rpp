from rpp.model.epp.epp_1_0 import (
    CommandType,
    CredsOptionsType,
    Epp,
    ExtUritype,
    LoginSvcType,
    LoginType,
)


def login(
    cl_id,
    pw,
    version="1.0",
    lang="en",
    obj_uri=["urn:ietf:params:xml:ns:domain-1.0"],
    ext_uri=[],
) -> Epp:
    login_options = CredsOptionsType(version=version, lang=lang)

    login_svc = LoginSvcType(
        obj_uri=obj_uri, svc_extension=ExtUritype(ext_uri=ext_uri) if ext_uri else None
    )

    login = LoginType(
        cl_id=cl_id, pw=pw, options=login_options, svcs=login_svc
    )

    login_cmd = CommandType(login=login)
    return Epp(command=login_cmd)


def logout(trId: str) -> Epp:
    logout_cmd = CommandType(logout="", cl_trid=trId)
    return Epp(command=logout_cmd)
