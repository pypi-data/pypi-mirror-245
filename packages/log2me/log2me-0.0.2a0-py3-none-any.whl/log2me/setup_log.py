import logging
import os.path
from datetime import datetime

from rich.logging import RichHandler

from .settings import LogSettings


def get_log_file(file_path: str) -> str:
    """
    Get the full file path for the log file.

    Args:
        file_path: The path of the log file. Can contain the following
            placeholders:

            - %date%: The current date in the format YYYY-MM-DD.
            - %time%: The current time in the format HH-MM-SS.
            - %Y%: The current year.
            - %M%: The current month.
            - %D%: The current day.
            - %H%: The current hour.
            - %m%: The current minute.
            - %s%: The current second.
            - %ms%: The current microsecond.

    Returns:
        The full file path for the log file, with placeholders expanded.
    """
    now = datetime.now()
    final_file_path = (
        file_path.replace("%date%", now.strftime("%Y-%m-%d"))
        .replace("%time%", now.strftime("%H-%M-%S"))
        .replace(
            "%Y%",
            str(now.year),
        )
        .replace(
            "%M%",
            str(now.month),
        )
        .replace(
            "%D%",
            str(now.day),
        )
        .replace(
            "%H%",
            str(now.hour),
        )
        .replace(
            "%m%",
            str(now.minute),
        )
        .replace(
            "%s%",
            str(now.second),
        )
        .replace(
            "%ms%",
            str(now.microsecond),
        )
    )
    final_dir_path = os.path.dirname(final_file_path)
    if not os.path.isdir(final_dir_path):
        os.makedirs(final_dir_path)
    print(final_file_path)
    return final_file_path


def setup_logging(stg: LogSettings, debug: bool = False) -> logging.Logger:
    """
    Sets up logging for the application.

    If a log file is specified in the settings, the log file will be created
    and used. Otherwise, only the console will be used.
    The path of the log file can contain the following placeholders:

    - %date%: The current date in the format YYYY-MM-DD.
    - %time%: The current time in the format HH-MM-SS.
    - %Y%: The current year.
    - %M%: The current month.
    - %D%: The current day.
    - %H%: The current hour.
    - %m%: The current minute.
    - %s%: The current second.
    - %ms%: The current microsecond.

    Args:
        stg: The settings object.

    Returns:
        The logger object.
    """
    # The file handler for the log file.
    if stg.file_path and stg.file_level and stg.file_level > 0:
        fh = logging.FileHandler(
            get_log_file(stg.file_path),
            "w" if stg.file_override else "a",
            "utf-8",
        )
        fh.setLevel(stg.file_level)
        fh.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s",
                datefmt="%I:%M:%S %p",
            )
        )
    else:
        fh = None

    if stg.console_level:
        ch = RichHandler()
        ch.setLevel(stg.console_level)
        # ch.setFormatter(logging.Formatter(
        #     '%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s',
        #     datefmt='%I:%M:%S %p'
        # ))
    else:
        ch = None

    # Top level logger.
    logger = logging.getLogger()
    logger.handlers = []
    if fh:
        logger.addHandler(fh)
    if ch:
        logger.addHandler(ch)

    if ch or fh:
        logger.setLevel(
            min(
                stg.file_level if stg.file_level else logging.CRITICAL,
                stg.console_level if stg.console_level else logging.CRITICAL,
            )
        )
    else:
        logger.setLevel(logging.CRITICAL)

    # Change the log levels for specific loggers.
    for logger_name, logger_level in stg.others.items():
        if logger_level is not None:
            logging.getLogger(logger_name).setLevel(logger_level)

    # See all loggers.
    if debug:
        from log2me.print_loggers import print_loggers

        print_loggers()

    return logging.getLogger(stg.base)
