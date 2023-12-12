import logging

try:
    SHOULD_CONVERT_TO_UNICODE = True
    from orjson import dumps
except ImportError:
    SHOULD_CONVERT_TO_UNICODE = False
    from json import dumps
from .DefaultFormatter import DefaultFormatter
from typing import Optional, List, Union
from datetime import datetime, date


class AwsFormatter(DefaultFormatter, logging.Formatter):

    def __init__(
            self,
            fmt: Optional[str] = None,
            datefmt: Optional[str] = "%Y-%m-%dT%H:%M:%S.%fZ",
            style: str = "%",
            json_serialize_default: callable = None,
            add_log_record_attrs: List[str] = None,
            **kwargs
    ):
        super().__init__(fmt, datefmt, style, use_colors=False, **kwargs)
        self.json_serialize_default = self._json_serialize_default
        if json_serialize_default is not None:
            self.json_serialize_default = json_serialize_default
        if add_log_record_attrs is not None:
            self.add_log_record_attrs = add_log_record_attrs
        else:
            self.add_log_record_attrs = [
                "client_addr",
                "request_line",
                "status_code",
                "method",
                "full_path",
                "http_version",
                "body",
            ]

    def _json_serialize_default(self, o):
        """
        A standard 'default' json serializer function.
        - Serializes datetime objects using their .isoformat() method.
        - Serializes all other objects using repr().
        """
        if isinstance(o, (date, datetime)):
            return datetime.strftime(o, self.datefmt)
        else:
            return repr(o)

    def format(self, record: logging.LogRecord) -> str:
        level_name = record.levelname
        seperator = " " * (8 - len(record.levelname))
        record.__dict__["levelprefix"] = level_name + ":" + seperator
        msg = {
            "timestamp": datetime.strftime(datetime.utcfromtimestamp(record.created), self.datefmt),
            "level": record.levelname,
            "message": super().format(record),
            "lineno": record.lineno,
            "file": record.filename,
            "path": record.pathname,
            "logger": record.name,
        }
        if record.exc_info and not record.exc_text:
            msg["message.exception"] = self.formatException(record.exc_info)
        if record.exc_text:
            msg["message.exc_text"] = record.exc_text
        if record.stack_info:
            msg["stack_trace"] = self.formatStack(record.stack_info, )

        for field in self.add_log_record_attrs:
            value = getattr(record, field, None)
            if value:
                msg[field] = value
        record.msg = msg
        result: Union[bytes, str] = dumps(record.msg, default=self.json_serialize_default)
        if SHOULD_CONVERT_TO_UNICODE:
            result = result.decode("utf-8")
        return result
