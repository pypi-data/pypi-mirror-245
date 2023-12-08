try:
    import sys
    import logging
    import traceback
    from typing import List
    from logging import Handler
    from threading import local
    from datetime import datetime

    from pythonjsonlogger import jsonlogger

except Exception as e:
    print(e)
    sys.exit(1)


class CustomLocal(local):
    def __init__(self) -> None:
        self.val = ""


logger_var_fyId = CustomLocal()
logger_var_requestId = CustomLocal()


class FyersJsonFormatter(jsonlogger.JsonFormatter):
    """
    Defines a custom json formatter for the logger.

    :param format_string: Format string to be used for the json formatter
    """
    def add_fields(self, log_record, record, message_dict):
        """
        Updates the log record with the required fields. Values from the message_dict are added to the log record, as specified in the format_string. 
        """
        try:
            super(FyersJsonFormatter, self).add_fields(log_record, record, message_dict)

            # add UTC timestamp
            log_record['timestamp'] = datetime.utcfromtimestamp(record.created).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            # add log level
            log_record['level'] = record.levelname

            # add location = [function_name:line_number] module_name
            log_record['location'] = f"[{record.funcName}:{record.lineno}] {record.module}"        
        except Exception as e:
            pass


def _get_default_format_string() -> str:
    return "%(timestamp)s %(level)s %(name)s %(location)s %(message)s"


def _get_default_stream_handler() -> Handler:
    _stream_handler = logging.StreamHandler(sys.stdout)
    _stream_handler.setFormatter(FyersJsonFormatter(_get_default_format_string()))
    return _stream_handler


class FyersLogger:
    """
    Defines a custom logger for the application. This logger can be used to log messages to the console, file, etc.
    :param name: Name of the logger
    :param level: Log level to be used for the logger
    :param stack_level: Stack level to be used for the logger
    :param handlers: List of handlers to be added to the logger
    """

    def __init__(self, name, level=logging.DEBUG, stack_level: int = 4, handlers: List[Handler] = None):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self.stacklevel = stack_level

        if handlers:
            for handler in handlers:
                self._logger.addHandler(handler)
        else:
            _stream_handler = _get_default_stream_handler()
            self._logger.addHandler(_stream_handler)

    @staticmethod
    def get_json_formatter(format_string: str = None):
        """
        Returns a json formatter with the given format string. If no format string is provided, the default format string is used.
        :param format_string: Format string to be used for the json formatter

        """
        if not format_string:
            format_string = _get_default_format_string()
        return FyersJsonFormatter(format_string)


    def _log(self, level, message, *args, **kwargs):
        extra = dict(**kwargs)
        arguments = list(args)
        extra["log_arguments"] = arguments
        extra["fyId"] = logger_var_fyId.val
        extra["requestId"] = logger_var_requestId.val

        stack_level = self.stacklevel
        if extra.get("stacklevel"):
            stack_level = extra.pop("stacklevel")
        assert stack_level > 0
        
        while stack_level > 0:
            try:
                self._logger.log(level, message, stacklevel=stack_level, extra=extra)
                break
            except Exception as e:
                stack_level -= 1
        

    def add_handler(self, handler: Handler) -> None:
        """
        Add a handler to the logger. This can be a custom StreamHandler, FileHandler, etc.
        :param handler: Handler to be added
        """
        self._logger.addHandler(handler)


    def debug(self, message: str, *args, **kwargs) -> None:
        self._log(logging.DEBUG, message, *args, **kwargs)

    
    def info(self, message: str, *args, **kwargs) -> None:
        self._log(logging.INFO, message, *args, **kwargs)

    
    def warning(self, message: str, *args, **kwargs) -> None:
        self._log(logging.WARNING, message, *args, **kwargs)

    
    def error(self, message: str, *args, **kwargs) -> None:
        self._log(logging.ERROR, message, *args, **kwargs)


    def critical(self, message: str, *args, **kwargs) -> None:
        self._log(logging.CRITICAL, message, *args, **kwargs)


    def exception(self, message: str, *args, **kwargs) -> None:
        self._log(logging.ERROR, f"{message}\n %{traceback.format_exc()}", *args, **kwargs)


    def set_fyId(self, fyId: str) -> None:
        """Sets FyId for a particular request. This function needs to be called only once for each request

        Args:
            fyId (str): Fyers ID
        """
        logger_var_fyId.val = fyId

    def set_requestId(self, requestId: str) -> None:
        """Sets RequestId for a particular request. This function needs to be called only once for each request

        Args:
            requestId (str): Request ID [This should be unique for each request]
        """
        logger_var_requestId.val = requestId


    def clear_data(self) -> None:
        """Clears data for this thread so that the data is not propagated in the next request."""
        logger_var_fyId.val = ""
        logger_var_requestId.val = ""
