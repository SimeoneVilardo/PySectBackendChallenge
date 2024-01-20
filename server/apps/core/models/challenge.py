from django.db import models


class Challenge(models.Model):
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    points = models.IntegerField()
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
