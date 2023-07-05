import logging


def log_config(level_str):
    """
    https://docs.python.org/3/howto/logging.html#logging-to-a-file
    """
    numeric_level = getattr(logging, level_str.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {}".format(level_str))
    logging.basicConfig(level=numeric_level)
