import sys
from pydantic import StrictStr
from typing import Optional, Any


class TaskException(Exception):

    ergon = None

    def __init__(
        self,
        ergon,
        task_exception_id: StrictStr = None,
        processing_status_message: StrictStr = None,
    ):

        ergon.update_task_execution(
            task_exception_id=task_exception_id,
            processing_status_message=str(processing_status_message),
        )

        super().__init__(self)


class TaskFailed(Exception):

    def __init__(
        self,
        ergon,
        processing_status_message: Optional[StrictStr] = None,
    ):

        ergon.update_task_execution(
            processing_status_id="system_error",
            processing_status_message=processing_status_message
        )
        sys.exit(f"Task failed due to generic unknown error {processing_status_message}")


class DispatcherQIException(Exception):

    ergon = None

    def __init__(
        self,
        ergon,
        processing_exception_id: StrictStr,
        processing_status_message: StrictStr = None,
        external_id: StrictStr = None,
        payload: Any = None,
    ):

        ergon.create_queue_item(
            queue_id=ergon.api_client.config.task_exec_config.target_queue_id,
            external_id=external_id,
            payload=payload,
            processing_exception_id=processing_exception_id,
            processing_status_message=str(processing_status_message),
            processing_status_id=None
        )

        super().__init__(self)


class PerformerQIException(Exception):

    ergon = None

    def __init__(
        self,
        ergon,
        processing_exception_id: StrictStr,
        processing_status_message: StrictStr = None,
        payload: Any = None,
    ):

        ergon.update_queue_item(
            queue_id=ergon.api_client.config.task_exec_config.source_queue_id,
            queue_item_id=ergon.api_client.queue_item.id,
            payload=payload,
            processing_exception_id=processing_exception_id,
            processing_status_message=str(processing_status_message)
        )

        super().__init__(self)


class DispatcherQISysError(Exception):

    ergon = None

    def __init__(
        self,
        ergon,
        processing_status_message: StrictStr = None,
        external_id: StrictStr = None,
        payload: Any = None
    ):

        ergon.create_queue_item(
            queue_id=ergon.api_client.config.task_exec_config.target_queue_id,
            external_id=external_id,
            payload=payload,
            processing_status_id="system_error",
            processing_status_message=str(processing_status_message)
        )

        super().__init__(self)


class PerformerQISysError(Exception):

    ergon = None

    def __init__(self, ergon, processing_status_message: StrictStr = None):

        ergon.update_queue_item(
            queue_item_id=ergon.api_client.queue_item.id,
            queue_id=ergon.api_client.config.task_exec_config.source_queue_id,
            processing_status_id="system_error",
            processing_status_message=str(processing_status_message)
        )

        super().__init__(self)


class DispatcherQIBusException(Exception):

    ergon = None

    def __init__(
        self,
        ergon,
        processing_status_message: StrictStr = None,
        payload: Any = None,
        external_id: StrictStr = None
    ):

        ergon.create_queue_item(
            queue_id=ergon.api_client.config.task_exec_config.target_queue_id,
            payload=payload,
            processing_status_id="business_exception",
            processing_status_message=processing_status_message,
            external_id=external_id
        )

        super().__init__(self)



class PerformerQIBusException(Exception):

    ergon = None

    def __init__(self, ergon, processing_status_message: StrictStr = None):

        ergon.update_queue_item(
            queue_item_id=ergon.api_client.queue_item.id,
            queue_id=ergon.api_client.config.task_exec_config.source_queue_id,
            processing_status_id="business_exception",
            processing_status_message=processing_status_message
        )

        super().__init__(self)