from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel

# Greeting

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

class PeriodModel(BaseModel):
    unit: str
    value: int

class AuthInfoModel(BaseModel):
    value: str
    roid: Optional[str] = None

class BaseRequestModel(BaseModel):
    clTRID: Optional[str] = None

# Response

class TrIDModel(BaseModel):
    clTRID: Optional[str] = None
    svTRID: Optional[str] = None

class MessageQueueModel(BaseModel):
    count: int
    id: Optional[str] = None
    qDate: datetime = None
    message: str = None

class ResultModel(BaseModel):
    code: int
    message: str
    lang: Optional[str] = None
    value: Optional[List[Any]] = None 
    extValue: Optional[List[Any]] = None 

class BaseResponseModel(BaseModel):
    result: List[ResultModel]
    trID: TrIDModel
    messages: Optional[MessageQueueModel] = None
    resData: Optional[Any] = None  
    extension: Optional[Any] = None 
    
# class TransferResponse(BaseModel):
#     name: str
#     trStatus: str
#     reId: str
#     reDate: datetime
#     acID: str
#     acDate: datetime
#     exDate: Optional[datetime] = None 

