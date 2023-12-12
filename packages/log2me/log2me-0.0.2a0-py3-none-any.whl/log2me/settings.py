import logging
from typing import Dict, Optional

from pydantic import BaseModel, Field


class LogSettings(BaseModel):
    """Settings for the loggers.

    Attributes:
        console_level: The level to use for the console output.
        file_level: The level to use for the file output.
        file_path: The path where the log file should be created.
            Can contain the following placeholders:

            - %date%: The current date in the format YYYY-MM-DD.
            - %time%: The current time in the format HH-MM-SS.
            - %Y%: The current year.
            - %M%: The current month.
            - %D%: The current day.
            - %H%: The current hour.
            - %m%: The current minute.
            - %s%: The current second.
            - %ms%: The current microsecond.

            If `None` logging is disabled.
        file_override: Should the file be opened in overwrite mode or
            append mode?
        base: The base logger (used with `getLogger()`).
        others: Change the log levels for specific loggers.
    """

    console_level: Optional[int] = Field(
        logging.INFO, description="The level to use for the console output."
    )
    file_level: Optional[int] = Field(
        -1, description="The level to use for the file output."
    )
    file_path: Optional[str] = Field(
        None,
        description=(
            "The path where the log file should be created. "
            "Can contain the following placeholders:\n"
            "- %date%: The current date in the format YYYY-MM-DD.\n"
            "- %time%: The current time in the format HH-MM-SS.\n"
            "- %Y%: The current year.\n"
            "- %M%: The current month.\n"
            "- %D%: The current day.\n"
            "- %H%: The current hour.\n"
            "- %m%: The current minute.\n"
            "- %s%: The current second.\n"
            "- %ms%: The current microsecond.\n"
            "If `None` logging is disabled."
        ),
    )
    file_override: Optional[bool] = Field(
        False,
        description=(
            "Should the file be opened in overwrite mode or append mode?"
        ),
    )
    base: Optional[str] = Field(
        "log2me", description="The base logger (used with `getLogger()`)."
    )
    others: Dict[str, int] = Field(
        default_factory=dict,
        description=(
            "Change the log levels for specific loggers. "
            "The key is the name of the logger, the value is "
            "the level. If the value is None, the level will "
            "not be changed."
        ),
    )
