from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field, RootModel


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

class PeriodUnit(str, Enum):
    m = "m"
    y = "y"
    
class PeriodModel(BaseModel):
    unit: PeriodUnit
    value: int

class AuthInfoModel(BaseModel):
    value: str
    roid: Optional[str] = None

class BaseRequestModel(BaseModel):
    pass
    #type_: Optional[str] = Field(default=None, alias='@type')

# Response

class TrIDModel(BaseModel):
    clTRID: Optional[str] = None
    svTRID: Optional[str] = None

class MessageQueueModel(BaseModel):
    count: int
    id: Optional[str] = None
    qDate: Optional[datetime] = None
    message: Optional[str] = None

class ResultModel(BaseModel):
    code: int
    message: str
    lang: Optional[str] = None
    value: Optional[List[Any]] = None 
    extValue: Optional[List[Any]] = None 

class BaseResponseModel(BaseModel):
    model_config = ConfigDict(
            populate_by_alias=True,
            populate_by_name=True
      )
    type_: Optional[str] = Field(default=None, alias='@type')
    result: List[ResultModel]
    #trID: TrIDModel
    messages: Optional[MessageQueueModel] = None
    resData: Optional[Any] = None  
    extension: Optional[Any] = None 
    
class StatusModel(BaseModel):
    name: str
    #reason: Optional[str] = None

class ErrorModel(BaseModel):
    code: str
    message: str
    lang: Optional[str] = None

class ProblemModel(BaseModel):
    type: str = Field(default="https://www.example.org/rpp/problem", alias='type')
    status: int
    title: str
    errors: Optional[List[ErrorModel]] = None

class BaseCheckResponse(BaseModel):
    avail: bool
    reason: Optional[str] = None

