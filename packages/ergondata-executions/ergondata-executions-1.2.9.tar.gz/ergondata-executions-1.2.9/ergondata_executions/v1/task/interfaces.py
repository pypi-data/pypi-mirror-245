from datetime import datetime
from ergondata_executions.interfaces import *
from ergondata_executions.v1.workspace.interfaces import Workspace
from ergondata_executions.v1.process.interfaces import Process

class TaskStatus(BaseModel):
    id: Literal["success", "reset", "released", "business_exception", "system_error", "processing"]
    name: StrictStr


class Task(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    process: Process
    created_at: datetime
    updated_at: datetime


class CreateTaskRequestPayload(BaseModel):
    name: StrictStr
    description: StrictStr
    process_id: StrictStr
    task_type_id: Literal["dispatcher", "performer", "performer-and-dispatcher"]
    cron_schedule_expression: StrictStr
    cron_schedule_expression_description: StrictStr
    reset_ongoing_execution: StrictBool = False
    release_ongoing_execution: StrictBool = False
    timezone: StrictStr

class UpdateTaskRequestPayload(CreateTaskRequestPayload):
    pass

class CreateTaskResponsePayload(APIBaseResponse):
    data: Optional[Task] = None

class DeleteTaskResponsePayload(APIBaseResponse):
    task_id: Optional[StrictStr] = None


class GetTasksResponsePayload(APIBaseResponse):
    data: List[Task]

class UpdateTaskResponsePayload(CreateTaskResponsePayload):
    data: Workspace