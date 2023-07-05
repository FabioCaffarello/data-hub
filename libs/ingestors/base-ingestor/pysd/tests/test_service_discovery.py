import unittest
import os
from unittest import mock
from pysd import service_discovery


class TestServiceDiscovery(unittest.TestCase):
    def setUp(self):
        self.envvars = {
            "RABITMQ_PORT_5672": "tcp://localhost:5672"
        }
        self.sd = service_discovery.ServiceDiscovery(self.envvars)

    def test__init__with_envvars(self):
        self.assertEqual(self.sd._vars, self.envvars)

    def test__init__with_none_envvars(self):
        with self.assertRaises(service_discovery.UnrecoverableError):
            service_discovery.ServiceDiscovery(None)

    @mock.patch.dict("os.environ", {"RABITMQ_PORT_5672": "tcp://localhost:5672"})
    def test_new_from_env(self):
        sd = service_discovery.new_from_env()
        self.assertIsInstance(sd, service_discovery.ServiceDiscovery)
        self.assertEqual(sd._vars, os.environ)

    def test__get_endpoint(self):
        endpoint = self.sd._get_endpoint("RABITMQ_PORT_5672")
        self.assertEqual(endpoint, "http://localhost:5672")

    def test__get_endpoint_with_custom_protocol(self):
        endpoint = self.sd._get_endpoint("RABITMQ_PORT_5672", "amqp")
        self.assertEqual(endpoint, "amqp://localhost:5672")

    def test__get_endpoint_with_missing_varname(self):
        with self.assertRaises(service_discovery.ServiceUnavailableError):
            self.sd._get_endpoint("INVALID_VARNAME")

    def test_rabbitmq_endpoint(self):
        endpoint = self.sd.rabbitmq_endpoint()
        self.assertEqual(endpoint, "amqp://localhost:5672")


if __name__ == "__main__":
    unittest.main()
