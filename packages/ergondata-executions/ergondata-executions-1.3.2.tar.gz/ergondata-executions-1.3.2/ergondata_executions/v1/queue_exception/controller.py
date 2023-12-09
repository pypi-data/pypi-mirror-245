import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.queue_exception.interfaces import *
from ergondata_executions.v1.decorators import *

class QueueExceptionController:

    CREATE_QUEUE_EXCEPTION_URL = "queues/{0}/exceptions"
    GET_QUEUE_EXCEPTIONS_URL = "queues/{0}/exceptions"
    DELETE_QUEUE_EXCEPTION_URL = "queues/{0}/exceptions/{1}"
    UPDATE_QUEUE_EXCEPTION_URL = "queues/{0}/exceptions/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating queue_exception {name}", out_schema=CreateQueueExceptionResponsePayload)
    def create_queue_exception(
        self,
        queue_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        queue_item_status_id: Literal["success", "business_exception", "system_error"],
        reprocess_within: StrictInt = 0,
        reprocess_outside: StrictInt = 0,
    ) -> CreateQueueExceptionResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_QUEUE_EXCEPTION_URL.format(queue_id)}",
            json=CreateQueueExceptionRequestPayload(
                name=name,
                description=description,
                queue_item_status_id=queue_item_status_id,
                reprocess_within=reprocess_within,
                reprocess_outside=reprocess_outside
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting queue_exception {queue_exception_id}", out_schema=DeleteQueueExceptionResponsePayload)
    def delete_queue_exception(
        self,
        queue_id: StrictStr,
        queue_exception_id: StrictStr
    ) -> DeleteQueueExceptionResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_QUEUE_EXCEPTION_URL.format(queue_id, queue_exception_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting queue_exceptions", out_schema=GetQueueExceptionsResponsePayload)
    def get_queue_exceptions(self, queue_id: StrictStr) -> GetQueueExceptionsResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_QUEUE_EXCEPTIONS_URL.format(queue_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating queue_exception {name}", out_schema=UpdateQueueExceptionResponsePayload)
    def update_queue_exception(
        self,
        queue_exception_id: StrictStr,
        queue_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        queue_item_status_id: Literal["success", "business_exception", "system_error"],
        reprocess_within: StrictInt = 0,
        reprocess_outside: StrictInt = 0,
    ) -> UpdateQueueExceptionResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_QUEUE_EXCEPTION_URL.format(queue_id, queue_exception_id)}",
            json=UpdateQueueExceptionRequestPayload(
                name=name,
                description=description,
                queue_item_status_id=queue_item_status_id,
                reprocess_within=reprocess_within,
                reprocess_outside=reprocess_outside
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
