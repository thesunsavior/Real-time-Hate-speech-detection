import json
import pika

# Define the function to publish to RabbitMQ
async def queue_message(channel, routing_key:str, json_message: dict):
    print (f"Publishing message to queue: {json_message}")
    # Publish the message to the queue
    channel.basic_publish(
        exchange="",
        routing_key=routing_key,
        body=json.dumps(json_message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )
