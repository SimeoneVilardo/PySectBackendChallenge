from django.db import models
from server.apps.core.models.user import User


class Reward(models.Model):
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    redemption = models.ManyToManyField(User, related_name='redeemed_rewards', blank=True)
    users = models.ManyToManyField(User, related_name='available_rewards', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "rewards"
        verbose_name = "challenge reward"
        verbose_name_plural = "challenge rewards"