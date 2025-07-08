from typing import List
from pydantic import BaseModel

class Msg(BaseModel):
    value: str
    code: str
    field: str

class SIDNExtMessageModel(BaseModel):
    sidn_messages: List[Msg]