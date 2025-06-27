from rpp.model.epp.domain_1_0 import InfoNameType
from rpp.model.epp.epp_1_0 import CommandType, Epp, ReadWriteType
from rpp.model.epp.host_1_0 import Create, Info
from rpp.model.epp.helpers import random_tr_id
from rpp.model.rpp.host import HostCreateRequest, HostAddr

from rpp.model.epp.host_1_0 import AddrType, IpType

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
            create=ReadWriteType(other_element=Create(name=host.name,
                                                       addr=hostaddr_to_epp(host.addr)
                                                      )
        ),
        cl_trid=host.clTRID or random_tr_id()
        )
        
    )
    
    return epp_request

def host_info(host: str) -> Epp:

    epp_request = Epp(
        command=CommandType(
            info=ReadWriteType(
                other_element=Info(name=InfoNameType(value=host))
            )
        )
    )

    return epp_request