import logging
from pysd import service_discovery
import pika


def connect():
    """
    Connects on the queue broker and returns a connection instance
    """
    return Connection(_connect_rabbitmq())


def _connect_rabbitmq():
    log = logging.getLogger("botqueue.queue.connection.rabbitmq")
    sd = service_discovery.new_from_env()
    urlparams = sd.rabbitmq_endpoint()
    max_conn_attempts = 30
    retry_delay_sec = 60
    heartbeat_interval_sec = 60
    urlparams += "?connection_attempts={}&retry_delay={}&heartbeat={}".format(
        max_conn_attempts,
        retry_delay_sec,
        heartbeat_interval_sec
    )
    log.info("connecting to rabbitmq[{}]".format(urlparams))
    return pika.BlockingConnection(pika.URLParameters(urlparams))


def get_queues_names(botname, provider):
    input_queue = "{}.{}.input".format(provider, botname)
    output_queue = "{}.{}.output".format(provider, botname)
    return input_queue, output_queue



class Connection:
    def __init__(self, conn):
        self.__conn = conn
        self.__chan = None
        self.log = logging.getLogger("botqueue.queue.connection")


class Queue:
    """
    Queue abstraction using a RabbitMQ Blocking Connection. All methods will be synchronous.
    When the queue @max_size is achieved any call to push will block till space is freed on the queue.
    """

    def __init__(self, connection, name, max_size=10000, cache_enabled=True, cache_max_age=10.0):
        if max_size <= 0:
            raise InvalidSizeError("Invalid queue size: {}".format(max_size))

        self._cache_enabled = cache_enabled
        self._lastlen_timestamp = 0
        self._lastlen = 0
        self._cache_max_age = cache_max_age
        self._name = name
        self._max_size = max_size
        self._connection = connection
        self._log = logging.getLogger(
            "botqueue.queue.{}".format(self.__class__.__name__)
        )
        self._log.debug("declaring queue")
        self._declare_queue()

    def _declare_queue(self, passive=False):
        return self._connection.declare_queue(self._name, passive)



class InvalidSizeError(Exception):
    pass
