from datetime import datetime
from ergondata_executions.interfaces import *
from ergondata_executions.v1.task.interfaces import Task, TaskStatus
from pydantic import StrictFloat, validator


class TaskHighDurationEvent(BaseModel):
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

class TaskEventSubscription(BaseModel):
    id: StrictStr
    event: Any
    whatsapp_integration: StrictBool
    whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None
    email_integration: StrictBool
    email_recipients: Optional[Union[List[StrictStr], None]] = None
    webhook_integration: StrictBool
    webhook_url: Optional[Union[StrictStr, None]] = None
    task_exception_id: Optional[StrictStr] = None
    task: Task
    payload: Union[Any, TaskHighDurationEvent] = None
    created_at: datetime
    updated_at: datetime

class CreateTaskEventSubscriptionRequestPayload(BaseModel):
    event_id: StrictStr
    whatsapp_integration: StrictBool = False
    whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None
    email_integration: StrictBool = False
    email_recipients: Optional[Union[List[StrictStr], None]] = None
    webhook_integration: StrictBool = False
    webhook_url: Optional[Union[StrictStr, None]] = None
    task_exception_id: Optional[StrictStr] = None
    payload: Union[Any, TaskHighDurationEvent] = None


class UpdateTaskEventSubscriptionRequestPayload(CreateTaskEventSubscriptionRequestPayload):
    pass


class CreateTaskEventSubscriptionResponsePayload(APIBaseResponse):
    data: Optional[TaskEventSubscription] = None


class DeleteTaskEventSubscriptionResponsePayload(APIBaseResponse):
    process_id: Optional[StrictStr] = None


class GetTaskEventSubscriptionsResponsePayload(APIBaseResponse):
    data: List[TaskEventSubscription]


class UpdateTaskEventSubscriptionResponsePayload(CreateTaskEventSubscriptionResponsePayload):
    data: TaskEventSubscription

