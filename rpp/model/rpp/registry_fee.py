# Fee Models
# from: https://datatracker.ietf.org/doc/html/rfc8748#

from datetime import timedelta
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel
from pydantic import condecimal, Field
from typing import List, Optional
from pydantic import BaseModel, Field, condecimal
from enum import Enum

from rpp.model.rpp.common import PeriodModel

# class FeeCreditModel(BaseModel):
#     description: str
#     value: float
#     lang: Optional[str] = None

# class FeeModel(BaseModel):
#     description: Optional[str] = None
#     refundable: Optional[bool] = None
#     gracePeriod: Optional[PeriodModel] = None
#     applied: Optional[bool] = None
#     lang: Optional[str] = None

# class RegistryFeeModel(BaseModel):
#     currency: Optional[str] = None
#     period: Optional[PeriodModel] = None
#     fees: List[FeeModel]
#     credit: Optional[List[FeeCreditModel]] = None
#     balance: Optional[float] = None
#     creditLimit: Optional[float] = None




class FeeCommandEnum(str, Enum):
    create = "create"
    delete = "delete"
    renew = "renew"
    update = "update"
    transfer = "transfer"
    restore = "restore"
    custom = "custom"

class FeeAppliedEnum(str, Enum):
    immediate = "immediate"
    delayed = "delayed"

class FeeReasonType(BaseModel):
    value: str
    lang: Optional[str] = "en"

class FeeType(BaseModel):
    value: condecimal(ge=0) # type: ignore
    description: Optional[str] = None
    lang: Optional[str] = "en"
    refundable: Optional[bool] = None
    grace_period: Optional[timedelta] = Field(default=None, alias="grace-period")
    applied: Optional[FeeAppliedEnum] = None

class CreditType(BaseModel):
    value: condecimal(le=0)  # type: ignore
    description: Optional[str] = None
    lang: Optional[str] = "en"

# class FeeObjectIdentifierType(BaseModel):
#     value: str
#     element: Optional[str] = Field(default="name")

class FeeCommandType(BaseModel):
    period: Optional[PeriodModel] = None 
    name: FeeCommandEnum
    customName: Optional[str] = None
    phase: Optional[str] = None
    subphase: Optional[str] = None

class FeeCommandDataType(FeeCommandType):
    fee: Optional[List[FeeType]] = None
    credit: Optional[List[CreditType]] = None
    reason: Optional[FeeReasonType] = None
    standard: Optional[bool] = False

class FeeObjectCDType(BaseModel):
    objID: str
    class_: Optional[str] = Field(default=None, alias="class")
    command: Optional[List[FeeCommandDataType]] = None
    reason: Optional[FeeReasonType] = None
    avail: Optional[bool] = True

class FeeCheckType(BaseModel):
    currency: Optional[str] = None
    command: List[FeeCommandType]

class FeeChkDataType(BaseModel):
    currency: str
    cd: List[FeeObjectCDType]

class FeeTransformCommandType(BaseModel):
    currency: Optional[str] = None
    fee: List[FeeType]
    credit: Optional[List[CreditType]] = None

class FeeTransformResultType(BaseModel):
    currency: Optional[str] = None
    period: Optional[PeriodModel] = None
    fee: Optional[List[FeeType]] = None
    credit: Optional[List[CreditType]] = None
    balance: Optional[Decimal] = None
    creditLimit: Optional[Decimal] = None

# # For forward references
# from pydantic import ConfigDict
# FeeCommandType.model_rebuild()
# FeeTransformResultType.model_rebuild()

class BaseResponseModelWithFee(BaseModel):
    fees: Optional[FeeTransformResultType] = None