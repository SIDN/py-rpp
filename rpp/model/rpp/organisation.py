from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, IPvAnyAddress

from rpp.model.rpp.common import BaseRequestModel

class OrganisationModel(BaseModel):
    name: str
    date: datetime


class OrganisationInfoRequestModel(BaseRequestModel):
    name: str

class OrganisationInfoResponseModel(BaseModel):
    name: str

class OrganisationDeleteRequestModel(BaseRequestModel):
    name: str

class OrganisationUpdateRequestModel(BaseRequestModel):
    name: str
