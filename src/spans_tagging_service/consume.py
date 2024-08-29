
import pika
import json
import os
import sys

from redis_om import get_redis_connection, HashModel

from config import Config
from utils.model_factory import get_model
from utils.span_inference import spans_inference

from dotenv import load_dotenv

load_dotenv()


config = Config()

model, tokenizer = get_model(config.MODEL_NAME)
infer_fn = spans_inference(model, tokenizer)

redis = get_redis_connection(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    decode_responses=True
)


class SpanMessage(HashModel):
    id: str
    message: str
    spans: list

    class Meta:
        database = redis


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        body = body.decode("utf-8")
        json_data = json.loads(body)

        message_id = json_data["id"]
        message = json_data["message"]
        spans = infer_fn(message)

        json_message = {"id": message_id, "message": message, "spans": spans}

        # save to Redis
        try:
            span_message = SpanMessage(**json_message)
            span_message.save()
        except:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(
            queue=config.SPAN_TAGGING_QUEUE, on_message_callback=callback
        )

        print("Waiting for messages. To exit press CTRL+C")

        channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
