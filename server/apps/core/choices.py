from django.db import models


class ChallengeSubmissionStatusChoices(models.TextChoices):
    READY = "ready"
    BROKEN = "broken"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
