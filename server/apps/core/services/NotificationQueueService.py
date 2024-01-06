from django.conf import settings
import redis
from django.contrib.auth.models import User
from server.apps.core.models import ChallengeSubmission


class NotificationQueueService:
    client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    @classmethod
    def publish(cls, challenge_submission: ChallengeSubmission):
        user: User = challenge_submission.user
        cls.client.publish(user.username, str(challenge_submission.id))
