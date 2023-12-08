import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.task_event_subscription.interfaces import *
from ergondata_executions.v1.decorators import *

class TaskEventSubscriptionController:

    CREATE_TASK_EVENT_SUBSCRIPTION_URL = "tasks/{0}/events/subscriptions"
    GET_TASK_EVENT_SUBSCRIPTIONS_URL = "tasks/{0}/events/subscriptions"
    DELETE_TASK_EVENT_SUBSCRIPTION_URL = "tasks/{0}/events/subscriptions/{1}"
    UPDATE_TASK_EVENT_SUBSCRIPTION_URL = "tasks/{0}/events/subscriptions/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating task_event_subscription {event_id}", out_schema=CreateTaskEventSubscriptionResponsePayload)
    def create_task_event_subscription(
        self,
        task_id: StrictStr,
        event_id: StrictStr,
        payload: Any = None,
        whatsapp_integration: StrictBool = False,
        email_integration: StrictBool = False,
        webhook_integration: StrictBool = False,
        whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None,
        email_recipients: Optional[Union[List[StrictStr], None]] = None,
        webhook_url: Optional[Union[StrictStr, None]] = None,
        task_exception_id: Optional[StrictStr] = None
    ) -> CreateTaskEventSubscriptionResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_EVENT_SUBSCRIPTION_URL.format(task_id)}",
            json=CreateTaskEventSubscriptionRequestPayload(
                event_id=event_id,
                whatsapp_integration=whatsapp_integration,
                email_integration=email_integration,
                webhook_integration=webhook_integration,
                payload=payload,
                whatsapp_recipients=whatsapp_recipients,
                email_recipients=email_recipients,
                webhook_url=webhook_url,
                task_exception_id=task_exception_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting task_event_subscription {task_event_subscription_id}", out_schema=DeleteTaskEventSubscriptionResponsePayload)
    def delete_task_event_subscription(
        self,
        task_id: StrictStr,
        task_event_subscription_id: StrictStr
    ) -> DeleteTaskEventSubscriptionResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_TASK_EVENT_SUBSCRIPTION_URL.format(task_id, task_event_subscription_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting task_event_subscriptions", out_schema=GetTaskEventSubscriptionsResponsePayload)
    def get_task_event_subscriptions(self, task_id: StrictStr) -> GetTaskEventSubscriptionsResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_TASK_EVENT_SUBSCRIPTIONS_URL.format(task_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating task_event_subscription {task_event_subscription_id}", out_schema=UpdateTaskEventSubscriptionResponsePayload)
    def update_task_event_subscription(
        self,
        task_event_subscription_id: StrictStr,
        task_id: StrictStr,
        event_id: StrictStr,
        payload: Any = None,
        whatsapp_integration: StrictBool = False,
        email_integration: StrictBool = False,
        webhook_integration: StrictBool = False,
        whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None,
        email_recipients: Optional[Union[List[StrictStr], None]] = None,
        webhook_url: Optional[Union[StrictStr, None]] = None,
        task_exception_id: Optional[StrictStr] = None
    ) -> UpdateTaskEventSubscriptionResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_TASK_EVENT_SUBSCRIPTION_URL.format(task_id, task_event_subscription_id)}",
            json=UpdateTaskEventSubscriptionRequestPayload(
                event_id=event_id,
                whatsapp_integration=whatsapp_integration,
                email_integration=email_integration,
                webhook_integration=webhook_integration,
                payload=payload,
                whatsapp_recipients=whatsapp_recipients,
                email_recipients=email_recipients,
                webhook_url=webhook_url,
                task_exception_id=task_exception_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
