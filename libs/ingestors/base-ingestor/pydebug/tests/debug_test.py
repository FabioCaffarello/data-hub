import unittest
from unittest import mock
import os
import logging
import tempfile
import shutil
from pydebug.debug import new, EnabledDebug, DisabledDebug


class TestNew(unittest.TestCase):
    def test_new_debug_enabled(self):
        debug_enabled = True

        with mock.patch("logging.debug") as mock_debug:
            with tempfile.TemporaryDirectory() as temp_dir:
                storage = new(debug_enabled, temp_dir)
                self.assertIsInstance(storage, EnabledDebug)
                self.assertEqual(storage._debug_dir, temp_dir)

    def test_new_debug_disabled(self):
        debug_enabled = False
        debug_storage_dir = None

        with mock.patch("logging.debug") as mock_debug:
            storage = new(debug_enabled, debug_storage_dir)

        mock_debug.assert_called_with("Debug disabled, creating stub")
        self.assertIsInstance(storage, DisabledDebug)


# class TestEnabledDebug(unittest.TestCase):
#     def setUp(self):
#         self.debug_dir = "/debug"
#         self.debug = EnabledDebug(self.debug_dir)

#     @mock.patch('pydebug.debug.shutil.rmtree')
#     @mock.patch('pydebug.debug.os.makedirs')
#     def test__create_dir(self, mock_makedirs, mock_rmtree):
#         path = "/path/to/dir"
#         mock_rmtree.return_value = None  # Configure the mock to do nothing
#         mock_makedirs.return_value = None  # Configure the mock to do nothing

#         # Call the method
#         self.debug._create_dir(path)

#         # Assertions
#         mock_rmtree.assert_called_once_with(path, ignore_errors=True)
#         mock_makedirs.assert_called_once_with(path)

#     def tearDown(self):
#         shutil.rmtree(self.debug_dir, ignore_errors=True)

#     @mock.patch('pydebug.debug.shutil.rmtree')
#     @mock.patch('pydebug.debug.os.makedirs')
#     def test_save_response(self, mock_makedirs, mock_rmtree):
#         mock_makedirs.return_value = None  # Configure the mock to do nothing
#         mock_rmtree.return_value = None  # Configure the mock to do nothing

#         filename = "response.txt"
#         response_body = b"Response body"
#         self.debug.save_response(filename, response_body)

#         response_dir = os.path.join(self.debug._debug_dir, "responses")
#         self.assertTrue(mock_makedirs.called)  # Assert that makedirs was called
#         mock_makedirs.assert_called_once_with(response_dir)  # Assert the correct arguments for makedirs
#         self.assertEqual(len(os.listdir(response_dir)), 1)

#     def test_save_captcha(self):
#         solution = "captcha_solution"
#         image = b"Captcha image"

#         self.debug.save_captcha(solution, image)

#         captchas_dir = "{}/captchas/".format(self.debug_dir)
#         expected_file = os.path.join(captchas_dir, "1-captcha_solution")
#         self.assertTrue(os.path.isfile(expected_file))
#         with open(expected_file, "rb") as file:
#             saved_captcha = file.read()
#         self.assertEqual(saved_captcha, image)


class TestDisabledDebug(unittest.TestCase):
    def setUp(self):
        self.debug = DisabledDebug()

    def test_save_response(self):
        filename = "response.txt"
        response = "Response object"

        self.debug.save_response(filename, response)

        # No assertions made as this method does nothing

    def test_save_captcha(self):
        image = "captcha_image"
        captcha = "Captcha object"

        self.debug.save_captcha(image, captcha)

        # No assertions made as this method does nothing


if __name__ == "__main__":
    unittest.main()
