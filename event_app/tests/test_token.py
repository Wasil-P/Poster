# from faker import Faker
from rest_framework.test import APITestCase
from users.models import User
from rest_framework import status


class TestJWTAuth(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create_user(
            username="username",
            password="567gjtfi7yuilgh78",
            email="user@mail.com",
        )
        print(cls.user)
        print(type(cls.user))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        #Проверка получения access- и refresh- токена
    def test_get_token_valid(self):
        resp = self.client.post("/api/token/",
                                data={
                                        "username": self.user.username,
                                        "password": "567gjtfi7yuilgh78",
                                    })

        data = resp.json()
        print(data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", data)
        self.assertIn("refresh", data)

    # Проверка отсутствия получения access- и refresh-токена
    # по неправильным данным и их без них.
    def test_get_token_invalid(self):
        resp = self.client.post("/api/token/",
                                data={
                                    "username": self.user.username,
                                    "password": "1",
                                })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        resp = self.client.post("/api/token/",
                                data={
                                    "username": self.user.username,
                                })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.post("/api/token/",
                                data={
                                    "password": "567gjtfi7yuilgh78",
                                })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # Проверка получения нового access-токена
    def test_get_token_refresh(self):
        resp = self.client.post("/api/token/",
                                data={
                                        "username": self.user.username,
                                        "password": "567gjtfi7yuilgh78",
                                    })

        data = resp.json()
        print(f'first_data - {data}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        refresh_token_first = resp.json()["refresh"]
        print(f'first_refresh - {refresh_token_first}')

        resp = self.client.post("/api/token/refresh/",
                                data={"refresh": refresh_token_first})
        print(f"new_access - {resp.json()}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.json())

    #Проверка отсутствия возможности получить новый access-токен
    # с помощью старого refresh-токена
        resp = self.client.post("/api/token/",
                                data={
                                        "username": self.user.username,
                                        "password": "567gjtfi7yuilgh78",
                                    })

        data = resp.json()
        print(f'second_data - {data}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        refresh_token_second = resp.json()["refresh"]
        print(f'second_refresh - {refresh_token_second}')

        resp = self.client.post("/api/token/refresh/",
                                data={"refresh": refresh_token_first})
        data = resp.json()
        print()
        print(f'new_access - {data}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access", resp.json())
