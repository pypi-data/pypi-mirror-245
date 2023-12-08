import sys
from pydantic import StrictStr
from typing import Optional, Any

class TaskException(Exception):

    ergon: Any

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


