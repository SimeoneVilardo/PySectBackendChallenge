from django.conf import settings
import redis
import boto3
import json
from server.apps.core.models import ChallengeSubmission


class SNSService:
    sns = boto3.client("sns", region_name=settings.AWS_DEFAULT_REGION)

    @classmethod
    def _publish(cls, topic_arn, message):
        cls.sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message),
        )

    @classmethod
    def publish_submission_create(cls, message: dict):
        cls._publish(settings.AWS_CHALLENGE_SUBMISSION_CREATE_TOPIC_ARN, message)
