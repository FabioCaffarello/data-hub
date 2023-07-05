import logging
import unittest
from botlog.log import log_config

class LogConfigTestCase(unittest.TestCase):

    def test_log_config_valid_level(self):
        level_str = 'DEBUG'
        log_config(level_str)

        logger = logging.getLogger(self._testMethodName)
        self.assertEqual(logger.getEffectiveLevel(), logging.DEBUG)

    def test_log_config_invalid_level(self):
        level_str = 'INVALID'
        with self.assertRaises(ValueError):
            log_config(level_str)

if __name__ == '__main__':
    unittest.main()
