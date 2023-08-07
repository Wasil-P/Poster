from rest_framework import status
from users.models import User
from ..models import Event
from datetime import datetime, timedelta
from django.shortcuts import reverse
from rest_framework.test import APITestCase

class TestEventListAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # создание переменных для мероприятий
        meeting_time_future = datetime.now() + timedelta(hours=7)
        meeting_time_past = datetime.now() - timedelta(hours=7)
        event_future = {"name": "future_event",
                        "meeting_time": meeting_time_future,
                        "description": "one_description"}
        event_past = {"name": "past_event",
                      "meeting_time": meeting_time_past,
                      "description": "two_description"}

        cls.event_f = Event.objects.create(**event_future)
        cls.event_p = Event.objects.create(**event_past)

        cls.event_future = event_future
        cls.event_past = event_past


        user = {"username": "user",
                 "password": "567gjtfi7yuilgh78",
                 "email": "user@mail.com"}
        User.objects.create_user(**user)

        cls.user = user

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self) -> None:
        self.user_tokens = self.client.post("/api/token/", self.user).json()

    # Проверка наличия данных, вывода
    def test_event_viewer(self):
        resp = self.client.get("/api/events/")

        data = resp.json()
        print(data)
        self.assertTrue(data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Проверка отсутствия прошедших мероприятий
        self.assertNotIn(self.event_past, data)

    # Проверка возможности подписаться на событие авторизированному пользователю
    def test_subscription_event_valid_data(self):
        resp = self.client.post(reverse("one_event_view", args=(self.event_f.id,)),
        HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Проверка возможности подписаться на событие которое прошло
    def test_subscription_event_past(self):
        resp = self.client.post(reverse("one_event_view", args=(self.event_p.id,)),
        HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}")

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    # Проверка возможности подписаться на событие незарегестрированному пользователю
    def test_subscription_event_invalid_data(self):
        # Невалидный access-токен
        invalid_access = "325j4ner8ergfnjxcvx90ertmkdfv0erjsdgd234cw4w35enbv"
        resp = self.client.post(reverse("one_event_view", args=(self.event_f.id,)),
        HTTP_AUTHORIZATION=f"Bearer {invalid_access}")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Без access-токена
        resp = self.client.post(reverse("one_event_view", args=(self.event_f.id,)))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    # Вывод всех подписок пользователя
    def test_view_my_list_valid_data(self):
        resp = self.client.get(reverse("my_list_event"),
        HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Проверка вывода подписок с невалидными данными
    def test_view_my_list_invalid_data(self):
        invalid_access = "325j4ner8ergfnjxcvx90ertmkdfv0erjsdgd234cw4w35enbv"
        resp = self.client.post(reverse("my_list_event"),
                                HTTP_AUTHORIZATION=f"Bearer {invalid_access}")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        resp = self.client.post(reverse("my_list_event"),)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
