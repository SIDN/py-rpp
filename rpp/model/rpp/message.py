from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, IPvAnyAddress


class MessageModel(BaseModel):
    code: int
    count: Optional[int] = None
    data: Optional[object] = None
    clientId: Optional[str] = None
    serverId: Optional[str] = None
