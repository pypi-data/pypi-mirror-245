from datetime import datetime
from ergondata_executions.interfaces import *
from ergondata_executions.v1.workspace.interfaces import Workspace

class Process(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    workspace: Optional[Workspace] = None
    created_at: datetime
    updated_at: datetime


class CreateProcessRequestPayload(BaseModel):
    name: StrictStr
    description: StrictStr
    workspace_id: StrictStr

class UpdateProcessRequestPayload(CreateProcessRequestPayload):
    pass

class CreateProcessResponsePayload(APIBaseResponse):
    data: Optional[Process] = None

class DeleteProcessResponsePayload(APIBaseResponse):
    process_id: Optional[StrictStr] = None


class GetProcessResponsePayload(APIBaseResponse):
    data: List[Process]

class UpdateProcessResponsePayload(CreateProcessResponsePayload):
    data: Workspace