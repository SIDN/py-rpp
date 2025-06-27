from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, IPvAnyAddress

class HostEventModel(BaseModel):
    name: str
    date: datetime

class HostAddr(BaseModel):
    v4: Optional[List[IPvAnyAddress]] = []
    v6: Optional[List[IPvAnyAddress]] = []

class HostModel(BaseModel):
    name: str
    roid: str
    status: List[str]
    registrar: str
    events: Dict[str, HostEventModel]
    addresses: HostAddr

class HostCreateRequest(BaseModel):
    name: str
    addr: Optional[HostAddr] = None
    clTRID: Optional[str] = None