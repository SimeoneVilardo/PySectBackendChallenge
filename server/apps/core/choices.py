from django.db import models


class SubmissionStatusChoices(models.TextChoices):
    READY = "ready"
    BROKEN = "broken"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
