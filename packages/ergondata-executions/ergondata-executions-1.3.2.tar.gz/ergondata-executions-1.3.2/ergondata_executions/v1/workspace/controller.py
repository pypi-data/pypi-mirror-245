import requests
from ergondata_executions.v1.workspace.interfaces import *
from ergondata_executions.v1.decorators import api_request
from ergondata_executions.v1.auth.controller import AuthController

class WorkspaceController:

    CREATE_WK_URL = "workspaces"
    GET_WKS_URL = "workspaces"
    DELETE_WK_URL = "workspaces/{0}"
    UPDATE_WK_URL = "workspaces/{0}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(out_schema=CreateWKResponsePayload, log_message="Creating workspace {name}")
    def create_workspace(self, name: StrictStr, description: StrictStr) -> CreateWKResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_WK_URL}",
            json=CreateWkRequestPayload(
                name=name,
                description=description
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting workspace {workspace_id}", out_schema=DeleteWKResponsePayload)
    def delete_workspace(self, workspace_id: StrictStr) -> DeleteWKResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_WK_URL.format(workspace_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting workspaces", out_schema=GetWorkspacesResponsePayload)
    def get_workspaces(self) -> GetWorkspacesResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_WKS_URL}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Updating workspace {name}", out_schema=UpdateWorkspaceResponsePayload)
    def update_workspace(self, workspace_id: StrictStr, name: StrictStr, description: StrictStr) -> UpdateWorkspaceResponsePayload:
        res: Any = requests.put(
            url=f"{self.api_client.ROOT_URL}{self.UPDATE_WK_URL.format(workspace_id)}",
            json=UpdateWkRequestPayload(
                name=name,
                description=description
            ).model_dump(),
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
