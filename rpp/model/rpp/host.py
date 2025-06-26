from typing import List, Optional
from pydantic import BaseModel, IPvAnyAddress

class HostAddr(BaseModel):
    v4: Optional[List[IPvAnyAddress]] = []
    v6: Optional[List[IPvAnyAddress]] = []
    

class Host(BaseModel):
    name: str
    addr: Optional[HostAddr] = None
    clTRID: Optional[str] = None