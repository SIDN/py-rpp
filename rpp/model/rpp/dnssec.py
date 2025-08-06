from typing import List, Optional
from pydantic import BaseModel


class SecDNSKeyDataModel(BaseModel):
    flags: int
    protocol: int
    alg: int
    pubKey: str

class DSDataModel(BaseModel):
    keyTag: int
    algorithm: int
    digestType: int
    digest: str

class DNSSECModel(BaseModel):
    delegationSigned: bool
    dsData: List[DSDataModel]

class DsOrKeyType(BaseModel):
    keyData: Optional[List[SecDNSKeyDataModel]] = None
    dsData: Optional[List[DSDataModel]] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.keyData is not None and self.dsData is not None:
            raise ValueError("Only one of keyData or dsData can be set.")
        if self.keyData is None and self.dsData is None:
            raise ValueError("One of keyData or dsData must be set.")