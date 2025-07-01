from typing import List, Optional
from pydantic import BaseModel

class SvcMenuModel(BaseModel):
    versions: List[str]
    languages: List[str]
    objects: List[str]
    extensions: Optional[List[str]] = None

class DcpStatementModel(BaseModel):
    purpose: List[str]
    recipient: List[str]
    retention: str
    
class DcpModel(BaseModel):
    access: List[str]
    statement: Optional[List[DcpStatementModel]] = None
    expiry: Optional[str] = None

class GreetingModel(BaseModel):
    server: str
    serverDateTime: str
    services: SvcMenuModel
    dcp: DcpModel

class ErrorModel(BaseModel):
    code: int
    message: Optional[str] = None