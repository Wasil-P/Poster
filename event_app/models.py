from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives


class Event(models.Model):
    name = models.CharField(max_length=100)
    meeting_time = models.DateTimeField()
    users = models.ManyToManyField("users.User", related_name="events")
    description = models.TextField(max_length=256)

    class Meta():
        db_table = "events"
        ordering = ["-meeting_time"]


@receiver([post_save], sender=Event)
def send_new_event(sender, instance: Event, **kwargs):

    for user in get_user_model().objects.all():

        if not user.email or user.notify is False:
            return

        email = EmailMultiAlternatives(
            subject=f"Новое мероприятие: {instance.name}",
            to=[user.email],
        )
        email.attach_alternative(
            f"Приглашаем вас посетить {instance.name} {instance.meeting_time}.<br>"
            f"{instance.description}.<br>"
            "text/html",
        )
        email.send()