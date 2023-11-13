from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'users'

        verbose_name = 'user'
        verbose_name_plural = 'users'
