import logging
import uuid
from datetime import datetime
from typing import Dict, Union
from dataclasses import dataclass, field
from google.cloud.logging_v2 import Client, Logger


@dataclass
class CustomMessage:
    """
    Logger message class.
    """

    project_id: str
    message: Union[str, Dict]
    attributes: Dict
    severity: str

    def __post_init__(self):
        if not self.attributes:
            self.attributes = {}
        if isinstance(self.message, (Dict, str)):
            self.struct_message = {"message": self.message, **self.attributes}
        else:
            raise TypeError("Type of logger message field must be str or Dict!")


@dataclass
class CustomStructuredLogger:
    """
    Custom Logger which provides functionality to easily log structured logs into google, use trace service, add labels
    and attributes. Also a local stdout logging is provided.
    """

    project_id: str
    name: str
    log_to_console: bool = True
    level_console: int = logging.DEBUG
    format_console: str = "%(asctime)s-%(name)s-%(levelname)s: %(message)s"
    log_to_cloud: bool = False
    labels: Dict = field(default_factory=dict)
    trace_id: str = uuid.uuid4().hex

    def __post_init__(self):
        self.trace: str = f"projects/{self.project_id}/traces/{self.trace_id}"
        if self.log_to_console:
            logging.basicConfig(format=self.format_console, level=self.level_console)
            self.console_logger = logging.getLogger(f"{self.name}_console")
        if self.log_to_cloud:
            self.google_logger: Logger = Client(project=self.project_id).logger(f"{self.name}_cloud")

    def _log_cloud(self, message: CustomMessage):
        self.google_logger.log_struct(
            info=message.struct_message,
            log_name=f"projects/{self.project_id}/logs/{self.name}",
            severity=message.severity,
            labels=self.labels,
            trace=self.trace,
            timestamp=datetime.utcnow(),
        )

    def _log_console(self, message: CustomMessage):
        self.console_logger.log(level=logging.getLevelName(message.severity), msg=message.struct_message)

    def _log(self, message: CustomMessage):
        """
        Calls loggers to submit messages to specific sinks (stdout/google cloud), depending on configuration.
        :param message:
        :return:
        """
        if self.log_to_console:
            self._log_console(message=message)
        if self.log_to_cloud:
            self._log_cloud(message=message)

    def info(self, message: Union[str, Dict], attributes: Dict = None):
        """
        Logs an INFO message.
        :param message: str or Dict object to log
        :param attributes: Dict for attributes which get listed in Google Logging UI
        :return:
        """
        custom_message: CustomMessage = CustomMessage(
            project_id=self.project_id,
            message=message,
            attributes=attributes,
            severity="INFO",
        )
        self._log(message=custom_message)

    def warning(self, message: Union[str, Dict], attributes: Dict = None):
        """
        Logs an WARNING message.
        :param message: str or Dict object to log
        :param attributes: Dict for attributes which get listed in Google Logging UI
        :return:
        """
        custom_message: CustomMessage = CustomMessage(
            project_id=self.project_id,
            message=message,
            attributes=attributes,
            severity="WARNING",
        )
        self._log(message=custom_message)

    def error(self, message: Union[str, Dict], attributes: Dict = None):
        """
        Logs an ERROR message.
        :param message: str or Dict object to log
        :param attributes: Dict for attributes which get listed in Google Logging UI
        :return:
        """
        custom_message: CustomMessage = CustomMessage(
            project_id=self.project_id,
            message=message,
            attributes=attributes,
            severity="ERROR",
        )
        self._log(message=custom_message)
