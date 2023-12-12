"""Module containing the actual hardcoded logging json configs methods."""

# Custom libs
from zeppos_logging.app_logger_config_name import AppLoggerConfigName
from zeppos_logging.app_logger_config import AppLoggerConfig


# pylint: disable=too-few-public-methods
class AppLoggerConfigs(dict):
    """Class to define the actual json logging configs method."""

    def __init__(self) -> None:
        """Initialize the actual logging json config methods available.

        Note:
            Currently available configs are:
            - default_format_1
            - mqtt_format_1
        :return: Nothing
        """
        self[AppLoggerConfigName.DEFAULT_FORMAT_1] = AppLoggerConfig.default_format_1
