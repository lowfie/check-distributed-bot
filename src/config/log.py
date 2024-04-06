import logging.config

LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "logging.Formatter",
            "fmt": "%(asctime)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "root": {"handlers": ["default"], "level": "INFO"},
        "celery.app.trace": {"handlers": [], "level": "INFO", "propagate": False},
        "celery.worker.strategy": {"handlers": [], "level": "INFO", "propagate": False},
    },
}


def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
