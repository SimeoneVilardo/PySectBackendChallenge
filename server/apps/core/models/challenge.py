from django.db import models
from decimal import Decimal


class Challenge(models.Model):
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    points = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=[(Decimal(x), str(x)) for x in [i * 0.5 for i in range(11)]],
    )
    input_sample = models.TextField()
    output_sample = models.TextField()
    memory_limit = models.IntegerField()
    time_limit = models.IntegerField()
    input = models.TextField()
    output = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "challenges"

        verbose_name = "python challenge"
        verbose_name_plural = "python challenges"
