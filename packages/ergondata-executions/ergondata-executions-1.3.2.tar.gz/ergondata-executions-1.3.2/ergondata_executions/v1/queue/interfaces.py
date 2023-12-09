from datetime import datetime
from ergondata_executions.interfaces import *
from ergondata_executions.v1.workspace.interfaces import Workspace
from ergondata_executions.v1.process.interfaces import Process

class QueueItemStatus(BaseModel):
    id: Literal["success", "reset", "released", "business_exception", "system_error", "processing", "pending"]
    name: StrictStr


class Queue(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    process_info: Process
    allow_to_include_repeated_queue_item: StrictBool
    allow_to_include_repeated_queue_item_success: StrictBool
    queue_item_max_retries_within_execution: StrictInt
    queue_item_max_retries_outside_execution: StrictInt
    created_at: datetime
    updated_at: datetime


class CreateQueueRequestPayload(BaseModel):
    name: StrictStr
    description: StrictStr
    process_id: StrictStr
    allow_to_include_repeated_queue_item: Optional[StrictBool] = False
    allow_to_include_repeated_queue_item_success: Optional[StrictBool] = False
    queue_item_max_retries_within_execution: Optional[StrictInt] = 0
    queue_item_max_retries_outside_execution: Optional[StrictInt] = 0
    skip_ongoing_queue_item: Optional[StrictBool] = False

class UpdateQueueRequestPayload(CreateQueueRequestPayload):
    pass

class CreateQueueResponsePayload(APIBaseResponse):
    data: Optional[Queue] = None

class DeleteQueueResponsePayload(APIBaseResponse):
    queue_id: Optional[StrictStr] = None


class GetQueuesResponsePayload(APIBaseResponse):
    data: List[Queue]

class UpdateQueueResponsePayload(CreateQueueResponsePayload):
    data: Workspace