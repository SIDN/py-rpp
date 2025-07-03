from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, RootModel, with_config, field_validator, ValidationError

from rpp.model.rpp.common import BaseRequestModel

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

class Card(BaseModel):
    model_config = ConfigDict(
            populate_by_alias=True,
            populate_by_name=True
      )
    type_: Optional[str] = Field(default="Card", alias='@type')
    version: Optional[str] = Field(default="2.0" )
    roid: Optional[str] = Field(default=None, alias='rpp.ietf.org:roid')
    id: str = Field( alias='rpp.ietf.org:id')
    name: Name
    organizations: Dict[str, Organization] = None
    addresses: Addresses
    phones: Optional[Phones] = None
    emails: Optional[Emails] = None
    

    @field_validator('version')
    @classmethod
    def version_must_be_2_0(cls, v):
        if v is not None and str(v) != "2.0":
            raise ValueError('version must be "2.0"')
        return v


class TransactionModel(BaseModel):
    clientId: str
    serverId: Optional[str] = None

class ContactCreateRequest(BaseRequestModel):
    card: Card 
    authInfo: Optional[str] = None

class ContactInfoRequest(BaseRequestModel):
    authInfo: Optional[str] = None
    #transaction: TransactionModel

class ContactCheckRequest(BaseRequestModel):
    name: str

class ContactInfoResponse(BaseModel):
    card: Card 
    status: Optional[List[str]] = None
    authInfo: Optional[str] = None
    transaction: TransactionModel
    events: Optional[Dict[str, EventModel]] = None