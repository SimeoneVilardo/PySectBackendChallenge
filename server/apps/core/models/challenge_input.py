from django.db import models
from django.contrib.postgres.fields import ArrayField

class ChallengeInput(models.Model):
    challenge = models.ForeignKey(
        'Challenge',
        related_name='challenge_inputs',
        on_delete=models.CASCADE,
        db_index=True,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'challenge_inputs'

        verbose_name = 'python challenge input'
        verbose_name_plural = 'python challenge inputs'
