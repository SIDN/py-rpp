
from rpp.model.epp.epp_1_0 import Epp
from rpp.model.rpp.common import BaseResponseModel
from rpp.model.rpp.organisation import OrganisationInfoResponseModel


def to_organisation_create(epp_response: Epp) -> BaseResponseModel:
    pass

def to_organisation_delete(epp_response: Epp) -> BaseResponseModel:
    pass

def to_organisation_info(epp_response) -> OrganisationInfoResponseModel | BaseResponseModel:
    pass

def to_organisation_check(epp_response: Epp) -> tuple[bool, int, str]:
    pass

def to_organisation_update(epp_response: Epp) -> BaseResponseModel:
    pass