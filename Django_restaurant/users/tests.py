from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserModelTestCase(TestCase):
    # 유저 모델 테스트 시 필요한 세팅 기재
    def setUp(self):

        self.user_data = {
            'email': 'test@test.com',
            'password': 'password1234',
            'nickname': 'nickname',
        }
        self.superuser_data = {
            'email': 'supertest@test.com',
            'password': 'password1234',
            "nickname": 'nicknamesuper',
            "is_superuser": True,
            "is_staff": True,
        }

    # UserManager의 create_user 메서드를 테스트하기 위한 코드 기재
    def test_user_manager_create_user(self):
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('password1234'))
        self.assertEqual(user.nickname, 'nickname')

    # UserManager의 create_superuser 메서드를 테스트하기 위한 코드 기재
    def test_user_manager_create_superuser(self):
        superuser = User.objects.create_user(**self.superuser_data)

        self.assertEqual(superuser.email, 'supertest@test.com')
        self.assertTrue(superuser.check_password('password1234'))
        self.assertEqual(superuser.nickname, 'nicknamesuper')
        self.assertEqual(superuser.is_superuser, True)
        self.assertEqual(superuser.is_staff, True)
