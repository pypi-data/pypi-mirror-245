import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.queue_event_subscription.interfaces import *
from ergondata_executions.v1.decorators import *

class QueueEventSubscriptionController:

    CREATE_QUEUE_EVENT_SUBSCRIPTION_URL = "queues/{0}/events/subscriptions"
    GET_QUEUE_EVENT_SUBSCRIPTIONS_URL = "queues/{0}/events/subscriptions"
    DELETE_QUEUE_EVENT_SUBSCRIPTION_URL = "queues/{0}/events/subscriptions/{1}"
    UPDATE_QUEUE_EVENT_SUBSCRIPTION_URL = "queues/{0}/events/subscriptions/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating queue_event_subscription {event_id}", out_schema=CreateQueueEventSubscriptionResponsePayload)
    def create_queue_event_subscription(
        self,
        queue_id: StrictStr,
        event_id: StrictStr,
        payload: Any = None,
        whatsapp_integration: StrictBool = False,
        email_integration: StrictBool = False,
        webhook_integration: StrictBool = False,
        whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None,
        email_recipients: Optional[Union[List[StrictStr], None]] = None,
        webhook_url: Optional[Union[StrictStr, None]] = None,
        queue_exception_id: Optional[StrictStr] = None
    ) -> CreateQueueEventSubscriptionResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_QUEUE_EVENT_SUBSCRIPTION_URL.format(queue_id)}",
            json=CreateQueueEventSubscriptionRequestPayload(
                event_id=event_id,
                whatsapp_integration=whatsapp_integration,
                email_integration=email_integration,
                webhook_integration=webhook_integration,
                payload=payload,
                whatsapp_recipients=whatsapp_recipients,
                email_recipients=email_recipients,
                webhook_url=webhook_url,
                queue_exception_id=queue_exception_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting queue_event_subscription {queue_event_subscription_id}", out_schema=DeleteQueueEventSubscriptionResponsePayload)
    def delete_queue_event_subscription(
        self,
        queue_id: StrictStr,
        queue_event_subscription_id: StrictStr
    ) -> DeleteQueueEventSubscriptionResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_QUEUE_EVENT_SUBSCRIPTION_URL.format(queue_id, queue_event_subscription_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting queue_event_subscriptions", out_schema=GetQueueEventSubscriptionsResponsePayload)
    def get_queue_event_subscriptions(self, queue_id: StrictStr) -> GetQueueEventSubscriptionsResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_QUEUE_EVENT_SUBSCRIPTIONS_URL.format(queue_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating queue_event_subscription {queue_event_subscription_id}", out_schema=UpdateQueueEventSubscriptionResponsePayload)
    def update_queue_event_subscription(
        self,
        queue_event_subscription_id: StrictStr,
        queue_id: StrictStr,
        payload: Any = None,
        whatsapp_integration: StrictBool = False,
        email_integration: StrictBool = False,
        webhook_integration: StrictBool = False,
        whatsapp_recipients: Optional[Union[List[WhatsappRecipient], None]] = None,
        email_recipients: Optional[Union[List[StrictStr], None]] = None,
        webhook_url: Optional[Union[StrictStr, None]] = None,
        queue_exception_id: Optional[StrictStr] = None
    ) -> UpdateQueueEventSubscriptionResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_QUEUE_EVENT_SUBSCRIPTION_URL.format(queue_id, queue_event_subscription_id)}",
            json=UpdateQueueEventSubscriptionRequestPayload(
                whatsapp_integration=whatsapp_integration,
                email_integration=email_integration,
                webhook_integration=webhook_integration,
                payload=payload,
                whatsapp_recipients=whatsapp_recipients,
                email_recipients=email_recipients,
                webhook_url=webhook_url,
                queue_exception_id=queue_exception_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
