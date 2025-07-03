from rpp.model.epp.domain_1_0 import InfoNameType
from rpp.model.epp.epp_1_0 import CommandType, Epp, ReadWriteType
from rpp.model.epp.helpers import random_tr_id
from rpp.model.epp.host_1_0 import AddRemType, AddrType, Check, ChgType, Create, Delete, Info, IpType, MNameType, Update
from rpp.model.rpp.host import HostAddr, HostCheckRequest, HostCreateRequest, HostDeleteRequest, HostInfoRequest, HostUpdateRequest


def hostaddr_to_epp(host_addr: HostAddr) -> list[AddrType]:
    addr_list = []
    if not host_addr:
        return addr_list  # Return empty list if no address is provided

    for ip in host_addr.v4 or []:
        addr_list.append(AddrType(value=str(ip), ip=IpType.V4))
    for ip in host_addr.v6 or []:
        addr_list.append(AddrType(value=str(ip), ip=IpType.V6))
    return addr_list


def host_create(host: HostCreateRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            create=ReadWriteType(
                other_element=Create(
                    name=host.name, addr=hostaddr_to_epp(host.addr)
                )
            ),
            cl_trid=host.clTRID or random_tr_id(),
        )
    )

    return epp_request


def host_info(request: HostInfoRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            info=ReadWriteType(
                other_element=Info(name=InfoNameType(value=request.name))
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request

def host_check(request: HostCheckRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            check=ReadWriteType(
                other_element=Check(name=[request.name])
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request

def host_delete(request: HostDeleteRequest) -> Epp:
    epp_request = Epp(
        command=CommandType(
            delete=ReadWriteType(
                other_element=Delete(name=request.name)
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request

def host_update(request: HostUpdateRequest) -> Epp:

    add = None
    rem = None
    chg = ChgType(name=request.change.name) if request.change else None

    if request.add is not None:
      add = AddRemType(
                add=hostaddr_to_epp(request.add.addr),
                status=request.add.status
            )
    if request.remove is not None:
      rem = AddRemType(
                add=hostaddr_to_epp(request.remove.addr),
                status=request.remove.status
            )


    epp_request = Epp(
        command=CommandType(
            update=ReadWriteType(
                other_element=Update(
                    name=request.name,
                    add=add,
                    rem=rem,
                    chg=chg
                )
            ),
            cl_trid=request.clTRID or random_tr_id(),
        )
    )

    return epp_request