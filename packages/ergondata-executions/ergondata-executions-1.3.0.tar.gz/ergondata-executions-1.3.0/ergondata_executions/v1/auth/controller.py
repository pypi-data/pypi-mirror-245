import requests
from ergondata_executions.v1.auth.interfaces import *
from ergondata_executions.v1.api_logger import APILogger
from ergondata_executions.v1.queue_item.interfaces import QueueItem


class AuthController(APILogger):

    # ROOT_URL = "https://executions.ergondata.com.br/api/"
    ROOT_URL = "http://127.0.0.1:8000/api/v1/"
    AUTH_URL = "auth"

    auth_token: StrictStr = None
    task_execution_id: StrictStr = None
    task_id: StrictStr = None
    task_execution_token: StrictStr = None
    queue_item: QueueItem

    def __init__(
        self,
        auth: AuthRequestPayload,
        config: APIConfig = APIConfig()
    ):

        super(AuthController, self).__init__(
            enable_logs=config.enable_logs,
            log_file_path=config.log_file_path
        )

        self.auth = auth
        self.timeout = config.api_timeout
        self.auth_token = self.__authenticate().token
        self.exec_token = None
        self.config = config

    def set_task_execution(self, exec_token: StrictStr, task_id: StrictStr, task_execution_id: StrictStr):
        self.exec_token = exec_token
        self.task_id = task_id
        self.task_execution_id = task_execution_id


    @property
    def auth_header(self):
        return {"Authorization": f"Bearer {self.auth_token}"}

    @property
    def exec_header(self):
        return {"Authorization": f"Bearer {self.exec_token}"}

    def __authenticate(self) -> AuthResponsePayload:

        try:

            self.log_info(f"Authenticating user { self.auth.username }")

            res = requests.post(
                url=f"{self.ROOT_URL}{self.AUTH_URL}",
                json=self.auth.model_dump(),
                timeout=self.timeout
            )

            response = AuthResponsePayload(**res.json())

            if res.status_code == 200:
                self.log_info(response)
            else:
                self.log_error(response.message)

            return response

        except BaseException as e:

            self.log_error(f"Failed to authenticate user. {e}")
            response = AuthResponsePayload(
                status="error",
                message=str(e)
            )
            return response


