"""shared_core.decorators.timeout unit tests."""

import time

import pytest
from shared_core.decorators.timeout import TimeoutError, timeout


def test_timeout_no_timeout():
    """Should return the function result when the function doesn't reach the timeout seconds."""

    @timeout(5)
    def test_func():
        """Test function."""
        return True

    assert test_func() is True


def test_timeout_no_error():
    """Should return None when the function reaches the timeout \
        but the decorator was configured to not raise an exception."""

    @timeout(1, error=False)
    def test_func():
        """Test function."""
        time.sleep(5)
        return True

    assert test_func() is None


def test_timeout():
    """Should throw an exception when the function reaches the timeout seconds."""

    @timeout(1)
    def test_func():
        """Test function."""
        time.sleep(5)
        return True

    with pytest.raises(TimeoutError) as error:
        test_func()

    assert str(error.value) == 'Function call timed out'


def test_timeout_custom_error():
    """Should throw an exception when the function reaches the timeout seconds."""

    @timeout(1, error_message='Custom error message')
    def test_func():
        """Test function."""
        time.sleep(5)
        return True

    with pytest.raises(TimeoutError) as error:
        test_func()

    assert str(error.value) == 'Custom error message'
