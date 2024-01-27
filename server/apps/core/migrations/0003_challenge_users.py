# Generated by Django 5.0 on 2024-01-27 20:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_challenge_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='available_challenges', to=settings.AUTH_USER_MODEL),
        ),
    ]
