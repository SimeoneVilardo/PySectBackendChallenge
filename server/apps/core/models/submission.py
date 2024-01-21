from django.contrib.auth.models import User
from django.db import models
from server.apps.core.choices import SubmissionStatusChoices


class Submission(models.Model):
    challenge = models.ForeignKey(
        "Challenge",
        related_name="submissions",
        on_delete=models.CASCADE,
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        related_name="submissions",
        on_delete=models.CASCADE,
        db_index=True,
    )
    src_data = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=100,
        choices=SubmissionStatusChoices.choices,
        default=SubmissionStatusChoices.READY,
    )
    memory = models.IntegerField(null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "submissions"

        verbose_name = "python challenge submission"
        verbose_name_plural = "python challenge submissions"

        """
        constraints = [
            models.UniqueConstraint(
                fields=['challenge', 'user', 'status'],
                name='unique_challenge_user_success'
            )
        ]
        """
