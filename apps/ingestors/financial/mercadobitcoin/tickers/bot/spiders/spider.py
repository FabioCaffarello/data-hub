import scrapy

from ingestor.spiders import basespider
from bot import config, items
from . import static, parser


class Spider(basespider.BaseSpider):
    config.LoggingConfig()
    name = 'mercadobitcoin-tickers'

    def start_requests(self):
        self._parser = parser.BotParser()
        self.logger.info(f"Receive Request with input: {self._input_data}")
        return self._first_request()

    def _first_request(self):
        yield scrapy.Request(
            url=self._parser._get_endpoint(),
            callback=self._on_processing_first_request,
        )

    def _on_processing_first_request(self, response):
        self.debug_response('tickers.json', response.json())
        self.logger.info("Receive first respone")

        data = self._parser.generator_parse_data(response.json())
        for _data in data:
            bot_items = items.BotLoader(items.BotItem())
            self.logger.info(f"Receive ticker {_data}")
            bot_items.add_fields(_data)
            yield bot_items.load_item()

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super().from_crawler(crawler, *args, **kwargs)
    #     rabbitmq_middleware = crawler.settings.get('RABBITMQ_MIDDLEWARE_ENABLED')
    #     if rabbitmq_middleware:
    #         spider.rabbitmq_middleware = rabbitmq_middleware(crawler)
    #     return spider

    # def spider_closed(self, spider):
    #     if self.rabbitmq_middleware:
    #         self.rabbitmq_middleware.connection.close()
