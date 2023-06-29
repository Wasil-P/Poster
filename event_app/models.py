from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    meeting_time = models.DateTimeField()
    users = models.ManyToManyField("users.User", related_name="events")
    description = models.TextField(max_length=256)


    class Meta():
        db_table = "events"
        ordering = ["-meeting_time"]
