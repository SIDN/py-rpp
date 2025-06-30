from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, RootModel, with_config

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
    version: Optional[str] = "1.0"
    uid: Optional[str] = None
    name: Name
    organizations: Dict[str, Organization] = None
    addresses: Addresses
    phones: Optional[Phones] = None
    emails: Optional[Emails] = None
    roid: Optional[str] = Field(default=None, alias='rpp.ietf.org:roid')
    id: Optional[str] = Field(default=None, alias='rpp.ietf.org:id')


class ContactCreateRequest(BaseModel):
    card: Card 
    authInfo: Optional[str] = None
    clTrId: Optional[str] = None


class ContactInfoResponse(BaseModel):
    card: Card 
    status: Optional[List[str]] = None
    authInfo: Optional[str] = None
    clTrId: Optional[str] = None
    events: Optional[Dict[str, EventModel]] = None