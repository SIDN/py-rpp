from typing import List
from pydantic import BaseModel

class ServerInfoModel(BaseModel):
    server: str
    extensions: List[str]
    currentTime: str
    messages: List[str]
    supportedTlds: List[str]