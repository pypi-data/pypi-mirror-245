from ergondata_executions.interfaces import *
from ergondata_executions.v1.task_execution.interfaces import TaskExecution


class TaskExecutionLogLevel(BaseModel):
    id: StrictStr
    name: StrictStr


class TaskExecutionLog(BaseModel):
    id: StrictStr
    message: StrictStr
    task_execution: StrictStr
    level: TaskExecutionLogLevel
    task_step_id: Union[StrictStr, None] = None
    created_at: datetime


class CreateTaskExecutionLogResponse(APIBaseResponse):
    data: Optional[TaskExecutionLog] = None


class CreateTaskExecutionLogRequest(BaseModel):
    level_id: Literal["info", "warning", "error"]
    message: StrictStr
    task_step_id: Optional[StrictStr] = None


class GetTaskExecutionLogsResponse(APIBaseResponse):
    data: Optional[List[TaskExecutionLog]]
    
    
class GetTaskExecutionLogsQueryParams(BaseModel):
    task_id: StrictStr
    task_execution_id: StrictStr
    page: StrictInt = 1
    page_size: StrictInt = 100
    message__contains: Optional[StrictStr] = None
    message__starts_with: Optional[StrictStr] = None
    message__regex: Optional[StrictStr] = None
    level_id: Optional[StrictStr] = None
    level_id__in: Optional[StrictStr] = None,
    task_step_id__contains: Optional[StrictStr] = None
    task_step_id__starts_with: Optional[StrictStr] = None
    task_step_id__regex: Optional[StrictStr] = None
    created_at_lte: Optional[datetime] = None
    created_at_lt: Optional[datetime] = None
    created_at_gt: Optional[datetime] = None
    created_at_gte: Optional[datetime] = None