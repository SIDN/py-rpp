from typing import List, Optional
from pydantic import BaseModel
from rpp.model.rpp.contact import Card

class PeriodModel(BaseModel):
    unit: str
    text: str

class NsItemModel(BaseModel):
    type: str
    value: str

class ContactModel(BaseModel):
    type: str
    value: str

class SecDNSKeyDataModel(BaseModel):
    flags: str
    protocol: str
    alg: str
    pubKey: str

class DSDataModel(BaseModel):
    keyTag: int
    algorithm: int
    digestType: int
    digest: str

class DNSSECModel(BaseModel):
    delegationSigned: bool
    dsData: List[DSDataModel]

class AddressListModel(BaseModel):
    v4: Optional[List[str]] = []
    v6: Optional[List[str]] = []

class NameserverModel(BaseModel):
    name: str
    address: Optional[AddressListModel]

class DomainCreateRequest(BaseModel):
    name: str
    period: Optional[PeriodModel] = None
    ns: Optional[List[NsItemModel]] = []
    registrant: str
    contact: List[ContactModel]
    authInfo: Optional[str] = None
    clTRID: Optional[str] = None
    secDNS_keyData: Optional[SecDNSKeyDataModel] = None

class DomainInfoResponse(BaseModel):
    name: str
    registrant: str
    dnssec: Optional[DNSSECModel] = None
    contacts: List[ContactModel]
    nameservers: List[NameserverModel]