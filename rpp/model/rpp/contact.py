from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, RootModel

class NameComponent(BaseModel):
    kind: str
    value: str

class Name(BaseModel):
    full: str
    components: Optional[List[NameComponent]] = None

class Organization(BaseModel):
    name: str

# class Organizations(BaseModel):
#     org: Organization

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
    type_: Optional[str] = Field(default="Card", alias='@type')
    version: Optional[str] = "1.0"
    uid: Optional[str] = None
    roid: Optional[str] = None
    id: Optional[str] = None
    status: Optional[List[str]] = None
    name: Name
    organizations: Dict[str, Organization] = None
    addresses: Addresses
    phones: Optional[Phones] = None
    emails: Optional[Emails] = None
    events: Dict[str, EventModel]
    authInfo: Optional[str] = None

    