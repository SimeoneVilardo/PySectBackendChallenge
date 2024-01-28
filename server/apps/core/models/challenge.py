from django.db import models
from decimal import Decimal

from django.db.models.query import QuerySet

from server.apps.core.models.user import User

class ChallengeManager(models.Manager):
    user = None

    def set_user(self, user: User):
        self.user = user
        return self.get_queryset()

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(models.Q(users__isnull=True) | models.Q(users__in=[self.user]))

class Challenge(models.Model):
    objects = models.Manager()
    users_objects = ChallengeManager()

    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    points = models.IntegerField(choices=[(i, str(i)) for i in range(1,11)])
    input_sample = models.TextField()
    output_sample = models.TextField()
    memory_limit = models.IntegerField()
    time_limit = models.IntegerField()
    input = models.TextField()
    output = models.TextField()
    users = models.ManyToManyField(User, related_name='available_challenges', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "challenges"

        verbose_name = "python challenge"
        verbose_name_plural = "python challenges"
