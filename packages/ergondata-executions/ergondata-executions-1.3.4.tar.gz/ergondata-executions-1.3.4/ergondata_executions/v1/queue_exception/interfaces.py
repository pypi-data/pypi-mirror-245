from ergondata_executions.interfaces import *
from ergondata_executions.v1.queue.interfaces import Queue, QueueItemStatus

class QueueException(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    queue: Queue
    queue_item_status: QueueItemStatus
    created_at: datetime
    updated_at: datetime


class CreateQueueExceptionRequestPayload(BaseModel):
    name: StrictStr
    description: StrictStr
    queue_item_status_id: Literal["success", "business_exception", "system_error"]
    reprocess_within: Optional[StrictBool] = False
    reprocess_outside: Optional[StrictBool] = False


class UpdateQueueExceptionRequestPayload(CreateQueueExceptionRequestPayload):
    pass

class CreateQueueExceptionResponsePayload(APIBaseResponse):
    data: Optional[QueueException] = None

class DeleteQueueExceptionResponsePayload(APIBaseResponse):
    process_id: Optional[StrictStr] = None


class GetQueueExceptionsResponsePayload(APIBaseResponse):
    data: List[QueueException]

class UpdateQueueExceptionResponsePayload(CreateQueueExceptionResponsePayload):
    data: Optional[QueueException] = None