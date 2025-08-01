from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, IPvAnyAddress

from rpp.model.rpp.common import BaseCheckResponse, BaseRequestModel, StatusModel

class HostEventModel(BaseModel):
    name: str
    date: datetime

class HostAddr(BaseModel):
    address: IPvAnyAddress
    family: str  # 'v4' or 'v6'

class HostInfoResponse(BaseModel):
    name: str
    roid: str
    status: List[str]
    registrar: str
    events: Dict[str, HostEventModel]
    addr: Optional[List[HostAddr]] = None

class HostCreateRequest(BaseRequestModel):
    name: str
    addr: Optional[List[HostAddr]] = None

class HostUpdateAddOrRemove(BaseModel):
    addr: List[HostAddr]
    status: Optional[List[StatusModel]] = None

class HostUpdateChange(BaseModel):
    name: str

class HostUpdateRequest(BaseRequestModel):
    add: Optional[HostUpdateAddOrRemove] = None
    remove: Optional[HostUpdateAddOrRemove] = None
    change: Optional[HostUpdateChange] = None

class HostCreateResponse(BaseModel):
    name: Optional[str] = None
    createDate: Optional[datetime] = None

class HostCheckResponse(BaseCheckResponse):
    name: str
    # avail: bool
    # reason: Optional[str] = None

