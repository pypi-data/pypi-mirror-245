from ergondata_executions.interfaces import *
from ergondata_executions.v1.queue.interfaces import Queue, QueueItemStatus
from ergondata_executions.v1.task_execution.interfaces import TaskExecution
from ergondata_executions.v1.task_exception.interfaces import TaskException
from ergondata_executions.v1.queue_priority.interfaces import QueuePriority
from typing import Any
from ergondata_executions.interfaces import APIPagination

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


class GetQueueItemsQueryParams(BaseModel):
    page: StrictInt = 1
    page_size: StrictInt = 100
    id: Optional[StrictStr] = None
    id__in: Optional[List[StrictStr]] = None
    external_id: Optional[StrictStr] = None
    external_id__in: Optional[List[StrictStr]] = None
    payload: Optional[StrictStr] = None
    payload__contains: Optional[StrictStr] = None
    payload__regex: Optional[StrictStr] = None
    task_producer_execution_id__exact: Optional[StrictStr] = None
    task_producer_execution_id__in: Optional[List[StrictStr]] = None
    task_consumer_execution_id__exact: Optional[StrictStr] = None
    task_consumer_execution_id__in: Optional[List[StrictStr]] = None
    processing_exception_id__exact: Optional[StrictStr] = None
    processing_exception_id__in: Optional[List[StrictStr]] = None
    processing_status_message__contains: Optional[StrictStr] = None
    processing_status_message__regex: Optional[StrictStr] = None
    max_retries_within_execution: Optional[StrictInt] = None
    max_retries_within_execution__lt: Optional[StrictInt] = None
    max_retries_within_execution__gt: Optional[StrictInt] = None
    max_retries_outside_execution: Optional[StrictInt] = None
    max_retries_outside_execution__gt: Optional[StrictInt] = None
    created_at__lte: Optional[datetime] = None
    created_at__lt: Optional[datetime] = None
    created_at__gt: Optional[datetime] = None
    created_at__gte: Optional[datetime] = None
    started_at__lte: Optional[datetime] = None
    started_at__lt: Optional[datetime] = None
    started_at__gt: Optional[datetime] = None
    started_at__gte: Optional[datetime] = None
    finished_at__lte: Optional[datetime] = None
    finished_at__lt: Optional[datetime] = None
    finished_at__gt: Optional[datetime] = None
    finished_at__gte: Optional[datetime] = None


class GetQueueItemsResponsePayload(APIBaseResponse):
    data: Optional[List[QueueItem]] = None
    pagination: Optional[APIPagination] = None


class GetQueueItemsReporter(BaseModel):
    queue_id: StrictStr
    data: List[QueueItem]