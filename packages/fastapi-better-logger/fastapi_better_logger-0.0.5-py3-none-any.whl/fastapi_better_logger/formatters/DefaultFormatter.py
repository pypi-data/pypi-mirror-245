import logging
import http
import sys
import click
from typing import Optional
from copy import copy


class DefaultFormatter(logging.Formatter):
    use_colors: bool

    status_code_colours = {
        1: lambda code: click.style(str(code), fg="bright_white"),
        2: lambda code: click.style(str(code), fg="green"),
        3: lambda code: click.style(str(code), fg="yellow"),
        4: lambda code: click.style(str(code), fg="red"),
        5: lambda code: click.style(str(code), fg="bright_red"),
    }

    def __init__(
            self,
            fmt: Optional[str] = None,
            datefmt: Optional[str] = None,
            style: str = "%",
            use_colors: Optional[bool] = None,
    ):
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def get_status_code(self, status_code: int) -> str:
        try:
            status_phrase = http.HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = ""
        status_and_phrase = "%s %s" % (status_code, status_phrase)
        if self.use_colors:
            def default() -> str:
                return status_and_phrase  # pragma: no cover

            func = self.status_code_colours.get(status_code // 100, default)
            return func(status_and_phrase)
        return status_and_phrase

    def get_http_attributes(self, record: logging.LogRecord) -> logging.LogRecord:
        record_copy = copy(record)
        if isinstance(record.args, dict):
            client_addr = record_copy.args.get("client_addr")
            method = record_copy.args.get("method")
            full_path = record_copy.args.get("full_path")
            http_version = record_copy.args.get("http_version")
            status_code = record_copy.args.get("status_code")
        else:
            client_addr = record_copy.args[0]
            method = record_copy.args[1]
            full_path = record_copy.args[2]
            http_version = record_copy.args[3]
            status_code = record_copy.args[4]
        status_code = self.get_status_code(int(status_code))
        request_line = "%s %s HTTP/%s" % (method, full_path, http_version)
        record_copy.__dict__.update(
            {
                "method": method,
                "full_path": full_path,
                "http_version": http_version,
                "client_addr": client_addr,
                "request_line": request_line,
                "status_code": status_code,
            }
        )
        return record_copy

    def formatMessage(self, record: logging.LogRecord) -> str:
        return super().formatMessage(record)

    def get_record_attributes(self, record: logging.LogRecord) -> logging.LogRecord:
        return self.get_http_attributes(record)
