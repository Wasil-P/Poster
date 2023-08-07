from users.models import User
from django import test
from rest_framework import status
# from faker import Faker


class UserCreateListAPIView(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        superuser = {"username": "superuser",
                    "password": "567gjtfi7yuilgh45",
                    "email": "superuser@mail.com"}

        user = {"username": "user",
                 "password": "567gjtfi7yuilgh78",
                 "email": "user@mail.com"}

        User.objects.create_user(is_superuser=True, **superuser)
        User.objects.create_user(**user)

        cls.superuser = superuser
        cls.user = user

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self) -> None:
        self.superuser_tokens = self.client.post("/api/token/", self.superuser).json()
        self.user_tokens = self.client.post("/api/token/", self.user).json()
        print(self.superuser_tokens)

    # Проверка доступа просмотра списка зарегестированных пользователей
    def test_list_users_permission(self):
        resp = self.client.get("/api/users/",
        HTTP_AUTHORIZATION=f"Bearer {self.superuser_tokens.get('access')}")
        data = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get("/api/users/",
        HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}")
        data = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        resp = self.client.get("/api/users/")
        data = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


    #Проверка возможности регистрации
    def test_register_user_valid_data(self):
        resp = self.client.post("/api/users/",
                                data={
                                    "username": "Ben",
                                    "password": "567gjtfi7yuilgh45",
                                    "email": "Ben@email.com"
                                })
        data = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


    # Проверка отсутствия возможности регистрации без данных
    def test_register_user_invalid_data(self):
        resp = self.client.post("/api/users/",
                                data={
                                    "password": "567gjtfi7yuilgh45",
                                    "email": "Ben@email.com"
                                })
        data = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.post("/api/users/",
                                data={
                                    "username": "Ben",
                                    "email": "Ben@email.com"
                                })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.post("/api/users/",
                                data={
                                    "username": "Ben",
                                    "password": "567gjtfi7yuilgh45",
                                })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.post("/api/users/", self.user)
        data = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


