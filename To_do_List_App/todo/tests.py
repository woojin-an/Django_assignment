from django.test import TestCase


class TodoViewTest(TestCase):
    def test_simple(self):
        assert 1 + 1 == 2

    def test_get_login_page(self):
        response = self.client.get('/accounts/login')
        assert response.status_code == 301