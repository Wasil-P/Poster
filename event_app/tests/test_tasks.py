from django import test
from users.models import User
from rest_framework import status


class TestTasks(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        user = {"username": "user",
                "password": "567gjtfi7yuilgh78",
                "email": "user@mail.com"}

        User.objects.create_user(**user)

        cls.user = user

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()