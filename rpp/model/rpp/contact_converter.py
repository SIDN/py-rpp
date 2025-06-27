from typing import List, Dict
from rpp.model.rpp.contact import Card, EventModel, Name, AddressComponent, Organization, Address

def to_contact_info(epp_response):
    """
    Converteer EPP contact info XML response naar een Card.
    """
    # Typical EPP contact info response structure:
    # epp_response.response.res_data.other_element[0] is the contact:infData
    res_data = epp_response.response.res_data.other_element[0]

    # Use Name model for the name property
    name = None
    if hasattr(res_data, "postal_info"):
        pi = res_data.postal_info[0]  # Assuming there's only one postal_info

        # Build components as list of AddressComponent
        components: List[AddressComponent] = []
        if pi.addr:
            if pi.addr.street:
                for street in pi.addr.street:
                    components.append(AddressComponent(kind="street", value=street))
            if pi.addr.city:
                components.append(AddressComponent(kind="city", value=pi.addr.city))
            if pi.addr.sp:
                components.append(AddressComponent(kind="state", value=pi.addr.sp))
            if pi.addr.pc:
                components.append(AddressComponent(kind="postal_code", value=pi.addr.pc))
            if pi.addr.cc:
                components.append(AddressComponent(kind="country", value=pi.addr.cc))

        name = Name(
            full=pi.name
        )

        addresses = { "addr": Address(components=components) }

        organizations = None
        if pi.org:
           organizations = {"org": Organization(name=pi.org)} 

        events: Dict[str, EventModel] = {}
        if hasattr(res_data, "cr_id"):
            events["Create"] = EventModel(name=res_data.cr_id, date=str(res_data.cr_date))

        if hasattr(res_data, "up_id"):
            events["Update"] = EventModel(name=res_data.up_id, date=str(res_data.up_date))

        if hasattr(res_data, "tr_id"):
            events["Transfer"] = EventModel(date=str(res_data.tr_date))
        
        authInfo = None
        if hasattr(res_data, "auth_info") and res_data.auth_info is not None:
            authInfo = res_data.auth_info.pw.value

    return Card(
        type_="Card",
        id=res_data.id,
        roid=res_data.roid,
        status=[s.s.value for s in res_data.status],
        name=name,
        organizations=organizations,
        addresses=addresses,
        events=events,
        authInfo=authInfo
    )