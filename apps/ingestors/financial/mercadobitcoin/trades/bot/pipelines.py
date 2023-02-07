# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BotPipeline:
    def process_item(self, item, spider):
        return item












import os

from itemadapter import ItemAdapter


# class DeleteOutputPipeline:

#     def open_spider(self, spider):
#         try:
#             os.remove("data/output.jsonl")
#         except OSError as e:
#             pass


# class BotPipeline:
#     def process_item(self, item, spider):
#         return item

# docker-compose.yml
version: '3'
services:
  mongodb:
    image: mongo
    ports:
      - "27017:27017"
    volumes:
      - ./data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: guest
      MONGO_INITDB_ROOT_PASSWORD: guest
    networks:
      - data-hub-network

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
      RABBITMQ_DEFAULT_VHOST: /
    networks:
      - data-hub-network

networks:
  data-hub-network:
    external: true
    driver: bridge

# schenas/output.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "tickers",
  "description": "A user model for a Scrapy crawler",
  "type": "object",
  "properties": {
      "ticker": {
          "type": "string",
          "description": "The ticker's symbol"
      }
  },
  "required": ["ticker"]
}


# settings.py
RABBITMQ_URI = "amqp://guest:guest@rabbitmq:5672/"
MONGO_URI = "mongodb://guest:guest@mongodb:27017/test_database"
ITEM_PIPELINES = {
  'bot.pipelines.RabbitMQPipeline': 300,
  'bot.pipelines.MongoPipeline': 600,
}

# models
from pydantic import BaseModel
import json

# Load the JSON output schema from a file
with open("schemas/output.json") as f:
    schema = json.load(f)

# Generate the model class based on the schema
class Ticker(BaseModel):
    __root__: dict

    class Config:
        orm_mode = True

# pipeline.py
import asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pika import BlockingConnection, ConnectionParameters
from .models import Ticker
import json


async def process_item(item, settings):
    client = AsyncIOMotorClient(settings['MONGO_URI'])
    await init_beanie(client.db_name, document_models=[Ticker])
    _doc = Ticker(**item)
    await _doc.save()

class MongoPipeline:
    async def process_item(self, item, spider):
        await process_item(item, self.settings)

class RabbitMQPipeline:
    def __init__(self, rabbitmq_uri):
        self.connection = BlockingConnection(ConnectionParameters(rabbitmq_uri))
        self.channel = self.connection.channel()

    @classmethod
    def from_settings(cls, settings):
        rabbitmq_uri = settings.get('RABBITMQ_URI')
        return cls(rabbitmq_uri)

    def open_spider(self, spider):
        self.channel.queue_declare(queue='items')

    def process_item(self, item, spider):
        self.channel.basic_publish(
            exchange='',
            routing_key='items',
            body=json.dumps(dict(item)))
        return item

    def close_spider(self, spider):
        self.connection.close()
