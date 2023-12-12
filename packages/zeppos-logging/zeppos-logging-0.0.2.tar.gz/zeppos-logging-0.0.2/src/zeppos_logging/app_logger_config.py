"""Module containing hardcoded logging json configs.

References: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
"""

# Standard libs
from typing import Dict


# pylint: disable=too-few-public-methods
class AppLoggerConfig:
    """Class to define hard-coded json logging configs."""

    @staticmethod
    def default_format_1() -> Dict:
        """Define the logging configuration in json for the `default_format_1`.

        Note:
            format => name, levelname, message with a date format of `yyyy-mm-ddThh-MM-ss` in a single line.
            handlers => console output.

        :return: Configuration of the formatters, filters, handlers, and loggers as well as the root logger.
        :rtype: Returns a dictionary object.
        """
        return {
            "version": 1,  # This has to be 1
            "disable_existing_loggers": True,
            "incremental": False,
            "formatters": {
                "default-single-line": {
                    "format": "{name:<10s} | {levelname:8s} | {message:s}",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "style": "{",
                }
            },
            "filters": {},
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "default-single-line",
                    "filters": "",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {},
            "root": {"handlers": ["console"]},
        }
