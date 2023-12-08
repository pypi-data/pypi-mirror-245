from ergondata_executions.interfaces import *
from ergondata_executions.v1.task.interfaces import Task, TaskStatus
from ergondata_executions.v1.task_exception.interfaces import TaskException
from ergondata_executions.v1.worker.interfaces import Worker

class CreateTaskExecutionRequestPayload(BaseModel):
    dev_mode: Optional[StrictBool] = True
    processing_status_message: Optional[StrictStr] = None


class TaskExecution(BaseModel):
    id: StrictStr
    task: Task
    worker: Worker
    processing_status: TaskStatus
    processing_message: Optional[StrictStr] = None
    task_exception: Optional[TaskException] = None
    dev_mode: Optional[StrictBool] = True
    created_at: datetime
    finished_at: Optional[datetime] = None


class CreateTaskExecutionResponsePayload(APIBaseResponse):
    data: Optional[TaskExecution] = None
    exec_token: Optional[StrictStr] = None


class UpdateTaskExecutionRequestPayload(BaseModel):
    processing_status_id: Optional[Literal["business_exception", "system_error", "success", None]] = None
    processing_status_message: Optional[StrictStr] = None
    task_exception_id: Optional[StrictStr] = None


class UpdateTaskExecutionResponsePayload(APIBaseResponse):
    data: Optional[TaskExecution] = None


class GetTaskExecutionsQueryParams(BaseModel):
    page: StrictInt = 1
    page_size: StrictInt = 100
    id__in: Optional[List[StrictStr]] = None
    processing_status_id__exact: Optional[Literal["success", "system_error", "business_exception", "processing"]] = None
    processing_status_id__in: Optional[List[Literal["success", "system_error", "business_exception", "processing"]]] = None
    processing_exception_id__exact: Optional[StrictStr] = None
    processing_exception_id__in: Optional[List[StrictStr]] = None
    worker_id: Optional[StrictStr] = None
    worker_id__in: Optional[StrictStr] = None
    created_at_lte: Optional[datetime] = None
    created_at_lt: Optional[datetime] = None
    created_at_gt: Optional[datetime] = None
    created_at_gte: Optional[datetime] = None
    finished_at_lte: Optional[datetime] = None
    finished_at_lt: Optional[datetime] = None
    finished_at_gt: Optional[datetime] = None
    finished_at_gte: Optional[datetime] = None


class GetTaskExecutionsResponsePayload(APIBaseResponse):
    data: List[TaskExecution]