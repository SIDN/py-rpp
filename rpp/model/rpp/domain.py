from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel
from rpp.model.rpp.common import BaseRequestModel
from rpp.model.rpp.entity import Card

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
    flags: int
    protocol: int
    alg: int
    pubKey: str

class DSDataModel(BaseModel):
    keyTag: int
    algorithm: int
    digestType: int
    digest: str

class DNSSECModel(BaseModel):
    delegationSigned: bool
    dsData: List[DSDataModel]

class DsOrKeyType(BaseModel):
    keyData: Optional[List[SecDNSKeyDataModel]] = None
    dsData: Optional[List[DSDataModel]] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.keyData is not None and self.dsData is not None:
            raise ValueError("Only one of keyData or dsData can be set.")
        if self.keyData is None and self.dsData is None:
            raise ValueError("One of keyData or dsData must be set.")
        
class AddressListModel(BaseModel):
    v4: Optional[List[str]] = []
    v6: Optional[List[str]] = []

class NameserverModel(BaseModel):
    linked: bool = False
    name: str

class EventModel(BaseModel):
    name: Optional[str] = None
    date:  datetime

class DomainCreateRequest(BaseRequestModel):
    name: str
    period: Optional[PeriodModel] = None
    ns: Optional[List[NsItemModel]] = []
    registrant: str
    contact: List[ContactModel]
    authInfo: Optional[str] = None
    dnssec: Optional[DsOrKeyType] = None

class DomainInfoRequest(BaseRequestModel):
    authInfo: str

class DomainCheckRequest(BaseRequestModel):
    name: str

class DomainInfoResponse(BaseModel):
    name: str
    registrant: str
    roid: str
    status: Optional[List[str]] = None
    dnssec: Optional[DsOrKeyType] = None
    contacts: List[ContactModel]
    nameservers: Optional[List[NameserverModel]] = None
    registrar: str
    events: Dict[str, EventModel]
    expires: Optional[datetime] = None
    authInfo: Optional[str] = None

