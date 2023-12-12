from .AwsFormatter import AwsFormatter
from logging import LogRecord


class AwsAccessFormatter(AwsFormatter):

    def format(self, record: LogRecord) -> str:
        record = self.get_record_attributes(record)
        return super().format(record)
