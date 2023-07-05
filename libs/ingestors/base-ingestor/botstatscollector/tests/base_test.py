import unittest
from unittest.mock import MagicMock
from botstatscollector import base
import time

class TestAbstractCollector(unittest.TestCase):
    def test_start_finish(self):
        collector = base.AbstractCollector()
        collector.time_metric = MagicMock()

        start_time = time.time()
        collector.start()
        # Simulate some time delay
        time.sleep(0.001)
        end_time = time.time()
        collector.finish()

        # Calculate the time difference manually
        time_diff = (end_time - start_time) * 1000

        self.assertAlmostEqual(
            collector.time_metric.call_args[0][1],
            time_diff,
            delta=0.02
        )


    def test_add_result_status(self):
        collector = base.AbstractCollector()
        collector.increment_metric = MagicMock()

        collector.add_result_status(200)

        collector.increment_metric.assert_called_once_with(
            "bot.result.status.2xx.total",
            tags=["bot.status=200"]
        )

    def test_add_result_status_unknown(self):
        collector = base.AbstractCollector()
        collector.increment_metric = MagicMock()

        collector.add_result_status(600)

        collector.increment_metric.assert_called_once_with(
            "bot.result.status.unknown.total",
            tags=["bot.status=600"]
        )


if __name__ == "__main__":
    unittest.main()
