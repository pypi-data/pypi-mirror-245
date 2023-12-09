import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.task_exception.interfaces import *
from ergondata_executions.v1.decorators import *

class TaskExceptionController:

    CREATE_TASK_EXCEPTION_URL = "tasks/{0}/exceptions"
    GET_TASK_EXCEPTIONS_URL = "tasks/{0}/exceptions"
    DELETE_TASK_EXCEPTION_URL = "tasks/{0}/exceptions/{1}"
    UPDATE_TASK_EXCEPTION_URL = "tasks/{0}/exceptions/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating task_exception {name}", out_schema=CreateTaskExceptionResponsePayload)
    def create_task_exception(
        self,
        task_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        task_status_id: Literal["success", "business_exception", "system_error"]
    ) -> CreateTaskExceptionResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_EXCEPTION_URL.format(task_id)}",
            json=CreateTaskExceptionRequestPayload(
                name=name,
                description=description,
                task_status_id=task_status_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting task_exception {task_exception_id}", out_schema=DeleteTaskExceptionResponsePayload)
    def delete_task_exception(
        self,
        task_id: StrictStr,
        task_exception_id: StrictStr
    ) -> DeleteTaskExceptionResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_TASK_EXCEPTION_URL.format(task_id, task_exception_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting task_exceptions", out_schema=GetTaskExceptionsResponsePayload)
    def get_task_exceptions(self, task_id: StrictStr) -> GetTaskExceptionsResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_TASK_EXCEPTIONS_URL.format(task_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating task_exception {name}", out_schema=UpdateTaskExceptionResponsePayload)
    def update_task_exception(
        self,
        task_exception_id: StrictStr,
        task_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        task_status_id: Literal["success", "reset", "released", "business_exception", "system_error"]
    ) -> UpdateTaskExceptionResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_TASK_EXCEPTION_URL.format(task_id, task_exception_id)}",
            json=UpdateTaskExceptionRequestPayload(
                name=name,
                description=description,
                task_status_id=task_status_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
