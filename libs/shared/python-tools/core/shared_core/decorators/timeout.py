"""
Timeout decorator.

This function decorator by default raises a TimeoutError exception if the function call takes longer than the specified.

Could also be used to only log a warning if the function call takes longer than the specified and return None.

Example Usage:

```python
import time

@timeout(1, error_message='Function slow; aborted')
def slow_function():
    time.sleep(5)
```

or without exception:

```python
import time

@timeout(1, error=False)
def slow_function():
    time.sleep(5)
```
"""

import functools
import logging
import signal
from typing import Callable

logger = logging.getLogger(__name__)


class TimeoutError(Exception):
    """Timeout exception."""


def timeout(seconds: int, *, error: bool = True, error_message: str = 'Function call timed out'):
    """
    Timeout Decorator.

    Args:
        seconds (int): Timeout in seconds
        error (bool, optional): Raise exception on timeout, default True
        error_message (str, optional): Timeout error message, default 'Function call timed out'

    Returns:
        Decorated function.
    """

    def decorated(func: Callable) -> Callable:
        """Decorate the function."""

        def _handle_timeout(signum, frame):
            """Handle timeout alarm."""
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            """Wrappers the function."""
            # SIGALRM is not available on Windows so you get an attribute error instead.
            if hasattr(signal, "SIGALRM"):
                try:
                    signal.signal(signal.SIGALRM, _handle_timeout)
                    signal.alarm(seconds)
                    try:
                        result = func(*args, **kwargs)
                    finally:
                        signal.alarm(0)
                except TimeoutError as err:
                    if error:
                        raise err

                    logger.warning(f'{func.__module__}.{func.__name__}: {error_message}')
                    return None

                return result

        return functools.wraps(func)(wrapper)

    return decorated
