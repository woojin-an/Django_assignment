from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@test.com",
            "password": "password1234",
            "nickname": "nickname",
        }
        self.superuser_data = {
            "email": "supertest@test.com",
            "password": "password1234",
            "nickname": "nicknamesuper",
            "is_superuser": True,
            "is_staff": True,
        }

    def test_user_manager_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("password1234"))
        self.assertEqual(user.nickname, "nickname")

    def test_user_manager_create_superuser(self):
        superuser = User.objects.create_superuser(**self.superuser_data)
        self.assertEqual(superuser.email, "supertest@test.com")
        self.assertTrue(superuser.check_password("password1234"))
        self.assertEqual(superuser.nickname, "nicknamesuper")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

class UserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="password1234",
            nickname="nickname"
        )
        self.login_url = reverse('user-list')  # 로그인의 경우 적절한 URL 사용
        self.signup_url = reverse('user-list')  # 회원가입의 경우 적절한 URL 사용
        self.profile_url = reverse('user-detail', args=[self.user.id])

    def test_user_signup(self):
        url = self.signup_url
        data = {
            "email": "test1@test.com",
            "password": "password1234",
            "nickname": "nickname",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data['email']).exists())

    def test_user_login(self):
        url = self.login_url
        data = {
            "email": self.user.email,
            "password": "password1234",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_credentials(self):
        url = self.login_url
        data = {
            "email": "test1@test.com",
            "password": "WRONGPASSWORD",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_details(self):
        self.client.login(email=self.user.email, password="password1234")
        url = self.profile_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['nickname'], self.user.nickname)

    def test_update_user_details(self):
        self.client.login(email=self.user.email, password="password1234")
        url = self.profile_url
        update_data = {
            "nickname": "nicknameupdate",
        }
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, "nicknameupdate")

    def test_delete_user(self):
        self.client.login(email=self.user.email, password="password1234")
        url = self.profile_url
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email=self.user.email).exists())