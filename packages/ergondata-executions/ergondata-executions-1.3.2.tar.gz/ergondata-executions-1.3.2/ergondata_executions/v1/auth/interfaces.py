import logging

from pydantic import BaseModel, StrictStr, StrictInt
from typing import Union, Optional, Literal
from ergondata_executions.interfaces import APIBaseResponse


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
    task_exec_config: Union[Performer, Dispatcher, PerformerAndDispatcher, Linear] = None
    api_timeout: StrictInt = 10
    enable_logs: bool = True,
    log_file_path: StrictStr = None
    log_level: Literal["info", "debug", "error", "warning"] = "debug"