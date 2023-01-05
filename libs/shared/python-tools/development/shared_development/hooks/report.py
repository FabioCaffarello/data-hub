"""Pytest hook to add description to the HTML report."""

import pytest
from py.xml import html


def pytest_html_results_table_header(cells):
    """Add header to the HTML report."""
    cells.insert(2, html.th("Description"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """Add Row to the HTML report."""
    cells.insert(2, html.td(report.description))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add description to the HTML report."""
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__).lstrip().split('\n')[0]
