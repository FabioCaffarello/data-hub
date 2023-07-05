from botargparse import argparse as pyargparse

import unittest
from unittest.mock import patch
import argparse


class NewArgparseTestCase(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(log_level='INFO', concurrency=1))
    def test_new_argparse_default_values(self, mock_parse_args):
        description = 'Test description'
        parser = pyargparse.new(description)

        args = parser.parse_args()

        self.assertEqual(args.log_level, 'INFO')
        self.assertEqual(args.concurrency, 1)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(log_level='DEBUG', concurrency=5))
    def test_new_argparse_custom_values(self, mock_parse_args):
        description = 'Test description'
        parser = pyargparse.new(description)

        args = parser.parse_args()

        self.assertEqual(args.log_level, 'DEBUG')
        self.assertEqual(args.concurrency, 5)

if __name__ == '__main__':
    unittest.main()
