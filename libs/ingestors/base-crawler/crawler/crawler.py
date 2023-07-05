import logging
import uuid
from scrapy import signals
from twisted.internet import defer
from pyoutput import output
from pystatus import errors


class InvalidOutputError(Exception):
    pass


class BaseCrawler:
    """
    A layer on top of the Scrapy crawler that will provide the spider generated items as a twisted deferreds.
    This makes it very easy to run a crawler and get all its outputs
    """
    def __init__(self, crawler, input_msg, debug):
        self._log = logging.getLogger(
            "basecrawler.crawler.{}".format(self.__class__.__name__)
        )
        self._crawler = crawler
        self._debug = debug
        self._input_msg = input_msg
        self._processingId = str(uuid.uuid4())
        self._finished = False
        self._output_deferred = None
        self._pending_outputs = list()
        self._outputs_produced = 0
        self._process()

    def get_output(self):
        """
        Returns a deferred where you can wait for an output to be produced.
        Must be called multiple times until the returned deferred produces a None value.
        You cant call get_output concurrently to get the same output, it wont work.
        """
        if self._output_deferred is not None:
            self._log.warning(
                "Called get_output twice for the same output, this is not supported"
            )
            return None

        if self.finished():
            self._log.debug("Already finished, returning None")
            deferred = defer.Deferred()
            deferred.callback(None)
            return deferred

        if self._pending_outputs == []:
            self._log.debug("No pending output, returning deferred")
            self._output_deferred = defer.Deferred()
            return self._output_deferred

        self._log.debug("We have a pending output, returning it")
        output = self._pending_outputs.pop(0)
        deferred = defer.Deferred()
        deferred.callback(output)
        return deferred

    def _process(self):
        self._log.info("Handling input: {}".format(self._input_msg))

        self._crawler.signals.connect(
              self._on_item_scrapped, signal=signals.item_scraped
        )

        self._crawler.signals.connect(
              self._on_spider_closed, signal=signals.spider_closed
        )

        self._crawler.signals.connect(
              self._on_spider_idle, signal=signals.spider_idle
        )

        self._crawler.signals.connect(
              self._on_spider_error, signal=signals.spider_error
        )
        try:
              deferred_crawl = self._crawler.crawl(
                  input_msg=self._input_msg, self._debug
              )
        except Exception as err:
            self._log.exception("error starting crawler, sending error on output")
            self._push_error_output(output.new_unhandled_error_status(err))
        else:
            deferred_crawl.addErrback(self._on_start_crawling_error)

    def _on_spider_error(self, failure, response, spider):
        self._log.warning("received signals.spider_error")
        self._handle_failure(failure)

    def _on_spider_idle(self, spider):
        self._log.info("Spider idle")

    def _on_spider_closed(self, spider, reason):
        self._log.info("Spider closed reason: " + str(reason))
        if spider.eos is not None:
            self._handle_end_of_stream(spider.eos)
        self._finish()

    def _handle_end_of_stream(self, item):
        self._log.info("generating end of stream")
        result = self._new_result_from_output(item)
        return self._push_output(result)

    def _on_item_scrapped(self, item, response, spider):
        if not isinstance(item, output.Output):
            raise InvalidOutputError(
                "Item: {} is not a valid Output instance".format(item)
            )

        result = self._new_result_from_output(item)
        return self._push_output(result)

    def _new_result_from_output(self, output):
        status = self._create_output_status(output)
        metadata = self._create_output_metadata(output)
        return {"data": output.data, "metadata": metadata, "status": status}

    def _create_output_metadata(self, outputmsg):
        metadata = output.new_metadata(self._input_msg, self._processingId)
        metadata.update(outputmsg.metadata)
        if outputmsg.source_uris != {}:
            metadata["sourceURIs"] = outputmsg.source_uris
        return metadata

    def _create_output_status(self, output):
        status = {"code": output.status_code, "detail": output.status_detail}
        if output.status_pages is not None:
            status["pages"] = {
                "index": output.status_pages.index,
                "total": output.status_pages.total,
            }
        return status

    def _push_error_output(self, status):
            self._push_output(
                {"status": status, "metadata": output.new_metadata(self._input_msg)}
            )

    def _push_output(self, data):
        if self.finished():
            self._log.warning("cant push output on finished crawler")
            return
        self._log.debug("Generated output: {0}".format(data))
        self._outputs_produced += 1
        if self._output_deferred is not None:
            self._log.debug("Already have deferred, calling callback")
            deferred = self._output_deferred
            self._output_deferred = None
            deferred.callback(data)
            return
        self._log.debug("Output has been produced before a call to get_output()")
        self._pending_outputs.append(data)

    def finished(self):
        """
        Returns True if finished processing and all outputs already been get
        """
        return self._finished and len(self._pending_outputs) == 0


    def _finish(self):
        if self._finished:
            return

        self._log.info("lets finish the process")
        if self._outputs_produced == 0:
            self._log.warning("finished crawling without any output, this is an error")
            self._handle_no_output_produced()

        self._finished = True
        if self._output_deferred is not None:
            self._output_deferred.callback(None)
            self._output_deferred = None

    def _on_start_crawling_error(self, failure):
        self._log.warning("we have a failure on the start_crawling method")
        self._handle_failure(failure)
        self._log.warning("finishing the crawler")
        self._finish()

    def _handle_failure(self, failure):
        self._log.warning("sending error output: {0}".format(failure))
        failure.trap(Exception)
        status = output.new_unhandled_error_status(failure)
        if failure.check(errors.CrawlingError) is not None:
            status = output.new_status(
                failure.value.status_code,
                failure.value.status_detail,
            )
        self._push_error_output(status)

    def _handle_no_output_produced(self):
        self._log.warning("sending no output produced error")
        status = output.new_no_output_produced_error_status()
        self._push_error_output(status)
