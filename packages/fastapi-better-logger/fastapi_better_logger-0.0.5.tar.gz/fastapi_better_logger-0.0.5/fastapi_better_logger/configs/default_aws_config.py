AWS_DEFAULT_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "alembic": {
            "()": "fastapi_better_logger.AwsFormatter",
            "fmt": "ALEMBIC: %(message)s",
        },
        "default": {
            "()": "fastapi_better_logger.AwsFormatter",
            "fmt": "%(message)s",
        },
        "access": {
            "()": "fastapi_better_logger.AwsAccessFormatter",
            "fmt": '%(client_addr)s - %(request_line)s',  # noqa: E501
        },
    },
    "handlers": {
        "alembic": {
            "formatter": "alembic",
            "class": "fastapi_better_logger.AwsLogHandler",
            "log_group_name": "test_log_group_name",
            "log_stream_name": "test_log_stream_name",
            "use_queues": True,
        },
        "default": {
            "formatter": "default",
            "class": "fastapi_better_logger.AwsLogHandler",
            "log_group_name": "test_log_group_name",
            "log_stream_name": "test_log_stream_name",
            "use_queues": True,
        },
        "access": {
            "formatter": "access",
            "class": "fastapi_better_logger.AwsAccessLogHandler",
            "log_group_name": "test_log_group_name",
            "log_stream_name": "test_log_stream_name",
            "use_queues": True,
        },
    },
    "loggers": {
        "alembic.runtime.migration": {"handlers": ["alembic"], "level": "WARNING", "propagate": False},
        "sqlalchemy.engine.Engine": {"handlers": ["alembic"], "level": "INFO", "propagate": False},
        "fastapi": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "fastapi.logger": {"handlers": ["access"], "level": "DEBUG", "propagate": False},
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
