"""Main AppLogger Singleton Class Module."""

# Standard Libs
import logging
import logging.config
from typing import Any, Dict, Optional

# Custom libs
from zeppos_logging.app_logger_config import AppLoggerConfig
from zeppos_logging.app_logger_configs import AppLoggerConfigs
from zeppos_logging.app_logger_config_name import AppLoggerConfigName


# pylint: disable=too-few-public-methods
class AppLogger:
    """Singleton AppLogger Class."""

    logging.basicConfig(level=logging.INFO)
    __logger: logging.Logger = logging.getLogger()
    __logger.addHandler(logging.NullHandler())
    config_dict: Dict[str, Any]

    @staticmethod
    def apply_configuration(
        app_logger_config_name: Optional[AppLoggerConfigName] = None,
    ) -> None:
        """Apply the yaml configuration if any is available.

        :param app_logger_config_name: the name of the config to be used to log information
            Available configs:
            - default_format_1
            - mqtt_format_1

            By default the `default_format_1` gets set which is logging to the console only.
        :return: Nothing
        """
        app_logger_config_name_resolved: AppLoggerConfigName = (
            AppLoggerConfigName.DEFAULT_FORMAT_1 if app_logger_config_name is None else app_logger_config_name
        )
        AppLogger.debug("Applying json configuration.")
        AppLogger._configure_logger(app_logger_config_name=app_logger_config_name_resolved)

    @staticmethod
    def _configure_logger(app_logger_config_name: AppLoggerConfigName) -> None:
        """Set the logger configuration.

        :param app_logger_config_name: the name of the config to be used to log information
            Available configs:
            - default_format_1
            - mqtt_format_1

        :return: Nothing
        """
        AppLogger._set_config_dict_for_config_section(app_logger_config_name=app_logger_config_name)
        # set the retrieved config_dict on the actual python logging object
        logging.config.dictConfig(AppLogger.config_dict)

    @staticmethod
    def _set_config_dict_for_config_section(app_logger_config_name: AppLoggerConfigName) -> None:
        """Set the config dictionary.

        :param app_logger_config_name: the name of the config to be used to log information
            Available configs:
            - default_format_1
            - mqtt_format_1

        :return: Nothing
        """
        AppLogger.debug(message=f"Getting Config Section for [{app_logger_config_name.value}]")
        configs = AppLoggerConfigs()

        if app_logger_config_name in configs.keys():
            AppLogger.debug(message=f"Found `{app_logger_config_name.value}` configuration.")
            AppLogger.config_dict = configs[app_logger_config_name]()
        else:
            AppLogger.debug(message=f"`{app_logger_config_name.value}` configuration not found.")
            AppLogger.debug(message="Default fall-back logging enabled.")
            AppLogger.config_dict = AppLoggerConfig.default_format_1()

    @staticmethod
    def set_level(logging_level: int) -> None:
        """Set the logging level for the logger at the root level.

        :param logging_level: The level to set the root level logger to.
        :return: Nothing
        """
        AppLogger.__logger.setLevel(logging_level)

    @staticmethod
    def set_debug_level() -> None:
        """Set the logging level to debug.

        :return: Nothing
        """
        AppLogger.set_level(logging.DEBUG)

    @staticmethod
    def set_info_level() -> None:
        """Set the logging level to info.

        :return: Nothing
        """
        AppLogger.set_level(logging.INFO)

    @staticmethod
    def set_error_level() -> None:
        """Set the logging level to error.

        :return: Nothing
        """
        AppLogger.set_level(logging.ERROR)

    @staticmethod
    def set_warning_level() -> None:
        """Set the logging level to warning.

        :return: Nothing
        """
        AppLogger.set_level(logging.WARNING)

    @staticmethod
    def set_critical_level() -> None:
        """Set the logging level to critical.

        Note: Critical and Fatal are the same level.

        :return: Nothing
        """
        AppLogger.set_level(logging.CRITICAL)

    @staticmethod
    def set_fatal_level() -> None:
        """Set the logging level to fatal.

        Note: Critical and Fatal are the same level.

        :return: Nothing
        """
        AppLogger.set_level(logging.FATAL)

    @staticmethod
    def debug(message: str) -> None:
        """Log at debug level.

        :param message: Message to log
        :return: Nothing
        """
        AppLogger.__logger.debug(msg=message)

    @staticmethod
    def info(message: str) -> None:
        """Log at info or information level.

        :param message: Message to log
        :return: Nothing
        """
        AppLogger.__logger.info(msg=message)

    @staticmethod
    def warning(message: str) -> None:
        """Log at warning level.

        :param message: Message to log
        :return: Nothing
        """
        AppLogger.__logger.warning(msg=message)

    @staticmethod
    def error(message: str) -> None:
        """Log at error level.

        :param message: Message to log
        :return: Nothing
        """
        AppLogger.__logger.error(msg=message)

    @staticmethod
    def critical(message: str) -> None:
        """Log at critical level.

        :param message: Message to log
        :return: Nothing
        """
        AppLogger.__logger.critical(msg=message)

    @staticmethod
    def fatal(message: str) -> None:
        """Log at fatal level.

        :param message: Message to log
        :return: Nothing
        """
        AppLogger.__logger.fatal(msg=message)
