import logging
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from botqueue import queue
import json
from botstatscollector import factory
from pyoutput import output
from pystatus import success, server_error, client_error
from crawler.crawler import BaseCrawler
from pydebug import debug

log = logging.getLogger("basecrawler.loop")


def run(spider_class, settings, concurrency):
    """
    Register schema, runs the mainloop, getting inputs from the queue,
    pasing them to the Spider and getting the output from the spider so them
    pushing it on the output queue.
    This function never returns, only if something really exceptional happens...
    """
    reactor.callWhenRunning(_start_loops(spider_class, settings, concurrency))
    reactor.run()
    log.warning("main loop exit, some fatal error happened on bot")


def _start_loops(spider_class, settings, concurrency):
    # register schema

    concurrency = int(concurrency)

    def start():
        log.info("running {} loops".format(concurrency))
        log.info("creating queues")

        runner = CrawlerRunner(settings)
        try:
            connection = queue.connect()
            input_queue_name, output_queue_name = queue.get_queues_names(
                spider_class.name, spider_class.provider
            )
            input_queue = queue.Queue(connection, input_queue_name)
            output_queue = queue.Queue(connection, output_queue_name)
            reactor.callWhenRunning(_new_heartbeat_sender(connection))
        except Exception as err:
            log.error("fatal error connecting to queue: {}".format(err))
            log.error("aborting")
            reactor.crash()

        log.info("created queues with success")

        for i in range(concurrency):
            log.info("Running loop {}".format(i))
            loop = Loop(
                logging.getLogger("basecrawler.loop.Loop({})".format(i)),
                input_queue,
                output_queue,
                runner,
                spider_class,
                settings
            )
            reactor.callWhenRunning(loop.run)

    return start


def _new_heartbeat_sender(connection):
    heartbeat_interval_sender = 15.0
    log = logging.getLogger("basecrawler.loop.heartbeat")

    @defer.inlineCallbacks
    def heartbeat_sender():
        while True:
            try:
                yield _sleep(heartbeat_interval_sender)
                log.info("sending heartbeat")
                connection.heartbeat()
                log.info("sent heartbeat with success")
            except Exception as err:
                log.error("error sending heartbeat: {}".format(err))
                try:
                    log.info("attempting to reconnect")
                    connection.reconnect()
                    log.info("reconnected with success")
                except Exception as err:
                    log.error("fatal error reconnecting: {}".format(err))
                    _crash(log)
    return heartbeat_sender


def _sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d

def _crash(log):
    log.info("exiting all concurrent bots, crashing twisted reactor")
    reactor.crash()
    log.info("crashed reactor, bot should exit soon")

