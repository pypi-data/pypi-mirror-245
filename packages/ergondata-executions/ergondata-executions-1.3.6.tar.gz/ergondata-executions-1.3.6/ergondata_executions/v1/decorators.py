import sys
import wrapt
from typing import Type
from pydantic import StrictBool, StrictStr, BaseModel
from ergondata_executions.v1.api_exceptions import *
from ergondata_executions.v1.queue_item.interfaces import CreateQueueItemRequestPayload, UpdateQueueItemRequestPayload


def api_request(
    out_schema: Type[BaseModel],
    exec_token: StrictBool = False,
    queue_item: StrictBool = None,
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

            if queue_item:
                self.api_client.queue_item = data.data

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
        self.ergon.update_task_execution(processing_status_id="success")
        self.ergon.write_tk_exec_log(message="Stepped out of main method with success. Task execution finished.")

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


@wrapt.decorator
def dispatch_queue_item_decorator(wrapped, instance, args, kwargs):

    self = instance

    try:

        # Access the item argument if available
        result: CreateQueueItemRequestPayload = wrapped(*args, **kwargs)

        self.ergon.create_queue_item(
            queue_id=self.ergon.api_client.config.task_exec_config.target_queue_id,
            processing_status_message=result.processing_status_message,
            payload=result.payload,
            external_id=result.external_id,
            processing_priority_id=result.processing_priority_id,
            processing_status_id=result.processing_status_id
        )

        return result

    except DispatcherQIException:
        self.ergon.write_tk_exec_log(message=f"Queue item raised an exception", level="error")
    except DispatcherQISysError:
        self.ergon.write_tk_exec_log(message=f"Queue item raised a system exception", level="error")
    except DispatcherQIBusException:
        self.ergon.write_tk_exec_log(message=f"Queue item raised a business exception", level="error")
    except BaseException as e:
        self.ergon.write_tk_exec_log(message=f"Queue item raised an unknown error {e}", level="error")


def create_queue_item(wrapped_function=None):
    # Check if the decorator is called without parentheses
    if wrapped_function is None:
        return dispatch_queue_item_decorator
    else:
        return dispatch_queue_item_decorator(wrapped_function)

@wrapt.decorator
def get_queue_item_decorator(wrapped, instance, args, kwargs):

    self = instance
    queue_id = self.ergon.api_client.config.task_exec_config.source_queue_id
    self.ergon.write_tk_exec_log(message=f"Reading queue items from {queue_id}")

    while True:

        try:

            queue_item = self.ergon.get_queue_item(queue_id=queue_id)

            if not queue_item.data:
                self.ergon.write_tk_exec_log(message=f"No more queue items to read from {queue_id}")
                break

            result: UpdateQueueItemRequestPayload = wrapped(queue_item, queue_id)

            self.ergon.update_queue_item(
                queue_id=queue_id,
                queue_item_id=queue_item.data.id,
                processing_status_id=result.processing_status_id,
                processing_status_message=result.processing_status_message,
                payload=result.payload
            )

            self.ergon.write_tk_exec_log(message=f"Queue item {queue_item.data.id} processed with success")

        except PerformerQIException:
            self.ergon.write_tk_exec_log(message=f"Queue item raised an exception", level="error")
        except PerformerQISysError:
            self.ergon.write_tk_exec_log(message=f"Queue item raised a system exception", level="error")
        except PerformerQIBusException:
            self.ergon.write_tk_exec_log(message=f"Queue item raised a business exception", level="error")
        except BaseException as e:
            self.ergon.update_queue_item(
            queue_item_id=self.ergon.api_client.queue_item.id,
            processing_status_id="system_error",
            processing_status_message=str(e),
            queue_id=queue_id
        )


def get_next_item(wrapped_function=None):
    # Check if the decorator is called without parentheses
    if wrapped_function is None:
        return get_queue_item_decorator
    else:
        return get_queue_item_decorator(wrapped_function)

