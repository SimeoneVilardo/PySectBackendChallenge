from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Exists, OuterRef
from server.apps.core.choices import SubmissionStatusChoices
from server.apps.core.models.submission import Submission
from server.apps.core.models.user import User


class ChallengeManager(models.Manager):
    user = None

    def set_user(self, user: User):
        self.user = user
        return self.get_queryset()

    def get_queryset(self) -> QuerySet:
        queryset = (
            super()
            .get_queryset()
            .filter(models.Q(users__isnull=True) | models.Q(users__in=[self.user]))
            .annotate(
                is_completed=Exists(
                    Submission.objects.filter(
                        challenge_id=OuterRef("pk"),
                        status=SubmissionStatusChoices.SUCCESS,
                    )
                )
            )
            .order_by("id")
        )
        return queryset


class Challenge(models.Model):
    objects = models.Manager()
    users_objects = ChallengeManager()

    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    points = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    input_sample = models.TextField()
    output_sample = models.TextField()
    memory_limit = models.IntegerField()
    time_limit = models.IntegerField()
    input = models.TextField()
    output = models.TextField()
    users = models.ManyToManyField(
        User, related_name="available_challenges", blank=True
    )

    @property
    def is_completed_prop(self):
        return self.is_completed

    def __str__(self):
        return self.name

    class Meta:
        db_table = "challenges"

        verbose_name = "python challenge"
        verbose_name_plural = "python challenges"
