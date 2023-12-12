import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.queue_priority.interfaces import *
from ergondata_executions.v1.decorators import *

class QueuePriorityController:

    CREATE_QUEUE_PRIORITY_URL = "queues/{0}/priorities"
    GET_QUEUE_PRIORITIES_URL = "queues/{0}/priorities"
    DELETE_QUEUE_PRIORITY_URL = "queues/{0}/priorities/{1}"
    UPDATE_QUEUE_PRIORITY_URL = "queues/{0}/priorities/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating queue_priority {name}", out_schema=CreateQueuePriorityResponsePayload)
    def create_queue_priority(
        self,
        queue_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
    ) -> CreateQueuePriorityResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_QUEUE_PRIORITY_URL.format(queue_id)}",
            json=CreateQueuePriorityRequestPayload(
                name=name,
                description=description
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting queue_priority {queue_priority_id}", out_schema=DeleteQueuePriorityResponsePayload)
    def delete_queue_priority(
        self,
        queue_id: StrictStr,
        queue_priority_id: StrictStr
    ) -> DeleteQueuePriorityResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_QUEUE_PRIORITY_URL.format(queue_id, queue_priority_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting queue_priorities", out_schema=GetQueuePrioritiesResponsePayload)
    def get_queue_priorities(self, queue_id: StrictStr) -> GetQueuePrioritiesResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_QUEUE_PRIORITIES_URL.format(queue_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating queue_priority {name}", out_schema=UpdateQueuePriorityResponsePayload)
    def update_queue_priority(
        self,
        queue_priority_id: StrictStr,
        queue_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
    ) -> UpdateQueuePriorityResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_QUEUE_PRIORITY_URL.format(queue_id, queue_priority_id)}",
            json=UpdateQueuePriorityRequestPayload(
                name=name,
                description=description,
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
