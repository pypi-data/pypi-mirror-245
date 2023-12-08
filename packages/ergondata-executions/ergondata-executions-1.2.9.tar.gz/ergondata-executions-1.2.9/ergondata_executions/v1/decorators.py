import sys
import wrapt
from typing import Type
from pydantic import StrictBool, StrictStr, BaseModel
from ergondata_executions.v1.api_exceptions import TaskException, TaskFailed

def api_request(
    out_schema: Type[BaseModel],
    exec_token: StrictBool = False,
    log_message: StrictStr = None,
    log_response: StrictBool = True
):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):

        self = instance
        if log_message:
            self.api_client.log_info(log_message.format(**kwargs))
        response = wrapped(*args, **kwargs)

        data = out_schema(**response.json())

        if response.status_code == 200:

            if log_response:
                self.api_client.log_info(data)

            if exec_token:

                self.api_client.set_task_execution(
                    exec_token=data.exec_token,
                    task_id=data.data.task.id,
                    task_execution_id=data.data.id
                )

        else:
            self.api_client.log_error(data)

        return data

    return wrapper


def func_logger(log_in: StrictBool = True, log_out: StrictBool = True, log_args: StrictBool = True):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):

        self = instance
        ergon = self.ergon
        function_id = wrapped.__name__

        if log_in:

            arg_str = ', '.join(f"{k}={v}" for k, v in zip(wrapped.__code__.co_varnames, args))
            arg_str += ', '.join(f"{k}={v}" for k, v in kwargs.items())

            if arg_str and log_args:
                message = f"Stepped in {function_id} with arguments: {arg_str}"
            else:
                message = f"Stepped in {function_id}"

            ergon.write_tk_exec_log(
                message=message,
                level="info",
                task_step_id=function_id
            )

        result = wrapped(*args, **kwargs)

        if log_out:
            ergon.write_tk_exec_log(
                message=f"Stepped out {function_id}",
                level="info",
                task_step_id=function_id
            )

        return result

    return wrapper

@wrapt.decorator
def run_decorator(wrapped, instance, args, kwargs):

    self = instance

    self.ergon.write_tk_exec_log(
        message="Running main method",
        task_step_id="main",
        level="info"
    )

    try:
        result = wrapped(*args, **kwargs)
        self.ergon.write_tk_exec_log(message="Task execution finished")
        self.ergon.update_task_execution(processing_status_id="success")
    except TaskException:
        sys.exit("Task execution failed due to TaskException")
    except BaseException as e:
        raise TaskFailed(ergon=self.ergon, processing_status_message=str(e))
    return result

def run(wrapped_function=None):
    # Check if the decorator is called without parentheses
    if wrapped_function is None:
        return run_decorator
    else:
        return run_decorator(wrapped_function)

