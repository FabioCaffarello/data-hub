import scrapy

from ingestor.spiders import basespider
from bot import rabbitmq, config
from . import static, parser


class Spider(basespider.BaseSpider):
    config.LoggingConfig()
    name = 'mercadobitcoin-trades'

    def start_requests(self):
        self._parser = parser.BotParser()
        self.logger.info(f"Receive Request with input: {self._input_data}")
        return self._first_request()

    def _first_request(self):
        yield scrapy.Request(
            # url=static.SWAGGER_ENDPOINT,
            url=self._parser._get_endpoint(),
            callback=self._on_processing_first_request,
        )

    def _on_processing_first_request(self, response):
        # self.logger.info(yaml.safe_load(response.body))
        # self.debug_response('swagger.yaml', yaml.safe_load(response.body))
        self.logger.info(response.body)
        self.logger.info(self._input_data)
        self.debug_response('tickers.json', response.json())
        # rabbitmq.publish('dummie msg')
        return
