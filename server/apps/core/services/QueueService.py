import asyncio
from types import AsyncGeneratorType
from typing import AsyncGenerator
import boto3
import json
from django.conf import settings


class QueueService:
    sqs = boto3.resource("sqs", region_name="eu-north-1")
    queue_url = "https://sqs.eu-north-1.amazonaws.com/340650704585/challenge-submission-status.fifo"
    queue = sqs.Queue(queue_url)
    _listener = None

    @classmethod
    def status_consumer(cls):
        if cls._listener is None:
            cls._listener = cls._create_listener()
        return cls._listener

    # @classmethod
    # async def _create_listener(cls):
    #     while True:
    #         yield f"data: foo\n\n"
    #         await asyncio.sleep(4)

    @classmethod
    async def _create_listener(cls):
        while True:
            messages = await asyncio.to_thread(
                cls.queue.receive_messages,
                AttributeNames=["All"],
                MessageAttributeNames=["All"],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20,
            )
            for message in messages:
                attributes = message.message_attributes
                challenge_submission_id = attributes["challenge_submission_id"]["StringValue"]
                user_id = attributes["user_id"]["StringValue"]
                status = attributes["status"]["StringValue"]
                payload = {"challenge_submission_id": challenge_submission_id, "user_id": user_id, "status": status}
                yield f"data: {json.dumps(payload)}\n\n"
                await asyncio.to_thread(message.delete)
