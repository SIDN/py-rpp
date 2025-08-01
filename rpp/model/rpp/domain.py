from datetime import date, datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from rpp.model.rpp.common import AuthInfoModel, BaseCheckResponse, BaseRequestModel, PeriodModel, StatusModel

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
    authInfo: Optional[AuthInfoModel] = None
    dnssec: Optional[DsOrKeyType] = None

class DomainCreateResponse(BaseModel):
    name: str
    created: datetime
    expires: Optional[datetime] = None

class DomainCheckResponse(BaseCheckResponse):
    name: str
    # avail: bool
    # reason: Optional[str] = None

class DomainInfoResponse(BaseModel):
    name: str
    registrant: Optional[str] = None
    roid: str
    status: Optional[List[str]] = None
    dnssec: Optional[DsOrKeyType] = None
    contacts: List[ContactModel]
    nameservers: Optional[List[NameserverModel]] = None
    registrar: str
    events: Dict[str, EventModel]
    expires: Optional[datetime] = None
    authInfo: Optional[AuthInfoModel] = None

class DomainUpdateAddOrRemove(BaseModel):
    ns: Optional[List[str]] = None
    contact: Optional[List[ContactModel]] = None
    status: Optional[List[StatusModel]] = None

class DomainUpdateChange(BaseModel):
    registrant: str
    authInfo: AuthInfoModel

class DomainUpdateRequest(BaseRequestModel):
    add: Optional[DomainUpdateAddOrRemove] = None
    remove: Optional[DomainUpdateAddOrRemove] = None
    change: Optional[DomainUpdateChange] = None

class DomainRenewRequest(BaseRequestModel):
    currentExpiry: date
    period: Optional[PeriodModel] = None

class DomainRenewResponse(BaseModel):
    name: str
    expDate: Optional[datetime] = None

class DomainTransferRequest(BaseRequestModel):
    period: Optional[PeriodModel] = None

class DomainTransferResponse(BaseModel):
    name: str
    trStatus: str
    reId: str
    reDate: datetime
    acID: str
    acDate: datetime
    exDate: Optional[datetime] = None 
