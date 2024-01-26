# Generated by Django 5.0 on 2024-01-25 21:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('redemption', models.ManyToManyField(blank=True, related_name='rewards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'challenge reward',
                'verbose_name_plural': 'challenge rewards',
                'db_table': 'rewards',
            },
        ),
    ]
