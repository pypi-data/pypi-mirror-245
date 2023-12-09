from ergondata_executions.interfaces import *
from ergondata_executions.v1.queue.interfaces import Queue, QueueItemStatus

class QueuePriority(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    queue: Queue
    created_at: datetime
    updated_at: datetime


class CreateQueuePriorityRequestPayload(BaseModel):
    name: StrictStr
    description: StrictStr


class UpdateQueuePriorityRequestPayload(BaseModel):
    name: StrictStr
    description: StrictStr

class CreateQueuePriorityResponsePayload(APIBaseResponse):
    data: Optional[QueuePriority] = None

class DeleteQueuePriorityResponsePayload(APIBaseResponse):
    queue_priority_id: Optional[StrictStr] = None


class GetQueuePrioritiesResponsePayload(APIBaseResponse):
    data: List[QueuePriority]

class UpdateQueuePriorityResponsePayload(CreateQueuePriorityResponsePayload):
    data: Optional[QueuePriority] = None