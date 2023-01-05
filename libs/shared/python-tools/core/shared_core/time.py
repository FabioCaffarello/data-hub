"""Time utils module."""

import time


def current_milli_time() -> int:
    """Get the current time with milliseconds."""
    return round(time.time() * 1000)
