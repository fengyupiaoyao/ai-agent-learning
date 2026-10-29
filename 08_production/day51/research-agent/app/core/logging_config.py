import logging
import logging.config


class RequestIdFilter(logging.Filter):
    """Add request id to log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        from app.core.request_context import request_id_var

        record.request_id = request_id_var.get()
        return True


def setup_logging(level: str = "INFO") -> None:
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_id": {
                "()": RequestIdFilter,
            }
        },
        "formatters": {
            "standard": {
                "format": (
                    "%(asctime)s %(levelname)s "
                    "request_id=%(request_id)s "
                    "logger=%(name)s %(message)s"
                )
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "filters": ["request_id"],
                "stream": "ext://sys.stdout",
            }
        },
        "root": {
            "level": level.upper(),
            "handlers": ["console"],
        },
    })
