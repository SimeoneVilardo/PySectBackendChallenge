from django.db import models

class ChallengeSubmissionStatusChoices(models.TextChoices):
    SUCCESS = "success", "success"
    READY = "ready", "ready"
    FAILURE = "failure", "failure"