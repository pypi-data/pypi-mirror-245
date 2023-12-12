import requests
from requests import Response

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.process.interfaces import *
from ergondata_executions.v1.decorators import *

class ProcessController:

    CREATE_PROCESS_URL = "processes"
    GET_PROCESSES_URL = "processes"
    DELETE_PROCESS_URL = "processes/{0}"
    UPDATE_PROCESS_URL = "processes/{0}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating process {name}", out_schema=CreateProcessResponsePayload)
    def create_process(self, workspace_id: StrictStr, name: StrictStr, description: StrictStr) -> CreateProcessResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_PROCESS_URL}",
            json=CreateProcessRequestPayload(
                name=name,
                description=description,
                workspace_id=workspace_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting process {process_id}", out_schema=DeleteProcessResponsePayload)
    def delete_process(self, process_id: StrictStr) -> DeleteProcessResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_PROCESS_URL.format(process_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting processes", out_schema=GetProcessResponsePayload)
    def get_processes(self) -> GetProcessResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_PROCESSES_URL}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating process {name}", out_schema=UpdateProcessResponsePayload)
    def update_process(
        self,
        process_id: StrictStr,
        workspace_id: StrictStr,
        name: StrictStr,
        description: StrictStr
    ) -> UpdateProcessResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_PROCESS_URL.format(process_id)}",
            json=UpdateProcessRequestPayload(
                name=name,
                description=description,
                workspace_id=workspace_id
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
