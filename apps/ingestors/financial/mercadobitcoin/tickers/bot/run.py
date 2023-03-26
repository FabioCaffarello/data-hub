# import pika
# from scrapy.crawler import CrawlerProcess
# from bot.spiders.spider import Spider
# from bot.middlewares import RabbitMQMiddleware
# from bot import settings

# # Define the connection parameters and queue name for RabbitMQ
# connection_params = pika.ConnectionParameters(host=settings.RABBITMQ_URI)
# queue_name = settings.RABBITMQ_QUEUE_INPUT

# # Create a Scrapy spider process
# process = CrawlerProcess()

# # Add the RabbitMQ middleware to the spider
# rabbitmq_middleware = RabbitMQMiddleware(connection_params, queue_name)
# process.crawl(Spider, rabbitmq_middleware=rabbitmq_middleware)

# # Start the listener for the RabbitMQ queue
# rabbitmq_middleware.start_consuming()

# # Start the Scrapy spider process
# process.start()
