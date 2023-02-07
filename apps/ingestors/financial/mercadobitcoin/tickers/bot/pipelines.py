import asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pika import BlockingConnection, URLParameters
from .models import Ticker
from bot.spiders.proto import spider_pb2
import json


async def process_item(item, settings):
    client = AsyncIOMotorClient(settings['MONGO_URI'])
    await init_beanie(client.db_name, document_models=[Ticker])
    _doc = Ticker(ticker=item.ticker)
    await _doc.save()

class MongoPipeline:
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    async def process_item(self, item, spider):
        await process_item(item, self.settings)

class RabbitMQPipeline:
    def __init__(self, rabbitmq_uri, rabbitmq_queue):
        self.rabbitmq_queue = rabbitmq_queue
        self.connection = BlockingConnection(URLParameters(rabbitmq_uri))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.rabbitmq_queue)

    @classmethod
    def from_settings(cls, settings):
        rabbitmq_uri = settings.get('RABBITMQ_URI')
        rabbitmq_queue = settings.get('RABBITMQ_QUEUE')
        return cls(rabbitmq_uri, rabbitmq_queue)

    def process_item(self, item, spider):
        item_pb = spider_pb2.ProtoItem(ticker=item['ticker'])
        self.channel.basic_publish(exchange='',
                                   routing_key=self.rabbitmq_queue,
                                   body=item_pb.SerializeToString())
        return item_pb

    def close_spider(self, spider):
        self.connection.close()
