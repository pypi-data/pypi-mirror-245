"""Module to format logging record information into json."""

# Standard libs
import json
import logging
import decimal


class JsonFormatter(logging.Formatter):
    """Class to format logging record into json."""

    def __init__(self, fmt: str, datefmt: str, delimiter: str) -> None:
        """Initialize the class with variables.

        :param fmt: string format
        :param datefmt: date datefmt
        :param delimiter: format delimiter
        :return: Nothing
        """
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.fmt = [item.strip() for item in fmt.split(",")]
        self.datefmt = datefmt
        self.delimiter = delimiter

    def format(self, record: logging.LogRecord) -> str:
        """Create a json format of the logging record.

        :param record: logging record with logging information used to format the json message
        :return: Json string with logging information.
        """
        output = {k: str(v) for k, v in record.__dict__.items() if k in self.fmt}

        if "asctime" in self.fmt and "msecs" in record.__dict__.keys():
            msecs = round(decimal.Decimal(record.__dict__["msecs"]), 0)
            output["asctime"] = f'{output["asctime"]}.{msecs}'
        return json.dumps(obj=output, default=str)
