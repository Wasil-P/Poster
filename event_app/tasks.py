from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta


@shared_task(ignore_result=True)
def send_reminder():

    for user in get_user_model().objects.all():

        if user.events.meeting_time == datetime.now() + timedelta(days=1):
            email = EmailMultiAlternatives(
                subject=f"Напоминание о мероприятии {user.events.name}",
                to=[user.email],
            )
            email.attach_alternative(
                f"Уведомляем вас, что вы согласились посетить {user.events.name}.<br>"
                f"{user.events.description}.<br>"
                f"Мероприятие проходит завтра {user.events.meeting_time}.",
                "text/html",
            )
            email.send()

        elif user.events.meeting_time == datetime.now() + timedelta(hours=6):
            email = EmailMultiAlternatives(
                subject=f"Напоминание о мероприятии {user.events.name}",
                to=[user.email],
            )
            email.attach_alternative(
                f"Уведомляем вас, что вы согласились посетить {user.events.name}.<br>"
                f"{user.events.description}.<br>"
                f"Мероприятие проходит сегодня {user.events.meeting_time}.",
                "text/html",
            )
            email.send()


