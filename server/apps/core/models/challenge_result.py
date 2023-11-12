from django.db import models
from django.contrib.postgres.fields import ArrayField


class ChallengeResult(models.Model):
    challenge = models.ForeignKey(
        'Challenge',
        related_name='challenge_results',
        on_delete=models.CASCADE,
        db_index=True,
    )
    output = ArrayField(models.TextField())
    error = ArrayField(models.TextField())

    def __str__(self):
        return self.file
    
    class Meta:
        db_table = 'challenge_results'

        verbose_name = 'python challenge result'
        verbose_name_plural = 'python challenge results'
