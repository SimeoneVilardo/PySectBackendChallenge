from django.db import models
from django.contrib.postgres.fields import ArrayField

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    reward = models.IntegerField()
    input_sample = ArrayField(models.JSONField())
    output_sample = ArrayField(models.JSONField())
    memory_limit = models.IntegerField()
    time_limit = models.IntegerField()
    input_path = models.CharField(max_length=255)
    output_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'challenges'

        verbose_name = 'python challenge'
        verbose_name_plural = 'python challenges'
