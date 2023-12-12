DEFAULT_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "alembic": {
            "()": "fastapi_better_logger.ColoredFormatter",
            "fmt": "%(levelprefix)s ALEMBIC: %(message)s [%(filename)s:%(lineno)d]",
            "use_colors": True,
        },
        "default": {
            "()": "fastapi_better_logger.ColoredFormatter",
            "fmt": "%(levelprefix)s %(message)s [%(filename)s:%(lineno)d]",
            "use_colors": True,
        },
        "access": {
            "()": "fastapi_better_logger.ColoredAccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501,
            "use_colors": True,
        },
    },
    "handlers": {
        "alembic": {
            "class": "logging.StreamHandler",
            "formatter": "alembic",
            "stream": "ext://sys.stderr",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
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
