from ergondata_executions.interfaces import *
from ergondata_executions.v1.queue.interfaces import Queue, QueueItemStatus
from ergondata_executions.v1.task_execution.interfaces import TaskExecution
from ergondata_executions.v1.task_exception.interfaces import TaskException
from ergondata_executions.v1.queue_priority.interfaces import QueuePriority
from typing import Any

class QueueItem(BaseModel):
    id: StrictStr
    external_id: Optional[StrictStr] = None
    processing_status: QueueItemStatus
    processing_status_message: Optional[StrictStr] = None
    processing_exception: Optional[TaskException] = None
    processing_exception_ids: Optional[List[StrictStr]] = None
    processing_priority: Optional[QueuePriority] = None
    payload: Any
    queue: Queue
    task_producer_execution: Optional[TaskExecution] = None
    task_consumer_execution: Optional[TaskExecution] = None
    retries_within_count: StrictInt
    retries_outside_count: StrictInt


class CreateQueueItemRequestPayload(BaseModel):
    payload: Any
    external_id: Optional[StrictStr] = None
    processing_status_id: Optional[Literal["pending", "success", "system_error", "business_exception"]] = "pending"
    processing_status_message: Optional[StrictStr] = None
    processing_exception_id: Optional[StrictStr] = None
    processing_priority_id: Optional[StrictStr] = None


class CreateQueueItemResponsePayload(APIBaseResponse):
    data: Optional[Union[QueueItem, None]] = None


class GetQueueItemQueryParams(BaseModel):
    priority_id__in: Optional[list[StrictStr]] = None
    external_id: Optional[StrictStr] = None


class GetQueueItemResponsePayload(APIBaseResponse):
    data: Optional[QueueItem] = None


class UpdateQueueItemRequestPayload(BaseModel):
    payload: Optional[Any] = None
    processing_status_id: Optional[Literal["success", "system_error", "business_exception"]] = None
    processing_status_message: Optional[StrictStr] = None
    processing_exception_id: Optional[StrictStr] = None


class UpdateQueueItemResponsePayload(CreateQueueItemResponsePayload):
    pass