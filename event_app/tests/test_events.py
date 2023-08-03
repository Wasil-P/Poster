from django import test
from rest_framework import status

from ..models import Event
from datetime import datetime, timedelta


class TestEventListAPIView(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        # создание переменных для мероприятий
        meeting_time_future = datetime.now() + timedelta(hours=6)
        meeting_time_past = datetime.now() - timedelta(hours=6)
        event_future = {"name": "future_event",
                        "meeting_time": meeting_time_future,
                        "description": "one_description"}
        event_past = {"name": "past_event",
                      "meeting_time": meeting_time_past,
                      "description": "two_description"}

        Event.objects.create(**event_future)
        Event.objects.create(**event_past)

        cls.event_future = event_future
        cls.event_past = event_past

    # Проверка наличия данных, вывода
    def test_event_viewer(self):
        resp = self.client.get("list_event_all")

        data = resp.json()
        self.assertTrue(data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Проверка вывода новых мероприятий
    def test_event_correct(self):
        resp = self.client.get("list_event_all", self.event_future)
        print(resp)
        print(self.event_future)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Проверка вывода старых мероприятий
    def test_event_not_correct(self):
        resp = self.client.get("list_event_all", self.event_past)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
