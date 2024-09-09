from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from restaurants.models import Restaurant


class RestaurantModelTestCase(TestCase):
    # Restaurant 모델 테스트 시 필요한 세팅 기재
    def setUp(self):
        self.restaurant_data = {
            'name': '식당',
            'address': '강남',
            'contact': '112',
            'open_time': '09:00',
            'close_time': '21:00',
            'last_order': '20:00',
            'regular_holiday': '월'
        }

    # objects의 create 메서드를 테스트하기 위한 코드 기재
    def test_create_restaurant(self):
        restaurants = Restaurant.objects.create(**self.restaurant_data)

        self.assertEqual(restaurants.name, self.restaurant_data['name'])
        self.assertEqual(restaurants.address, self.restaurant_data['address'])
        self.assertEqual(restaurants.contact, self.restaurant_data['contact'])
        self.assertEqual(restaurants.open_time, self.restaurant_data['open_time'])
        self.assertEqual(restaurants.close_time, self.restaurant_data['close_time'])
        self.assertEqual(restaurants.last_order, self.restaurant_data['last_order'])
        self.assertEqual(restaurants.regular_holiday, self.restaurant_data['regular_holiday'])
        self.assertEqual(restaurants.__str__(), self.restaurant_data['name'])


class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        self.restaurant_info = {
            'name': '식당',
            'address': '강남',
            'contact': '112',
            'open_time': '09:00',
            'close_time': '21:00',
            'last_order': '20:00',
            'regular_holiday': '월'
        }

    def test_restaurant_list_view(self):
        url = reverse('restaurant-list')
        Restaurant.objects.create(**self.restaurant_info)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0].get('name'), self.restaurant_info['name'])
        self.assertEqual(response.data.get('results')[0].get('description'), self.restaurant_info['description'])
        self.assertEqual(response.data.get('results')[0].get('address'), self.restaurant_info['address'])
        self.assertEqual(response.data.get('results')[0].get('contact'), self.restaurant_info['contact'])
        self.assertEqual(response.data.get('results')[0].get('open_time'), self.restaurant_info['open_time'])
        self.assertEqual(response.data.get('results')[0].get('close_time'), self.restaurant_info['close_time'])
        self.assertEqual(response.data.get('results')[0].get('last_order'), self.restaurant_info['last_order'])
        self.assertEqual(response.data.get('results')[0].get('regular_holiday'), self.restaurant_info['regular_holiday'])

    def test_restaurant_post_view(self):
        url = reverse('restaurant-list')
        response = self.client.post(url, self.restaurant_info, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.first().name, self.restaurant_info['name'])

    def test_restaurant_detail_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurant-detail', kwargs={'pk': restaurant.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), self.restaurant_info['name'])

    def test_restaurant_update_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurant-detail', kwargs={'pk': restaurant.id})
        updated_restaurant_info = {
            "name": "Updated Restaurant",
            "description": "Updated Description",
            "address":  "Updated Address",
            "contact": "Updated Contact",
            "open_time": "11:00:00",
            "close_time": "23:00:00",
            "last_order": "22:00:00",
            "regular_holiday": "TUE"
        }

        response = self.client.put(url, updated_restaurant_info, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(response.data.get('name'), updated_restaurant_info['name'])
        self.assertEqual(response.data.get('description'), updated_restaurant_info['description'])
        self.assertEqual(response.data.get('address'), updated_restaurant_info['address'])
        self.assertEqual(response.data.get('contact'), updated_restaurant_info['contact'])
        self.assertEqual(response.data.get('open_time'), updated_restaurant_info['open_time'])
        self.assertEqual(response.data.get('close_time'), updated_restaurant_info['close_time'])
        self.assertEqual(response.data.get('last_order'), updated_restaurant_info['last_order'])
        self.assertEqual(response.data.get('regular_holiday'), updated_restaurant_info['regular_holiday'])

    def test_restaurant_delete_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurant-detail', kwargs={'pk': restaurant.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Restaurant.objects.count(), 0)