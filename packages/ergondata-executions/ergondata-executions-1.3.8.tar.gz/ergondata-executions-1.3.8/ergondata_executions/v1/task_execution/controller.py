import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.task_execution.interfaces import *
from ergondata_executions.v1.decorators import *

class TaskExecutionController:

    CREATE_TASK_EXECUTION_URL = "tasks/{0}/executions"
    GET_TASK_EXECUTIONS_URL = "tasks/{0}/executions"
    DELETE_TASK_EXECUTION_URL = "tasks/{0}/executions/{1}"
    UPDATE_TASK_EXECUTION_URL = "tasks/{0}/executions/{1}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating task execution", out_schema=CreateTaskExecutionResponsePayload, exec_token=True)
    def create_task_execution(
        self,
        task_id: StrictStr,
        dev_mode: StrictBool = True,
        processing_status_message: StrictBool = None
    ) -> CreateTaskExecutionResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_TASK_EXECUTION_URL.format(task_id)}",
            json=CreateTaskExecutionRequestPayload(
                dev_mode=dev_mode,
                processing_status_message=processing_status_message
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating task execution  status", out_schema=UpdateTaskExecutionResponsePayload)
    def update_task_execution(
        self,
        task_execution_id: StrictStr = None,
        task_id: StrictStr = None,
        processing_status_id: Literal["success", "system_error", "business_exception", None] = None,
        task_exception_id: StrictStr = None,
        processing_status_message: StrictStr = None
    ) -> UpdateTaskExecutionResponsePayload:
        if task_execution_id:
            url = self.UPDATE_TASK_EXECUTION_URL.format(task_id, task_execution_id)
        else:
            url = self.UPDATE_TASK_EXECUTION_URL.format(self.api_client.task_id, self.api_client.task_execution_id)
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{url}",
            json=UpdateTaskExecutionRequestPayload(
                task_exception_id=task_exception_id,
                processing_status_message=processing_status_message,
                processing_status_id=processing_status_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting task executions", out_schema=GetTaskExecutionsResponsePayload)
    def get_task_executions(
        self,
        task_id: StrictStr,
        page: StrictInt = 1,
        page_size: StrictInt = 100,
        id__in: Optional[List[StrictStr]] = None,
        processing_status_id__exact: Optional[Literal["success", "system_error", "business_exception", "processing"]] = None,
        processing_status_id__in: Optional[List[Literal["success", "system_error", "business_exception", "processing", "reset", "released"]]] = None,
        processing_exception_id__exact: Optional[StrictStr] = None,
        processing_exception_id__in: Optional[List[StrictStr]] = None,
        worker_id: Optional[StrictStr] = None,
        worker_id__in: Optional[StrictStr] = None,
        created_at_lte: Optional[datetime] = None,
        created_at_lt: Optional[datetime] = None,
        created_at_gt: Optional[datetime] = None,
        created_at_gte: Optional[datetime] = None,
        finished_at_lte: Optional[datetime] = None,
        finished_at_lt: Optional[datetime] = None,
        finished_at_gt: Optional[datetime] = None,
        finished_at_gte: Optional[datetime] = None
    ) -> GetTaskExecutionsResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_TASK_EXECUTIONS_URL.format(task_id)}",
            params=GetTaskExecutionsQueryParams(
                page=page,
                page_size=page_size,
                id__in=id__in,
                processing_status_id__exact=processing_status_id__exact,
                processing_status_id__in=processing_status_id__in,
                processing_exception_id__exact=processing_exception_id__exact,
                processing_exception_id__in=processing_exception_id__in,
                worker_id=worker_id,
                worker_id__in=worker_id__in,
                created_at_lte=created_at_lte,
                created_at_lt=created_at_lt,
                created_at_gt=created_at_gt,
                created_at_gte=created_at_gte,
                finished_at_lte=finished_at_lte,
                finished_at_lt=finished_at_lt,
                finished_at_gt=finished_at_gt,
                finished_at_gte=finished_at_gte

            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res