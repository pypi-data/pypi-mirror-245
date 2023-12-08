import requests
from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.queue.interfaces import *
from ergondata_executions.v1.decorators import *

class QueueController:

    CREATE_QUEUE_URL = "queues"
    GET_QUEUES_URL = "queues"
    DELETE_QUEUE_URL = "queues/{0}"
    UPDATE_QUEUE_URL = "queues/{0}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating queue {name}", out_schema=CreateQueueResponsePayload)
    def create_queue(
        self,
        name: StrictStr,
        description: StrictStr,
        process_id: StrictStr,
        allow_to_include_repeated_queue_item: StrictBool = False,
        allow_to_include_repeated_queue_item_success: StrictBool = False,
        queue_item_max_retries_within_execution: StrictInt = 0,
        queue_item_max_retries_outside_execution: StrictInt = 0,
        skip_ongoing_queue_item: StrictBool = False
    ) -> CreateQueueResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_QUEUE_URL}",
            json=CreateQueueRequestPayload(
                name=name,
                description=description,
                process_id=process_id,
                allow_to_include_repeated_queue_item=allow_to_include_repeated_queue_item,
                allow_to_include_repeated_queue_item_success=allow_to_include_repeated_queue_item_success,
                queue_item_max_retries_within_execution=queue_item_max_retries_within_execution,
                queue_item_max_retries_outside_execution=queue_item_max_retries_outside_execution,
                skip_ongoing_queue_item=skip_ongoing_queue_item

            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting queue {queue_id}", out_schema=DeleteQueueResponsePayload)
    def delete_queue(self, queue_id: StrictStr) -> DeleteQueueResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_QUEUE_URL.format(queue_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting queues", out_schema=GetQueuesResponsePayload)
    def get_queues(self) -> GetQueuesResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_QUEUES_URL}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating queue {name}", out_schema=UpdateQueueResponsePayload)
    def update_queue(
        self,
        queue_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        process_id: StrictStr,
        allow_to_include_repeated_queue_item: StrictBool,
        allow_to_include_repeated_queue_item_success: StrictBool,
        queue_item_max_retries_within_execution: StrictInt,
        queue_item_max_retries_outside_execution: StrictInt,
        skip_ongoing_queue_item: StrictBool = False
    ) -> UpdateQueueResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_QUEUE_URL.format(queue_id)}",
            json=UpdateQueueRequestPayload(
                name=name,
                description=description,
                process_id=process_id,
                allow_to_include_repeated_queue_item=allow_to_include_repeated_queue_item,
                allow_to_include_repeated_queue_item_success=allow_to_include_repeated_queue_item_success,
                queue_item_max_retries_within_execution=queue_item_max_retries_within_execution,
                queue_item_max_retries_outside_execution=queue_item_max_retries_outside_execution,
                skip_ongoing_queue_item=skip_ongoing_queue_item
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
