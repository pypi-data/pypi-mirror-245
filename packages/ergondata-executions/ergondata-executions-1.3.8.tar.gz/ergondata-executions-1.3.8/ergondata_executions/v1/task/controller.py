import requests
from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.task.interfaces import *
from ergondata_executions.v1.decorators import *

class TaskController:

    CREATE_TASK_URL = "tasks"
    GET_TASKS_URL = "tasks"
    DELETE_TASK_URL = "tasks/{0}"
    UPDATE_TASK_URL = "tasks/{0}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating task {name}", out_schema=CreateTaskResponsePayload)
    def create_task(
        self,
        process_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        task_type_id: Literal["dispatcher", "performer", "performer-and-dispatcher"],
        cron_schedule_expression: StrictStr,
        timezone: StrictStr,
        cron_schedule_expression_description: StrictStr = None,
        reset_ongoing_execution: StrictBool = False,
        release_ongoing_execution: StrictBool = False,
    ) -> CreateTaskResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_URL}",
            json=CreateTaskRequestPayload(
                name=name,
                description=description,
                process_id=process_id,
                task_type_id=task_type_id,
                cron_schedule_expression_description=cron_schedule_expression_description,
                cron_schedule_expression=cron_schedule_expression,
                reset_ongoing_execution=reset_ongoing_execution,
                release_ongoing_execution=release_ongoing_execution,
                timezone=timezone
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting task {task_id}", out_schema=DeleteTaskResponsePayload)
    def delete_task(self, task_id: StrictStr) -> DeleteTaskResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_TASK_URL.format(task_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting tasks", out_schema=GetTasksResponsePayload)
    def get_tasks(self) -> GetTasksResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_TASKS_URL}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating task {name}", out_schema=UpdateTaskResponsePayload)
    def update_task(
        self,
        task_id: StrictStr,
        process_id: StrictStr,
        name: StrictStr,
        description: StrictStr,
        task_type_id: Literal["dispatcher", "performer", "performer-and-dispatcher"],
        cron_schedule_expression: StrictStr,
        cron_schedule_expression_description: StrictStr,
        timezone: StrictStr
    ) -> UpdateTaskResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_TASK_URL.format(task_id)}",
            json=UpdateTaskRequestPayload(
                name=name,
                description=description,
                process_id=process_id,
                task_type_id=task_type_id,
                cron_schedule_expression_description=cron_schedule_expression_description,
                cron_schedule_expression=cron_schedule_expression,
                timezone=timezone
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
