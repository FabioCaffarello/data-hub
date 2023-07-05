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
