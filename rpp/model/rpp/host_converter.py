from rpp.model.rpp.host import HostModel, HostEventModel, HostAddr
from typing import Dict

def to_host_info(epp_response):
    """Converteer EPP host info XML response naar een HostModel."""

    # Typical EPP host info response structure:
    # epp_response.response.res_data.other_element[0] is the host:infData
    res_data = epp_response.response.res_data.other_element[0]

    # Status
    status = [s.s for s in getattr(res_data, "status", [])]

    # Events (e.g. create, update, etc.)
    events: Dict[str, HostEventModel] = {}
    if hasattr(res_data, "cr_id") and res_data.cr_id is not None:
        events["Create"] = HostEventModel(name=res_data.cr_id, date=str(res_data.cr_date))

    if hasattr(res_data, "up_id") and res_data.up_id is not None:
        events["Update"] = HostEventModel(name=res_data.up_id, date=str(res_data.up_date))

    # Addresses
    v4 = []
    v6 = []
    if hasattr(res_data, "addr"):
        for addr in res_data.addr:
            if addr.ip.value == "v4":
                v4.append(addr.value)
            elif addr.ip.value == "v6":
                v6.append(addr.value)
    addresses = HostAddr(
        v4=v4 if v4 else None,
        v6=v6 if v6 else None
    )

    return HostModel(
        name=res_data.name,
        roid=res_data.roid,
        status=status,
        registrar=getattr(res_data, "cl_id", ""),
        events=events,
        addresses=addresses
    )