class Loop:
    def __init__(
        self,
        logger,
        input_queue,
        output_queue,
        runner,
        spider_class,
        settings
    ):
        self.logger = logger
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._runner = runner
        self._spider_class = spider_class
        self._settings = settings
        self._stats_collector_type = settings.get("STATS_COLLECTOR_TYPE")
        self._dbg = debug.new(
            settings.get("DEBUG_STORAGE_ENABLED"), settings.get("DEBUG_STORAGE_DIR")
        )

    @defer.inlineCallbacks
    def run(self):
        try:
            self.logger.info("starting loop")
            while True:
                yield self._process_input()
        except Exception as err:
            self.logger.exception(
                "We have an unhandle exception on the loop: {}".format(err)
            )
            _crash(self.logger)

    @defer.inlineCallbacks
    def _process_input(self):
        self.logger.info("pop next input")
        wait_input = 1.0
        self._has_partial_error = False
        self._has_output_success = False
        input_msg = None
        while input_msg is None:
            try:
                input_msg = self._input_queue.pop()
            except Exception as err:
                self.logger.error("error poping input: {}".format(err))
                yield _sleep(wait_input)
                continue
            if input_msg is None:
                self.logger.debug("no input available, waiting...")
                yield _sleep(wait_input)

        stats_collector = factory.new_collector(
            self._spider_class.name, self._stats_collector_type
        )
        stats_collector.start()
        try:
            self.logger.debug("parsing input as JSON")
            input_text = input_msg.decode("utf-8")
            input_json = json.loads(input_text)
        except ValueError as err:
            self.logger.exception("error parsing input as JSON: {}".format(err))
            error_output = {
                "status": output.new_bad_request_error_status(err),
                "metadata": output.new_metadata(input_text)
            }
            self.logger.warning("Producing error output: {}".format(error_output))
            self._push_output(error_output)
        else:
            self.logger.debug("parsed input with success, running crawler")
            crawler = self._runner.create_crawler(self._spider_class)
            yield self._run_crawler(
                BaseCrawler(crawler, input_json, self._dbg), stats_collector
            )
        finally:
            self.logger.debug("sending metrics for this crawling")
            stats_collector.finish()
            self.logger.debug("done")

    @defer.inlineCallbacks
    def _run_crawler(self, basecrawler_crawler, stats_collector):
        while not basecrawler_crawler.finished():
            log.info("Getting next output")
            output = yield basecrawler_crawler.get_output()
            if output is None:
                self.logger.info("Crawler is finished")
            self.logger.info("produced output: {}".format(output))
            pushed_output = False
            try_again_sec = 1
            while not pushed_output:
                try:
                    self._push_output(output)
                    pushed_output = True
                # TODO: Needs to create a CreateOutputException
                except CreateOutputException as err:
                    self.logger.error("CreateOutputException on push output: {}".format(err.message))
                    self._has_partial_error = True
                    self._push_output_on_exception(output, err.message, err.status)
                    pushed_output = True
                except NotImplementedError as err:
                    self.logger.error("error pushing output: get_base_id not implemented on spider / {}".format(err))
                    _crash(self.logger)
                    return
                except GetBaseIDException as err:
                    self.logger.error(err)
                    _crash(self.logger)
                    return
                except Exception as err:
                    self.logger.error("exception pushing output: {}".format(err))
                    yield _sleep(try_again_sec)

            stats_collector.add_result_status(output["status"]["code"])
            if output["status"]["code"] == client_error.UNAUTHORIZED:
                stats_collector.increment_metric(
                    "bot.result.status.detail",
                    [f"bot.status.detail={output['status']['code']}"],
                )
            self.logger.info("pushed output")

    def _push_output_on_exception(self, output, detail, status_code):
        if status_code == client_error.BAD_REQUEST:
            status_code = server_error.PARSING_INVALID_DATA
        output["status"]["code"] = status_code
        output["status"]["details"] = detail
        self._push_output(output)

    def _push_output(self, output):
        status_code = output["status"]["code"]
        if status_code == success.EOS and self._has_partial_error:
            output["status"]["code"] = success.PARTIAL_STREAM
            output["status"]["detail"] = "Partial Stream setted by basecrawler"
        if status_code == success.EOS and not self._has_output_success:
            output["status"]["code"] = server_error.STREAM_FAILED_EOS
            output["status"]["detail"] = "Stream failed setted by basecrawler"
        base_id = self._get_base_id(output)
        self.logger.info("using this base_id = {}".format(base_id))
        # set schema id
        # create output
        if status_code == success.OK:
            self._has_output_success = True
        self.logger.info("Output pushed with success: {}".format(output))


    def _get_base_id(self, output):
        try:
            if _is_not_output_status_ok(output["status"]["code"]):
                self.logger.info("using base_id from input")
                return _base_id_from_input_and_status_code(output)
            self.logger.info("using base_id from spider func")
            return str(self._spider_class.get_base_id(output))
        except Exception as err:
            raise GetBaseIDException(
                "unable get base id from spider / error = {}".format(err)
            )


class GetBaseIDException(Exception):
    pass

def _is_not_output_status_ok(status_code):
    return status_code != success.OK


def _base_id_from_input_and_status_code(output):
    input_ = output["metadata"]["input"]
    status_code = output["status"]["code"]
    return "{}{}".format(input_, status_code)
