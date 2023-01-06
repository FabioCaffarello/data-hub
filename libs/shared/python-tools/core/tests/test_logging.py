"""shared_core.logging tests."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

from shared_core import logging


def test_setup_logging_info(capsys: "pytest.CaptureFixture"):
    """Should setup logging using JSON format (INFO)."""
    logger = logging.setup_logging('test1', log_level='INFO')
    logger.info("test")

    _, err = capsys.readouterr()

    assert '{"levelname": "INFO", "message": "test"}' in err


def test_setup_logging_error(capsys: "pytest.CaptureFixture"):
    """Should setup logging using JSON format (ERROR)."""
    logger = logging.setup_logging('test1', log_level='ERROR')
    logger.info("test")
    logger.error("error")

    _, err = capsys.readouterr()
    assert '{"levelname": "ERROR", "message": "error"}' in err
