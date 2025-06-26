from typing import List, Dict, Optional
from pydantic import BaseModel, Field, RootModel

class NameComponent(BaseModel):
    kind: str
    value: str

class Name(BaseModel):
    full: str
    components: List[NameComponent]

class Organization(BaseModel):
    name: str

class Organizations(BaseModel):
    org: Organization

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

class Card(BaseModel):
    type_: str = Field(..., alias='@type')
    version: str
    uid: str
    name: Name
    organizations: Organizations
    addresses: Addresses
    phones: Phones
    emails: Emails

    
# {
#     "@type": "Card",
#     "version": "1.0",
#     "uid": "74b64df3-2d60-56b4-9df3-8594886f4456",
#     "name": {
#         "full": "Joe User",
#         "components": [
#             {
#                 "kind": "surname",
#                 "value": "User"
#             },
#             {
#                 "kind": "given",
#                 "value": "Joe"
#             }
#         ]
#     },
#     "organizations": {
#         "org": {
#             "name": "Org Example"
#         }
#     },
#     "addresses": {
#         "addr": {
#             "components": [
#                 {
#                     "kind": "name",
#                     "value": "Main Street 1"
#                 },
#                 {
#                     "kind": "locality",
#                     "value": "Ludwigshafen am Rhein"
#                 },
#                 {
#                     "kind": "region",
#                     "value": "Rhineland-Palatinate"
#                 },
#                 {
#                     "kind": "postcode",
#                     "value": "67067"
#                 },
#                 {
#                     "kind": "country",
#                     "value": "Germany"
#                 }
#             ],
#             "countryCode": "DE",
#             "coordinates": "geo:49.477409, 8.445180"
#         },
#         "addresses-1": {
#             "full": "Somewhere Street 1 Mutterstadt 67112 Germany",
#             "contexts": {
#                 "private": true
#             }
#         }
#     },
#     "phones": {
#         "voice": {
#             "features": {
#                 "voice": true
#             },
#             "number": "tel:+49-1522-3433333"
#         },
#         "fax": {
#             "features": {
#                 "fax": true
#             },
#             "number": "tel:+49-30-901820"
#         }
#     },
#     "emails": {
#         "email": {
#             "address": "joe.user@example.com"
#         }
#     }
# }