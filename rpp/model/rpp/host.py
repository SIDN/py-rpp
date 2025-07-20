from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, IPvAnyAddress

from rpp.model.rpp.common import BaseRequestModel

class HostEventModel(BaseModel):
    name: str
    date: datetime

class HostAddr(BaseModel):
    v4: Optional[List[IPvAnyAddress]] = []
    v6: Optional[List[IPvAnyAddress]] = []

class HostInfoResponseModel(BaseModel):
    name: str
    roid: str
    status: List[str]
    registrar: str
    events: Dict[str, HostEventModel]
    addr: Optional[HostAddr] = None

class HostCreateRequest(BaseRequestModel):
    name: str
    addr: Optional[HostAddr] = None

# class HostInfoRequest(BaseRequestModel):
#     name: str

# class HostDeleteRequest(BaseRequestModel):
#     name: str

# class HostCheckRequest(BaseRequestModel):
#     name: str

class HostUpdateAddOrRemove(BaseModel):
    addr: List[HostAddr]
    status: List[str]

class HostUpdateChange(BaseModel):
    name: str

class HostUpdateRequest(BaseRequestModel):
    add: Optional[HostUpdateAddOrRemove] = None
    remove: Optional[HostUpdateAddOrRemove] = None
    change: Optional[HostUpdateChange] = None

class HostCreateResDataModel(BaseModel):
    name: Optional[str] = None
    createDate: Optional[datetime] = None

class HostCheckResModel(BaseModel):
    name: str
    available: bool
    reason: Optional[str] = None
    lang: Optional[str] = None

