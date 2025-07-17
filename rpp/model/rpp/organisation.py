from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, RootModel, conlist
from enum import Enum

from rpp.model.rpp.common import BaseRequestModel
from rpp.model.rpp.entity import Card

class RoleStatusType(str, Enum):
    OK = "ok"
    CLIENT_LINK_PROHIBITED = "clientLinkProhibited"
    LINKED = "linked"
    SERVER_LINK_PROHIBITED = "serverLinkProhibited"

class OrganisationStatusType(str, Enum):
    OK = "ok"
    HOLD = "hold"
    TERMINATED = "terminated"
    CLIENT_DELETE_PROHIBITED = "clientDeleteProhibited"
    CLIENT_UPDATE_PROHIBITED = "clientUpdateProhibited"
    CLIENT_LINK_PROHIBITED = "clientLinkProhibited"
    LINKED = "linked"
    PENDING_CREATE = "pendingCreate"
    PENDING_UPDATE = "pendingUpdate"
    PENDING_DELETE = "pendingDelete"
    SERVER_DELETE_PROHIBITED = "serverDeleteProhibited"
    SERVER_UPDATE_PROHIBITED = "serverUpdateProhibited"
    SERVER_LINK_PROHIBITED = "serverLinkProhibited"


class OrganisationModel(BaseModel):
    name: str
    date: datetime


class OrganisationInfoRequest(BaseRequestModel):
    id: str

class OrganisationInfoResponse(BaseModel):
    pass

class OrganisationCheckRequest(BaseRequestModel):
    id: str

class OrganisationCheckResponse(BaseModel):
    pass

class OrganisationDeleteRequest(BaseRequestModel):
    id: str

class OrganisationUpdateRequest(BaseRequestModel):
    id: str

class OrganisationRole(BaseModel):
    type: str
    status: Optional[List[RoleStatusType]] = None
    roleID: Optional[str] = None

class OrganisationContact(BaseModel):
    type: str
    id: str

class LinkType(BaseModel):
    uri: str

class LinksType(RootModel[Dict[str, LinkType]]):
    pass

class OrganisationCard(Card):
    links: Optional[LinksType] = None

class OrganisationCreateRequest(BaseRequestModel):
    id: str
    role: OrganisationRole
    status: Optional[List[OrganisationStatusType]] = None
    parentId: Optional[str] = None
    contacts: Optional[List[OrganisationContact]] = None
    cards: Optional[List[OrganisationCard]] = Field(default=None, max_length=2)

class OrganisationCreateResponse(BaseModel):
    id: Optional[str] = None
    createDate: Optional[datetime] = None

class OrganisationUpdateAddOrRemove(BaseModel):
    status: List[str]

class OrganisationUpdateChange(BaseModel):
    contact: List[Card] 

class OrganisationUpdateRequest(BaseRequestModel):
    id: str
    add: Optional[OrganisationUpdateAddOrRemove] = None
    remove: Optional[OrganisationUpdateAddOrRemove] = None
    change: Optional[OrganisationUpdateChange] = None