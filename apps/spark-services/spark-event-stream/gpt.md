
project archtecture:

|____event_stream
| |____config
| | |____config.py
| |____controller
| | |____controller.py
| |____jobs
| | |____jobId.py
| | |____newJobId.py
| |____utils
| | |____utils.py
| |____main.py
| |____messaging
|   |____rabbitmq
|     |____consumer.py
|____configs
  |____new-job-id.json
  |____job-id.json

# event_stream/config/config.py
import os
import json
from dataclasses import dataclass


@dataclass
class Config:
    id: str
    name: str

class ConfigService:
    def __init__(self):
        self.configs = {}

    def add_config(self, config: Config):
        self.configs[config.id] = config

    def get_config(self, config_id: str) -> Config:
        return self.configs[config_id]

    def get_all_configs(self) -> list:
        return list(self.configs.values())


def load_configs_from_directory(directory: str) -> ConfigService:
    config_service = ConfigService()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                config_data = json.load(file)
                config = Config(**config_data)
                config_service.add_config(config)

    return config_service

# event_stream/messaging/rabbitmq/consumer.py
import aio_pika
import asyncio


class RabbitMQService:
    def __init__(self, host='localhost', port=5672, username='guest', password='guest'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(host=self.host, port=self.port, login=self.username, password=self.password)
        self.channel = await self.connection.channel()

    def on_connection_error(self, unused_connection, error):
        print(f"Connection error: {error}")
        self.connection.close()

    async def create_queue(self, queue_name):
        queue = await self.channel.declare_queue(queue_name)


    async def publish_message(self, queue_name, message):
        await self.channel.basic_publish(exchange='', routing_key=queue_name, body=message)

    async def consume_queue(self, queue_name, callback):
        await self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        await self.channel.start_consuming()

    async def close_connection(self):
        await self.channel.close()
        self.connection.close()

# event_stream/utils/utils.py
import inflection

def to_camel_case(raw_text):
    return inflection.camelize(raw_text, False)

# event_stream/main.py
import asyncio
from pathlib import Path
from event_stream.config.config import load_configs_from_directory
from event_stream.utils.utils import to_camel_case
from event_stream.messaging.rabbitmq.consumer import RabbitMQService
from event_stream.controller.controller import process_message


async def consume_queue(job_config, rabbitmq_service, queue_name):
    async def callback(message):
        # Process the message here
        print(f"Received message from queue '{queue_name}': {message.body.decode()}")
        message_body = message.body.decode()
        await process_message(job_config, message_body)

        await message.ack()  # Acknowledge the message

    async with rabbitmq_service.connection:
        channel = await rabbitmq_service.connection.channel()
        await channel.set_qos(prefetch_count=1)  # Limit unacknowledged messages to 1
        queue = await channel.declare_queue(queue_name)
        await queue.consume(callback)

        while True:
            await asyncio.sleep(0.1)



async def main():
    configs = load_configs_from_directory(Path(__file__).parent.parent / 'configs/jobs')
    all_configs = configs.get_all_configs()

    loop = asyncio.get_event_loop()
    tasks = []

    for job_config in all_configs:
        queue_name = to_camel_case(job_config.id)
        rabbitmq_service = RabbitMQService()  # Create a separate RabbitMQ service for each queue
        await rabbitmq_service.connect()
        await rabbitmq_service.create_queue(queue_name)

        task = asyncio.create_task(consume_queue(job_config, rabbitmq_service, queue_name))
        tasks.append(task)

    await asyncio.gather(*tasks)  # Wait for all tasks to complete

    for task in tasks:
        task.cancel()

    await asyncio.sleep(0.1)
    await rabbitmq_service.close_connection()



if __name__ == "__main__":
    asyncio.run(main())


# event_stream/controller/controller.py
import logging
from dataclasses import dataclass
from typing import Dict, Any
import json
from event_stream.config.config import JobConfig
import importlib

@dataclass
class MessageParameters:
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    status: Dict[str, Any]


class MessageProcessor:
    @staticmethod
    async def process_message(job_config: JobConfig, message_body: str):
        # Parse the message body and validate the fields
        print(job_config)
        message_params = MessageProcessor.parse_message_body(message_body)
        MessageProcessor.validate_message_params(message_params)

        # Perform additional processing or trigger a job based on the message data
        # ...
        # Import the module based on job_config.id
        module_name = f"event_stream.jobs.{job_config.id}"
        try:
            job_module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            logging.error(f"Module '{module_name}' not found")
            return

        # Trigger the job
        job_module.trigger_job(message_params.data)

    @staticmethod
    def parse_message_body(message_body: str) -> MessageParameters:
        try:
            parsed_body = json.loads(message_body)
        except json.JSONDecodeError as e:
            print(f"Failed to parse message body: {e}")
            raise ValueError("Invalid message body")

        message_data = parsed_body.get("data", {})
        message_metadata = parsed_body.get("metadata", {})
        message_status = parsed_body.get("status", {})

        print("Message body parsed successfully")
        return MessageParameters(data=message_data, metadata=message_metadata, status=message_status)

    @staticmethod
    def validate_message_params(message_params: MessageParameters):
        if not message_params.data:
            print("Invalid message: Missing data")
            raise ValueError("Invalid message: Missing data")
        # Additional validation rules
        # ...

        print("Message parameters validated successfully")


async def process_message(job_config, message_body: str, message):
    # print(job_config)
    await MessageProcessor.process_message(job_config, message_body)
