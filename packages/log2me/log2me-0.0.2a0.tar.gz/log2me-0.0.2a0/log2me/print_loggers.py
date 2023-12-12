"""A script that prints all the loggers and their levels."""
import logging


def print_loggers() -> None:
    """
    Print the loggers and their levels.
    """
    for logger_name in logging.Logger.manager.loggerDict:
        print(logger_name, ": ", end="")
        level = logging.getLogger(logger_name).getEffectiveLevel()

        print(logging.getLevelName(level))


if __name__ == "__main__":
    print_loggers()
    print("Done.")
