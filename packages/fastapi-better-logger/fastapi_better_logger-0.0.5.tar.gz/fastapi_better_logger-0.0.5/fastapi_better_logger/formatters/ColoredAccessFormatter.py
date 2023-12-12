from .ColoredFormatter import ColoredFormatter
from logging import LogRecord


class ColoredAccessFormatter(ColoredFormatter):

    def formatMessage(self, record: LogRecord) -> str:
        record_copy = self.get_record_attributes(record)
        return super().formatMessage(record_copy)
