import wrapt

from ergondata_executions.v1.auth.controller import *
from ergondata_executions.v1.auth.interfaces import AuthRequestPayload
from ergondata_executions.v1.workspace.controller import WorkspaceController
from ergondata_executions.v1.process.controller import ProcessController
from ergondata_executions.v1.task.controller import TaskController
from ergondata_executions.v1.task_exception.controller import TaskExceptionController
from ergondata_executions.v1.task_event_subscription.controller import TaskEventSubscriptionController
from ergondata_executions.v1.worker.controller import WorkerController
from ergondata_executions.v1.task_execution.controller import TaskExecutionController
from ergondata_executions.v1.task_execution_log.controller import TaskExecutionLogController
from ergondata_executions.v1.queue.controller import QueueController
from ergondata_executions.v1.queue_exception.controller import QueueExceptionController
from ergondata_executions.v1.queue_event_subscription.controller import QueueEventSubscriptionController
from ergondata_executions.v1.queue_priority.controller import QueuePriorityController
from ergondata_executions.v1.queue_item.controller import QueueItemController



class ErgonClient(
    WorkspaceController,
    ProcessController,
    TaskController,
    TaskExceptionController,
    TaskEventSubscriptionController,
    WorkerController,
    TaskExecutionController,
    TaskExecutionLogController,
    QueueController,
    QueueExceptionController,
    QueueEventSubscriptionController,
    QueuePriorityController,
    QueueItemController
):

    def __init__(
        self,
        auth: AuthRequestPayload,
        config: APIConfig = APIConfig()
    ):

        self.api_client = AuthController(
            auth=auth,
            config=config
        )

        super().__init__(api_client=self.api_client)

def task_execution(auth: AuthRequestPayload, config: APIConfig = APIConfig()):

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):

        ergon = ErgonClient(auth=auth, config=config)

        ergon.create_task_execution(task_id=ergon.api_client.config.task_exec_config.task_id)
        ergon.write_tk_exec_log(message="Task execution started")
        result = wrapped(ergon)

        return result

    return wrapper
