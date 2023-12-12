"""Module to define custom logging filter."""

# Standard lib
import logging
import socket


# pylint: disable=too-few-public-methods
class AppLoggerFilter(logging.Filter):
    """Class of custom AppLogger filter."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Set the filter information in the record.

        :param record: Logging record
        :return: True indicating the information is good.
        """
        record.client_ip = self._get_client_ip()
        record.host_name = self._get_host_name()
        record.functionName = self._get_function_name()

        return True

    def _get_client_ip(self) -> str:
        """Get the client ip where the code is running on.

        :return: The ipaddress of the current hostname
        """
        hostname = self._get_host_name()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def _get_host_name(self) -> str:
        """Get the hostname of the application this code is running on.

        :return: Hostname that serves up this code.
        """
        return socket.gethostname()

    def _get_function_name(self) -> str:
        """Get the name of the function this code is running on.

        Note: Since we are wrapping the debug, info, warning, error, fatal, and critical methods
              of the python `logging` class, we have to go into the trace stack to get the calling
              function name one level up from the wrapper class

        TODO: Complete the finding of the calling function in the trace stack.

        :return: Name of the function that called the logger.
        """
        return "Unknown"
