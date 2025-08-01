import datetime
from typing import Optional
from pydantic import BaseModel


class MessageAckModel(BaseModel):
    count: int
    id: str