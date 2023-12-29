from typing import AsyncGenerator
import boto3
from django.conf import settings


class QueueService:
    sqs = boto3.resource("sqs", region_name="eu-north-1")
    queue_url = "https://sqs.eu-north-1.amazonaws.com/340650704585/challenge-submission-status.fifo"
    queue = sqs.Queue(queue_url)
    _listener = None

    @classmethod
    async def status_consumer(cls) -> AsyncGenerator:
        if cls._listener is None:
            cls._listener = cls._create_listener()
        return cls._listener

    @classmethod
    async def _create_listener(cls) -> AsyncGenerator:
        while True:
            messages = cls.queue.receive_messages(
                AttributeNames=["All"], MessageAttributeNames=["All"], MaxNumberOfMessages=1, WaitTimeSeconds=20
            )
            for message in messages:
                data = message.message_attributes
                yield data
                message.delete()
