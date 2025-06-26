from rpp.model.rpp.domain import DomainInfoResponse, NameserverModel, ContactModel


def to_domain_info(epp_response):
     # --- Map EPP response to DomainInfoResponse ---
    res_data = epp_response.response.res_data.other_element[0]
    nameservers = []
    for ns in res_data.ns.host_obj:
        nameservers.append(NameserverModel(name=ns, address=None))  # Fill address if available

    contacts = []
    for contact in res_data.contact:
        contacts.append(ContactModel(type=contact.type_value, value=contact.value))

    domain_info_response = DomainInfoResponse(
        name=res_data.name,
        registrant=res_data.registrant,
        contacts=contacts,  # Now a list of ContactModel
        nameservers=nameservers,
        # Add other fields as needed
    )
    return domain_info_response