import logging
import logging.config
from pythonjsonlogger import jsonlogger

from source.config import config


def setup_logger():
    """
    Настройка логгера.
    """

    LOG_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                "json_ensure_ascii": False
            },
            "simple": {
                "format": "%(asctime)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple"
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": f"{config.PROJECT_DIR}/logs/app.log",
                "when": "D",
                "interval": 7,
                "backupCount": 0,
                "encoding": "utf-8"
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file"]
        },
    }

    # Инициализация логгера
    logging.config.dictConfig(LOG_CONFIG)
    return LOG_CONFIG
