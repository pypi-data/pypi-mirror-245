import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.task_execution_log.interfaces import *
from ergondata_executions.v1.decorators import *
from typing import Literal

class TaskExecutionLogController:

    CREATE_TASK_EXECUTION_LOG_URL = "tasks/{0}/executions/{1}/logs"
    GET_TASK_EXECUTION_LOGS_URL = "tasks/{0}/executions/{1}/logs"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(out_schema=CreateTaskExecutionLogResponse, log_response=False)
    def write_tk_exec_log(
        self,
        message: StrictStr,
        level: Literal["info", "warning", "error"] = "info",
        task_step_id: Optional[StrictStr] = None
    ) -> CreateTaskExecutionLogResponse:

        self.api_client.log(
            message=message,
            level=level
        )

        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_EXECUTION_LOG_URL.format(self.api_client.task_id, self.api_client.task_execution_id)}",
            json=CreateTaskExecutionLogRequest(
                message=message,
                level_id=level,
                task_step_id=task_step_id
            ).model_dump(),
            headers=self.api_client.exec_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting task execution logs", out_schema=GetTaskExecutionLogsResponse)
    def get_task_execution_logs(
        self,
        task_id: StrictStr,
        task_execution_id: StrictStr,
        page: StrictInt = 1,
        page_size: StrictInt = 100,
        message__contains: Optional[StrictStr] = None,
        message__starts_with: Optional[StrictStr] = None,
        message__regex: Optional[StrictStr] = None,
        level_id: Optional[StrictStr] = None,
        level_id__in: Optional[List[StrictStr]] = None,
        task_step_id__contains: Optional[StrictStr] = None,
        task_step_id__starts_with: Optional[StrictStr] = None,
        task_step_id__regex: Optional[StrictStr] = None,
        created_at_lte: Optional[datetime] = None,
        created_at_lt: Optional[datetime] = None,
        created_at_gt: Optional[datetime] = None,
        created_at_gte: Optional[datetime] = None,
    ) -> GetTaskExecutionLogsResponse:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_TASK_EXECUTION_LOGS_URL.format(task_id, task_execution_id)}",
            params=GetTaskExecutionLogsQueryParams(
                task_id=task_id,
                task_execution_id=task_execution_id,
                page=page,
                page_size=page_size,
                message__contains=message__contains,
                message__regex=message__regex,
                message__starts_with=message__starts_with,
                level_id=level_id,
                level_id__in=','.join(level_id__in),
                task_step_id__contains=task_step_id__contains,
                task_step_id__regex=task_step_id__regex,
                task_step_id__starts_with=task_step_id__starts_with,
                created_at_lte=created_at_lte,
                created_at_lt=created_at_lt,
                created_at_gt=created_at_gt,
                created_at_gte=created_at_gte

            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res