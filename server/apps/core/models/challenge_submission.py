from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField

from server.apps.core.choices import ChallengeSubmissionStatusChoices


class ChallengeSubmission(models.Model):
    challenge = models.ForeignKey(
        "Challenge",
        related_name="challenge_submissions",
        on_delete=models.CASCADE,
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        related_name="challenge_submissions",
        on_delete=models.CASCADE,
        db_index=True,
    )
    lambda_name = models.CharField(max_length=255, blank=True, null=True)
    src_path = models.CharField(max_length=255, blank=False, null=False)
    output = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=100,
        choices=ChallengeSubmissionStatusChoices.choices,
        default=ChallengeSubmissionStatusChoices.NOT_READY,
    )
    memory = models.IntegerField(null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    """
    def clean(self):
        # Check if the status is 'SUCCESS' before enforcing the unique constraint
        if self.status == ChallengeSubmissionStatusChoices.SUCCESS:
            existing_submissions = ChallengeSubmission.objects.filter(
                challenge=self.challenge,
                user=self.user,
                status=ChallengeSubmissionStatusChoices.SUCCESS,
            ).exclude(pk=self.pk)

            if existing_submissions.exists():
                raise ValidationError(
                    {'status': 'There is already a successful submission for this user and challenge.'}
                )

        super().clean()
    """

    class Meta:
        db_table = "challenge_submissions"

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
