from datetime import datetime
from ergondata_executions.interfaces import *
from ergondata_executions.v1.queue.interfaces import Queue, QueueItemStatus
from pydantic import StrictFloat, validator
from typing import Annotated


class QueueHighDurationEvent(BaseModel):
    duration_metric: Literal["absolute", "mean", "median"]
    duration_value: Union[StrictInt, StrictFloat]

    @validator('duration_value', pre=True, always=True)
    def check_duration_value(cls, duration_value, values):
        duration_metric = values.get('duration_metric')
        if duration_metric == "absolute":
            isinstance(duration_value, StrictInt)
        else:
            if not (duration_value, StrictFloat):
                raise ValidationError
            if duration_value > 1:
                raise ValidationError
            if duration_value < 0:
                raise ValidationError
        return duration_value

class QueueEventSubscription(BaseModel):
    id: StrictStr
    event: Any
    whatsapp_integration: StrictBool
    whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None
    email_integration: StrictBool
    email_recipients: Optional[Union[List[StrictStr], None]] = None
    webhook_integration: StrictBool
    webhook_url: Optional[Union[StrictStr, None]] = None
    queue_exception_id: Optional[StrictStr] = None
    queue: Queue
    payload: Union[Any, QueueHighDurationEvent] = None
    created_at: datetime
    updated_at: datetime

class CreateQueueEventSubscriptionRequestPayload(BaseModel):
    event_id: StrictStr
    whatsapp_integration: StrictBool = False
    whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None
    email_integration: StrictBool = False
    email_recipients: Optional[Union[List[StrictStr], None]] = None
    webhook_integration: StrictBool = False
    webhook_url: Optional[Union[StrictStr, None]] = None
    queue_exception_id: Optional[StrictStr] = None
    payload: Union[Any, QueueHighDurationEvent] = None


class UpdateQueueEventSubscriptionRequestPayload(BaseModel):
    whatsapp_integration: StrictBool = False
    whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None
    email_integration: StrictBool = False
    email_recipients: Optional[Union[List[StrictStr], None]] = None
    webhook_integration: StrictBool = False
    webhook_url: Optional[Union[StrictStr, None]] = None
    payload: Union[Any, QueueHighDurationEvent] = None


class CreateQueueEventSubscriptionResponsePayload(APIBaseResponse):
    data: Optional[QueueEventSubscription] = None


class DeleteQueueEventSubscriptionResponsePayload(APIBaseResponse):
    queue_event_subscription_id: Optional[StrictStr] = None


class GetQueueEventSubscriptionsResponsePayload(APIBaseResponse):
    data: List[QueueEventSubscription]


class UpdateQueueEventSubscriptionResponsePayload(CreateQueueEventSubscriptionResponsePayload):
    data: Optional[QueueEventSubscription] = None

