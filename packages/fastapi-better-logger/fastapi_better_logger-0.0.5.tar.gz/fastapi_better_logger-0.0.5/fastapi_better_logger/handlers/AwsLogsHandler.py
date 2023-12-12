from watchtower import CloudWatchLogHandler
from fastapi_better_logger.formatters import AwsFormatter, AwsAccessFormatter
import botocore


class AwsLogHandler(CloudWatchLogHandler):

    def __init__(
        self,
        log_group_name: str = ...,
        log_stream_name: str = ...,
        use_queues: bool = True,
        send_interval: int = 60,
        max_batch_size: int = 1024 * 1024,
        max_batch_count: int = 10000,
        boto3_client: botocore.client.BaseClient = None,
        boto3_profile_name: str = None,
        create_log_group: bool = True,
        json_serialize_default: callable = None,
        log_group_retention_days: int = None,
        create_log_stream: bool = True,
        max_message_size: int = 256 * 1024,
        log_group=None,
        stream_name=None,
        *args,
        **kwargs
    ):
        super().__init__(
            log_group_name,
            log_stream_name,
            use_queues,
            send_interval,
            max_batch_size,
            max_batch_count,
            boto3_client,
            boto3_profile_name,
            create_log_group,
            json_serialize_default,
            log_group_retention_days,
            create_log_stream,
            max_message_size,
            log_group,
            stream_name,
            *args,
            **kwargs
        )
        self.formatter = AwsFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            json_serialize_default=json_serialize_default,
        )


class AwsAccessLogHandler(CloudWatchLogHandler):

    def __init__(
        self,
        log_group_name: str = ...,
        log_stream_name: str = ...,
        use_queues: bool = True,
        send_interval: int = 60,
        max_batch_size: int = 1024 * 1024,
        max_batch_count: int = 10000,
        boto3_client: botocore.client.BaseClient = None,
        boto3_profile_name: str = None,
        create_log_group: bool = True,
        json_serialize_default: callable = None,
        log_group_retention_days: int = None,
        create_log_stream: bool = True,
        max_message_size: int = 256 * 1024,
        log_group=None,
        stream_name=None,
        *args,
        **kwargs
    ):
        super().__init__(
            log_group_name,
            log_stream_name,
            use_queues,
            send_interval,
            max_batch_size,
            max_batch_count,
            boto3_client,
            boto3_profile_name,
            create_log_group,
            json_serialize_default,
            log_group_retention_days,
            create_log_stream,
            max_message_size,
            log_group,
            stream_name,
            *args,
            **kwargs
        )
        self.formatter = AwsAccessFormatter(
            '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            json_serialize_default=json_serialize_default,
        )
