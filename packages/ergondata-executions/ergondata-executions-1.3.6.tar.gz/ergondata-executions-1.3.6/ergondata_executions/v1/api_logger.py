import logging
import os
import uuid
from typing import Literal, Union

class APILogger:
    def __init__(
        self,
        enable_logs: bool = True,
        log_file_path: str = 'logs',
        log_level: Literal["info", "debug", "error", "warning"] = "debug"
    ):
        self.enable_logs = enable_logs
        self.log_file_path = log_file_path
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level

        # Configure the logger to write to a file
        self._configure_file_handler()

        # Configure a console handler
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

    def _get_log_file_path(self):
        # Generate a unique filename using UUID
        log_filename = f"{uuid.uuid4()}.txt"
        return os.path.join(self.log_file_path, log_filename)

    def _configure_file_handler(self):

        if not self.log_file_path:
            return

        log_file_path = self._get_log_file_path()
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_error(self, message):
        if self.enable_logs:
            self.logger.error(message)

    def log_info(self, message):
        if self.enable_logs:
            self.logger.info(message)

    def log_warning(self, message):
        if self.enable_logs:
            self.logger.warning(message)


    def log(self, message, level: Literal["warning", "info", "error"] = "info"):
        if level == "warning":
            self.logger.log(msg=message, level=logging.WARNING)
        elif level == "info":
            self.logger.log(msg=message, level=logging.INFO)
        elif level == "error":
            self.logger.log(msg=message, level=logging.ERROR)
        else:
            pass
