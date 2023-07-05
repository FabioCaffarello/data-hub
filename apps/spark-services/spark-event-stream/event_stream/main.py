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
