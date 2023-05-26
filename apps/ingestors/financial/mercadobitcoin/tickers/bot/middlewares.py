# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import pika
from scrapy import Request
from scrapy.exceptions import NotConfigured
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BotSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BotDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class RabbitMQMiddleware:
#     def __init__(self, connection_params, queue_name):
#         self.connection_params = connection_params
#         self.queue_name = queue_name
#         self.connection = None
#         self.channel = None

#     @classmethod
#     def from_crawler(cls, crawler):
#         connection_params = pika.URLParameters(crawler.settings.get('RABBITMQ_URI'))
#         queue_name = crawler.settings.get('RABBITMQ_QUEUE_INPUT')
#         if not connection_params.host or not queue_name:
#             raise NotConfigured('RabbitMQMiddleware is not properly configured')
#         return cls(connection_params, queue_name)

#     def start_consuming(self):
#         self.connection = pika.BlockingConnection(self.connection_params)
#         self.channel = self.connection.channel()
#         self.channel.queue_declare(queue=self.queue_name)
#         self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.handle_delivery)
#         self.channel.start_consuming()

#     def handle_delivery(self, channel, method, properties, body):
#         url = body.decode()
#         request = Request(url=url)
#         self.spider.crawler.engine.schedule(request, self.spider)

#     def process_spider_input(self, response, request, spider):
#         self.spider = spider
#         if not hasattr(self, 'connection'):
#             self.start_consuming()
#         return None
