from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models.users.models import User


class ShortenerViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(email="testuser@ntest.com", password="testpass")

        # 데이터 선언
        cls.data = {
            "origin_url": "http://127.0.0.1:8000/api/v1/swagger/",
            "expiration_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

        cls.create_url = reverse("create-shorteners")

    def setUp(self):
        # 로그인
        login_url = reverse("users-login")
        login_data = {"email": "testuser@ntest.com", "password": "testpass"}
        response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    # 단축 url 생성
    def test_create_short_url(self):
        response = self.client.post(self.create_url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)
        self.assertEqual(response.data["origin_url"], self.data["origin_url"])
        self.assertEqual(response.data["user"], self.user.email)

    # 단축 URL 리다이렉트
    def test_get_redirect(self):
        response = self.client.post(self.create_url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 단축 URL로 리다이렉트 요청
        short_url = response.data["short_url"]
        url = reverse("redirect-shorteners", kwargs={"short_url": short_url})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 302)
