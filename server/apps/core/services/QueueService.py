import asyncio
from types import AsyncGeneratorType
from typing import AsyncGenerator
import boto3
import json
from django.conf import settings
import redis


class QueueService:
    sqs = boto3.resource("sqs", region_name="eu-north-1")
    queue_url = "https://sqs.eu-north-1.amazonaws.com/340650704585/challenge-submission-status.fifo"
    queue = sqs.Queue(queue_url)
    _listener = None

    # @classmethod
    # def status_consumer(cls):
    #     if cls._listener is None:
    #         cls._listener = cls._create_listener()
    #     return cls._listener

    # @classmethod
    # async def _create_listener(cls):
    #     while True:
    #         yield f"data: foo\n\n"
    #         await asyncio.sleep(4)

    @classmethod
    async def status_consumer(cls):
        redis_instance = redis.StrictRedis(host="localhost", port=6379, db=0)
        pubsub = redis_instance.pubsub()
        pubsub.subscribe("foo_queue")
        while True:
            for message in pubsub.listen():
                data = json.dumps({"message": message["data"].decode("utf-8")})
                yield f"data: {data}\n\n"
