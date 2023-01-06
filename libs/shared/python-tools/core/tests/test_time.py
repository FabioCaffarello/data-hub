"""shared_core.time tests."""

from unittest.mock import MagicMock, patch

from shared_core.time import current_milli_time


@patch('time.time')
def test_current_milli_time(mock_time: MagicMock):
    """Should return the current time in milliseconds and multiply by 1000."""
    mock_time.return_value = 1234
    assert current_milli_time() == 1234000
