import logging

from pydantic import BaseModel, StrictStr, StrictInt, StrictBool
from typing import Union, Optional, Literal, List
from ergondata_executions.interfaces import APIBaseResponse
from ergondata_executions.v1.queue_item.interfaces import GetQueueItemsQueryParams

class AuthRequestPayload(BaseModel):
    username: StrictStr
    password: StrictStr
    client_id: StrictStr


class AuthSuccessResponsePayload(BaseModel):
    token: Optional[Union[StrictStr, None]]


class AuthResponsePayload(APIBaseResponse):
    token: Optional[StrictStr] = None


class Dispatcher(BaseModel):
    task_id: StrictStr
    target_queue_id: StrictStr


class ReporterSourceQueue(BaseModel):
    id: StrictStr
    query: GetQueueItemsQueryParams = None
    add_pages: Union[StrictInt, Literal["all"], None] = None


class Reporter(BaseModel):
    task_id: StrictStr
    source_queues: List[ReporterSourceQueue]


class Linear(BaseModel):
    task_id: StrictStr


class Performer(BaseModel):
    task_id: StrictStr
    source_queue_id: StrictStr


class PerformerAndDispatcher(BaseModel):
    task_id: StrictStr
    source_queue_id: StrictStr
    target_queue_id: StrictStr


class TaskExecutionConfig(BaseModel):
    dispatcher: Dispatcher = None
    performer: Performer = None
    performer_and_dispatcher: PerformerAndDispatcher = None


class APIConfig(BaseModel):
    task_exec_config: Union[Performer, Dispatcher, PerformerAndDispatcher, Linear, Reporter] = None
    api_timeout: StrictInt = 10
    enable_logs: bool = True,
    log_file_path: StrictStr = None
    log_level: Literal["info", "debug", "error", "warning"] = "debug"
    preserve_logger_handler: StrictBool = True