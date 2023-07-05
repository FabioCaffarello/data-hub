import unittest
from unittest.mock import MagicMock, patch
from botstatscollector import statsd_collector


class TestStatsDCollector(unittest.TestCase):
    def setUp(self):
        self.collector = statsd_collector.StatsDCollector("test_bot")
        self.collector._client = MagicMock()

    def test_increment_metric(self):
        mock_client = self.collector._client

        self.collector.increment_metric("test_metric", tags=["tag1", "tag2"])
        expected_metric = "test_metric#bot.name=test_bot,tag1,tag2"
        mock_client.incr.assert_called_with(expected_metric)

    def test_increment_metric_no_tags(self):
        mock_client = self.collector._client

        self.collector.increment_metric("test_metric")
        expected_metric = "test_metric#bot.name=test_bot"
        mock_client.incr.assert_called_once_with(expected_metric)

    def test_increment_metric_non_list_tags(self):
        with self.assertRaises(TypeError):
            self.collector.increment_metric("test_metric", tags="tag1")

    def test_time_metric(self):
        mock_client = self.collector._client
        self.collector.time_metric("test_metric", 1000, tags=["tag1", "tag2"])
        expected_metric = "test_metric#bot.name=test_bot,tag1,tag2"
        mock_client.timing.assert_called_once_with(
            expected_metric,
            1000
        )

    def test_time_metric_no_tags(self):
        mock_client = self.collector._client

        self.collector.time_metric("test_metric", 1000)
        expected_metric = "test_metric#bot.name=test_bot"
        mock_client.timing.assert_called_once_with(expected_metric, 1000)

    def test_parse_statsd_metric_non_list_tags(self):
        with self.assertRaises(TypeError):
            self.collector.parse_statsd_metric("test_metric", "tag1")

    def test_parse_statsd_metric_empty_tags(self):
        metric = self.collector.parse_statsd_metric("test_metric", [])
        expected_metric = "test_metric#bot.name=test_bot"
        self.assertEqual(metric, expected_metric)

    def test_parse_statsd_metric(self):
        metric = self.collector.parse_statsd_metric("test_metric", ["tag1", "tag2"])
        expected_metric = "test_metric#bot.name=test_bot,tag1,tag2"
        self.assertEqual(metric, expected_metric)

if __name__ == "__main__":
    unittest.main()
