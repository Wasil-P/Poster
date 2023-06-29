# Generated by Django 4.2.2 on 2023-06-28 15:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(related_name='events', to=settings.AUTH_USER_MODEL),
        ),
    ]
