from django.conf import settings
import redis
from django.contrib.auth.models import User
from server.apps.core.models import Submission


class NotificationQueueService:
    client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    @classmethod
    def publish(cls, submission: Submission):
        user: User = submission.user
        cls.client.publish(user.username, str(submission.id))
