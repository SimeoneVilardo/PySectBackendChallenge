from django.db import models

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    src = models.CharField(max_length=255)
    reward = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'challenges'

        verbose_name = 'python challenge'
        verbose_name_plural = 'python challenges'
