import logging

from pydantic import BaseModel, StrictStr, StrictInt
from typing import Union, Optional, Literal
from ergondata_executions.interfaces import APIBaseResponse


class AuthRequestPayload(BaseModel):
    username: StrictStr
    password: StrictStr
    client_id: StrictStr


class AuthTaskExecRequestPayload(AuthRequestPayload):
    task_id: StrictStr


class AuthSuccessResponsePayload(BaseModel):
    token: Optional[Union[StrictStr, None]]


class AuthResponsePayload(APIBaseResponse):
    token: Optional[StrictStr] = None


class APIConfig(BaseModel):
    api_timeout: StrictInt = 10
    enable_logs: bool = True,
    log_file_path: StrictStr = None
    log_level: Literal["info", "debug", "error", "warning"] = "debug"