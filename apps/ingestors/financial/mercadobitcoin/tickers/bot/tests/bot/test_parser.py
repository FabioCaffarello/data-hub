"""spiders.parser tests."""
from unittest.mock import patch

import pytest
from bot.spiders import parser
from ingestor.tests import reference_files


class TestBotParser():

    @pytest.mark.parametrize(
        "expected",
        [
            ("https://www.mercadobitcoin.net/api/symbols")
        ]
    )
    def test_get_endpoint(self, expected):
        _parser = parser.BotParser()
        actual = _parser._get_endpoint()
        assert actual == expected

    @pytest.mark.parametrize(
        "raw_data, expected",
        [
            (reference_files.load_json('raw-tickers.json'), reference_files.load_json('tickers.json'))
        ]
    )
    def test_generator_parse_data(self, raw_data, expected):
        _parser = parser.BotParser()
        actual = _parser.generator_parse_data(raw_data)
        assert list(actual) == expected
