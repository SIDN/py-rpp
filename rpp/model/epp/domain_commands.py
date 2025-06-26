from rpp.model.epp.epp_1_0 import CommandType, Epp, ReadWriteType
from rpp.model.epp.domain_1_0 import Info, InfoNameType


def domain_info(domain: str) -> Epp:
    """
    Create a domain info request object for the given domain.

    :param domain: The domain name to create the DomainInfoType for.
    :return: An Epp object with the specified domain.
    """

    epp_request = Epp(
        command=CommandType(
            info=ReadWriteType(
                other_element=Info(name=InfoNameType(value=domain))
            )
        )
    )

    return epp_request
