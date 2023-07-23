from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta


@shared_task(ignore_result=True)
def send_event(user, event_one, day):
    email = EmailMultiAlternatives(
        subject=f"Напоминание о мероприятии {event_one.name}",
        to=[user.email],
    )
    email.attach_alternative(
        f"Уведомляем вас, что вы согласились посетить {event_one.name}.<br>"
        f"{event_one.description}.<br>"
        f"Мероприятие проходит {day} {event_one.meeting_time}.",
        "text/html",
    )
    email.send()


@shared_task(ignore_result=True)
def send_new_event(user_id: int):
    user_model = get_user_model()
    try:
        user = user_model.objects.get(id=user_id)
    except user_model.DoesNotExist:
        return

    if not user.email and user.notify is True:
        return


@shared_task(ignore_result=True)
def check_reminder_24_hour():
    for user in get_user_model().objects.all():

        if not user.email:
            return

        for event_one in user.events.all():
            time_from = event_one.meeting_time - timedelta(days=1)

            if datetime.now() >= time_from and event_one.meeting_time > datetime.now():
                day = "завтра"
                send_event.delay(user, event_one, day)


@shared_task(ignore_result=True)
def check_reminder_6_hour():
    for user in get_user_model().objects.all():

        if not user.email:
            return

        for event_one in user.events.all():
            time_from = event_one.meeting_time - timedelta(hours=6)
            time_after = event_one.meeting_time - timedelta(hours=5)

            if datetime.now() >= time_from and datetime.now() <= time_after:
                day = "сегодня"
                send_event.delay(user, event_one, day)