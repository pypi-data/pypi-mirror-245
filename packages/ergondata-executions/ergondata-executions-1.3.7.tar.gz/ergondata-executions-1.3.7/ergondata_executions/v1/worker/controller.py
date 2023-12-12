import requests

from ergondata_executions.v1.auth.controller import AuthController
from ergondata_executions.v1.worker.interfaces import *
from ergondata_executions.v1.decorators import *



class WorkerController:

    CREATE_WORKER_URL = "workers"
    GET_WORKERS_URL = "workers"
    DELETE_WORKER_URL = "workers/{0}"
    UPDATE_WORKER_URL = "workers/{0}"

    def __init__(self, api_client: AuthController):
        self.api_client = api_client

    @api_request(log_message="Creating worker", out_schema=CreateWorkerResponsePayload)
    def create_worker(self, friendlyName: StrictStr) -> CreateWorkerResponsePayload:
        res: Any = requests.post(
            url=f"{self.api_client.ROOT_URL}{self.CREATE_WORKER_URL}",
            json={"first_name": friendlyName},
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Deleting worker", out_schema=DeleteWorkerResponsePayload)
    def delete_worker(self, worker_id: StrictStr) -> DeleteWorkerResponsePayload:
        res: Any = requests.delete(
            url=f"{self.api_client.ROOT_URL}{self.DELETE_WORKER_URL.format(worker_id)}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res

    @api_request(log_message="Getting workers", out_schema=GetWorkersResponsePayload)
    def get_workers(self) -> GetWorkersResponsePayload:
        res: Any = requests.get(
            url=f"{self.api_client.ROOT_URL}{self.GET_WORKERS_URL}",
            headers=self.api_client.auth_header,
            timeout=self.api_client.timeout
        )
        return res
