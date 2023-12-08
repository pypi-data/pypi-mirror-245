from datetime import datetime
from ergondata_executions.interfaces import *
from ergondata_executions.v1.task.interfaces import Task, TaskStatus

class TaskException(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    task: Task
    task_status: TaskStatus
    created_at: datetime
    updated_at: datetime


class CreateTaskExceptionRequestPayload(BaseModel):
    name: StrictStr
    description: StrictStr
    task_status_id: Literal["success", "business_exception", "system_error"]


class UpdateTaskExceptionRequestPayload(CreateTaskExceptionRequestPayload):
    pass

class CreateTaskExceptionResponsePayload(APIBaseResponse):
    data: Optional[TaskException] = None

class DeleteTaskExceptionResponsePayload(APIBaseResponse):
    process_id: Optional[StrictStr] = None


class GetTaskExceptionsResponsePayload(APIBaseResponse):
    data: List[TaskException]

class UpdateTaskExceptionResponsePayload(CreateTaskExceptionResponsePayload):
    data: TaskException