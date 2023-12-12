import logging
import os
import uuid
from typing import Literal
from pydantic import StrictBool


class APILogger:

    _file_handlers = []

    def __init__(
        self,
        enable_logs: bool = True,
        log_file_path: str = 'logs',
        log_level: Literal["info", "debug", "error", "warning"] = "debug",
        preserve_logger_handler: StrictBool = True
    ):
        self.enable_logs = enable_logs
        self.log_file_path = log_file_path
        self.logger = self._create_logger()
        self.log_level = log_level
        self.preserve_logger_handler = preserve_logger_handler

        # Configure the logger only if it hasn't been configured yet
        self._configure_logger()

    def _create_logger(self):
        logger = logging.getLogger(str(uuid.uuid4()))  # Use a unique name for each logger instance
        return logger

    def _configure_logger(self):
        # Clear existing handlers if preserve_logger_handler is set to False

        self._configure_file_handler()
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Set the logger level to DEBUG to capture all messages
        if self.log_level == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif self.log_level == "info":
            self.logger.setLevel(logging.INFO)
        elif self.log_level == "warning":
            self.logger.setLevel(logging.WARNING)
        elif self.log_level == "error":
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.DEBUG)

    def _configure_file_handler(self):

        if not self.log_file_path:
            return

        log_file_name = self._get_log_file_name()
        log_file_path = os.path.join(self.log_file_path, log_file_name)

        if self.preserve_logger_handler and APILogger._file_handlers:
            self.logger.addHandler(APILogger._file_handlers[0])
        else:
            file_handler = logging.FileHandler(log_file_path)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            APILogger._file_handlers = [file_handler]

    def _get_log_file_name(self):
        # Generate a unique filename using UUID
        return f"{uuid.uuid4()}.txt"

    def log(self, message, level: Literal["warning", "info", "error"] = "info"):
        if level == "warning":
            self.logger.log(msg=message, level=logging.WARNING)
        elif level == "info":
            self.logger.log(msg=message, level=logging.INFO)
        elif level == "error":
            self.logger.log(msg=message, level=logging.ERROR)
        else:
            pass
