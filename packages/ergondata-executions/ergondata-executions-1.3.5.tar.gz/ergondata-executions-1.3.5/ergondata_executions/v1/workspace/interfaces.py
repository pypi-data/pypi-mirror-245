from datetime import datetime
from pydantic import BaseModel, StrictStr, StrictInt, Field
from ergondata_executions.interfaces import *

class Workspace(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    created_at: datetime
    updated_at: datetime


class CreateWkRequestPayload(BaseModel):
    name: StrictStr
    description: StrictStr

class UpdateWkRequestPayload(CreateWkRequestPayload):
    pass

class CreateWKResponsePayload(APIBaseResponse):
    data: Optional[Workspace] = None

class DeleteWKResponsePayload(APIBaseResponse):
    workspace_id: Optional[StrictStr] = None


class GetWorkspacesResponsePayload(APIBaseResponse):
    data: List[Workspace]

class UpdateWorkspaceResponsePayload(CreateWKResponsePayload):
    pass