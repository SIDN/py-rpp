
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.rpp.common import ProblemModel
from rpp.model.rpp.organisation import OrganisationCheckResponse, OrganisationCreateResponse, OrganisationInfoResponse


def to_organisation_create(epp_response: Epp) -> OrganisationCreateResponse | ProblemModel:
    pass

def to_organisation_delete(epp_response: Epp) -> None | ProblemModel:
    pass

def to_organisation_info(epp_response) -> OrganisationInfoResponse | ProblemModel:
    pass

def to_organisation_check(epp_response: Epp) -> OrganisationCheckResponse | ProblemModel:
    pass

def to_organisation_update(epp_response: Epp) -> None | ProblemModel:
    pass