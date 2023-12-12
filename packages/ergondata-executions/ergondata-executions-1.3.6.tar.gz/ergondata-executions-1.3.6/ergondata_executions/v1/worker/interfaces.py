from ergondata_executions.interfaces import *

class WorkerUser(BaseModel):
    id: StrictStr
    friendly_name: StrictStr = Field(alias="first_name")
    client: Client
    type: UserType
    created_at: datetime


class Worker(BaseModel):
    id: StrictStr
    user: WorkerUser
    created_at: datetime
    updated_at: datetime


class CreateWorkerResponsePayload(APIBaseResponse):
    data: Optional[Worker] = None


class DeleteWorkerResponsePayload(APIBaseResponse):
    worker_id: StrictStr


class GetWorkersResponsePayload(APIBaseResponse):
    data: list[Worker]
