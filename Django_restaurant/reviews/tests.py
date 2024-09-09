from django.contrib.auth import get_user_model
from django.test import TestCase
from restaurants.models import Restaurant
from reviews.models import Review

User = get_user_model()


class ReviewModelTest(TestCase):
    # Review 모델 테스트 시 필요한 세팅 기재
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            nickname='test',
            password='testtest1234',
            is_active=True
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
        )
        self.review_data = {
            'user': User.objects.first(),
            'restaurant': Restaurant.objects.first(),
            'title': 'test title',
            'comment': 'test comment',
        }

    # objects의 create 메서드를 테스트하기 위한 코드 기재
    def test_create_review(self):
        review = Review.objects.create(**self.review_data)

        self.assertEqual(review.user, self.review_data['user'])
        self.assertEqual(review.restaurant, self.review_data['restaurant'])
        self.assertEqual(review.title, self.review_data['title'])
        self.assertEqual(review.comment, self.review_data['comment'])
        self.assertEqual(review.__str__(), f'{self.review_data['restaurant']} 리뷰')

