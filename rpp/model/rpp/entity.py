from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator

from rpp.model.rpp.common import AuthInfoModel, BaseRequestModel, StatusModel

class NameComponent(BaseModel):
    kind: str
    value: str

class Name(BaseModel):
    full: str
    components: Optional[List[NameComponent]] = None

class Organization(BaseModel):
    name: str

class AddressComponent(BaseModel):
    kind: str
    value: str

class Address(BaseModel):
    components: Optional[List[AddressComponent]] = None
    countryCode: Optional[str] = None
    coordinates: Optional[str] = None
    full: Optional[str] = None
    contexts: Optional[Dict[str, bool]] = None

class Addresses(RootModel[Dict[str, Address]]):
    pass

class PhoneFeatures(BaseModel):
    voice: Optional[bool] = None
    fax: Optional[bool] = None

class Phone(BaseModel):
    features: PhoneFeatures
    number: str

class Phones(RootModel[Dict[str, Phone]]):
    pass

class Email(BaseModel):
    address: str

class Emails(RootModel[Dict[str, Email]]):
    pass

class EventModel(BaseModel):
    name: str
    date: datetime

class SidnLegalForm(BaseModel):
    name: str
    number: str

class Card(BaseModel):
    model_config = ConfigDict(
            populate_by_alias=True,
            populate_by_name=True
      )
    type_: Optional[str] = Field(default="Card", alias='@type')
    version: Optional[str] = Field(default="2.0" )
    id: str = Field( alias='rpp.ietf.org:id')
    name: Name
    organizations: Dict[str, Organization] = None
    addresses: Addresses
    phones: Optional[Phones] = None
    emails: Optional[Emails] = None
    # if internationalized, use the 'int_' field = True
    int_: Optional[bool] = False
    legalForm: Optional[SidnLegalForm] = Field(default=None, alias='rpp.ietf.org:legalForm')

    @field_validator('version')
    @classmethod
    def version_must_be_2_0(cls, v):
        if v is not None and str(v) != "2.0":
            raise ValueError('version must be "2.0"')
        return v

class EntityCreateRequest(BaseRequestModel):
    card: Card 
    authInfo: Optional[AuthInfoModel] = None

class EntityCreateResponseModel(BaseModel):
    id: Optional[str] = None
    createDate: Optional[datetime] = None

class EntityInfoResponse(BaseModel):
    roid: Optional[str] = Field(default=None, alias='rpp.ietf.org:roid')
    card: Card 
    status: Optional[List[str]] = None
    authInfo: Optional[AuthInfoModel] = None
    events: Optional[Dict[str, EventModel]] = None

class EntityUpdateAddOrRemove(BaseModel):
    status: List[StatusModel]

class EntityUpdateChange(BaseModel):
    contact: List[Card] 
    authInfo: AuthInfoModel

class EntityUpdateRequest(BaseRequestModel):
    add: Optional[EntityUpdateAddOrRemove] = None
    remove: Optional[EntityUpdateAddOrRemove] = None
    change: Optional[EntityUpdateChange] = None

class EntityTransferResponse(BaseModel):
    id: str
    trStatus: str
    reId: str
    reDate: datetime
    acID: str
    acDate: datetime
    exDate: Optional[datetime] = None 