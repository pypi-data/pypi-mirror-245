"""Logger module for cpytest."""

import logging


def _make_formatter(fmt: str, datefmt: str | None = None) -> logging.Formatter:
    try:
        import colorlog  # pylint: disable=import-outside-toplevel
        from typing import cast  # pylint: disable=import-outside-toplevel

        color_mapping = {
            'DEBUG': 'bold_black',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
        formatter = colorlog.ColoredFormatter(
            f"%(log_color)s{fmt}",
            datefmt=datefmt,
            log_colors=color_mapping,
        )
        return cast(logging.Formatter, formatter)
    except ImportError:
        return logging.Formatter(fmt, datefmt=datefmt)


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(_make_formatter("%(name)-8s %(levelname)-8s %(message)s"))
    logger.addHandler(ch)
    return logger
