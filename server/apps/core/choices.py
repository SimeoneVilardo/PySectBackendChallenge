from django.db import models

class ChallengeSubmissionStatusChoices(models.TextChoices):
    NOT_READY = "not_ready", "not_ready"
    READY = "ready", "ready"
    PENDING = "pending", "pending"
    SUCCESS = "success", "success"
    FAILURE = "failure", "failure"