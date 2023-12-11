import logging
import logging.config
import sys

from izihawa_utils.exceptions import BaseError
from izihawa_utils.file import mkdir_p

from .handlers import QueueHandler


def configure_logging(config: dict, make_path: bool = False, default_level=logging.INFO):
    if config.get("application", {}).get("debug", False) or "logging" not in config:
        logging.basicConfig(stream=sys.stdout, level=default_level)
    else:
        if make_path:
            mkdir_p(config["log_path"])
        logging.config.dictConfig(config["logging"])


def error_log(e, level=logging.ERROR, **fields):
    level = getattr(e, "level", level)
    if isinstance(e, BaseError):
        e = e.as_internal_dict()
        e.update(fields)
    elif fields:
        e = {"error": repr(e), **fields}
    logging.getLogger("error").log(msg=str(e), level=level)


__all__ = [
    "QueueHandler",
    "configure_logging",
    "error_log",
]
