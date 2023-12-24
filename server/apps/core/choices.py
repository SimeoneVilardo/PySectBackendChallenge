from django.db import models


class ChallengeSubmissionStatusChoices(models.TextChoices):
    NOT_READY = "not_ready"
    READY = "ready"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
