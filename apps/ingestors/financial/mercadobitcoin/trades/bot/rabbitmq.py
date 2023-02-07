import pika


params = pika.URLParameters("amqp://guest:guest@rabbitmq:5672/")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare('test-orders')

def publish(msg):
    channel.basic_publish(exchange='', routing_key='test-orders', body=msg)
