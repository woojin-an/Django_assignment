from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant


class RestaurantViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # 유저 생성
        self.user = get_user_model().objects.create_user(
            nickname='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        # 유저 로그인
        self.client.login(email='testuser@example.com', password='testpassword')

        # 테스트용 식당 데이터 생성
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Address",
            contact="010-1234-5678",
            open_time="10:00:00",
            close_time="22:00:00",
            last_order="21:30:00",
            regular_holiday="MON"
        )

    def test_list_restaurants(self):
        # 식당 목록 조회 테스트
        response = self.client.get('/api/restaurants/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        print("Response data:", response_data)
        self.assertTrue(any(item['name'] == "Test Restaurant" for item in response_data['results']))

    def test_create_restaurant(self):
        # 식당 생성 테스트
        data = {
            "name": "New Restaurant",
            "address": "456 New Address",
            "contact": "010-9876-5432",
            "open_time": "09:00:00",
            "close_time": "23:00:00",
            "last_order": "22:30:00",
            "regular_holiday": "TUE"
        }
        response = self.client.post('/api/restaurants/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_retrieve_restaurant(self):
        # 특정 식당 조회 테스트
        response = self.client.get(f'/api/restaurants/{self.restaurant.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test Restaurant")

    def test_update_restaurant(self):
        # 식당 정보 수정 테스트
        data = {
            "name": "Updated Restaurant",
            "address": "789 Updated Address",
        }
        response = self.client.patch(f'/api/restaurants/{self.restaurant.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, "Updated Restaurant")

    def test_delete_restaurant(self):
        # 식당 삭제 테스트
        response = self.client.delete(f'/api/restaurants/{self.restaurant.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Restaurant.objects.count(), 0)
