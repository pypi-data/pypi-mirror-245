import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.queue_item.interfaces import *
from ergondata_executions.v1.decorators import *

class QueueItemController:

    CREATE_QUEUE_ITEM_URL = "queues/{0}/items"
    GET_QUEUE_ITEM_URL = "queues/{0}/item"
    DELETE_QUEUE_EXCEPTION_URL = "queues/{0}/exceptions/{1}"
    UPDATE_QUEUE_ITEM_URL = "queues/{0}/items/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating queue item", out_schema=CreateQueueItemResponsePayload)
    def create_queue_item(
        self,
        queue_id: StrictStr,
        payload: Any,
        external_id: StrictStr = None,
        processing_status_id: Union[StrictStr, None] = "pending",
        processing_exception_id: StrictStr = None,
        processing_priority_id: StrictStr = None,
        processing_status_message: StrictStr = None,

    ) -> CreateQueueItemResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_QUEUE_ITEM_URL.format(queue_id)}",
            json=CreateQueueItemRequestPayload(
                external_id=external_id,
                payload=payload,
                processing_status_id=processing_status_id,
                processing_priority_id=processing_priority_id,
                processing_status_message=processing_status_message,
                processing_exception_id=processing_exception_id
            ).model_dump(),
            headers=self.api_client.exec_header if self.api_client.exec_token else self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting queue item", out_schema=GetQueueItemResponsePayload, queue_item=True)
    def get_queue_item(
        self,
        queue_id: StrictStr,
        external_id: StrictStr = None,
        priority_id__in: List[StrictStr] = None
    ) -> GetQueueItemResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_QUEUE_ITEM_URL.format(queue_id)}",
            params=GetQueueItemQueryParams(
                external_id=external_id,
                priority_id__in=priority_id__in
            ).model_dump(),
            headers=self.api_client.exec_header if self.api_client.exec_token else self.api_client.auth_header
        )
        return res

    @api_request(log_message="Updating queue item", out_schema=UpdateQueueItemResponsePayload)
    def update_queue_item(
        self,
        queue_item_id: StrictStr,
        queue_id: StrictStr,
        payload: Any = None,
        processing_status_id: StrictStr = None,
        processing_exception_id: StrictStr = None,
        processing_status_message: StrictStr = None,
    ) -> UpdateQueueItemResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_QUEUE_ITEM_URL.format(queue_id, queue_item_id)}",
            json=UpdateQueueItemRequestPayload(
                payload=payload,
                processing_status_id=processing_status_id,
                processing_exception_id=processing_exception_id,
                processing_status_message=processing_status_message
            ).model_dump(),
            headers=self.api_client.exec_header if self.api_client.exec_token else self.api_client.auth_header
        )
        return res