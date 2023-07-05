import unittest
from botstatscollector import statsd_collector, factory


class TestNewCollector(unittest.TestCase):
    def test_new_collector_statsd(self):
        botname = "test_bot"
        stats_collector_type = "statsd"

        collector = factory.new_collector(botname, stats_collector_type)

        self.assertIsInstance(collector, statsd_collector.StatsDCollector)
        self.assertEqual(collector._botname_tag, "bot.name=test_bot")


if __name__ == "__main__":
    unittest.main()
