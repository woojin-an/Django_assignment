from django.http import Http404
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Review  # 가정: 리뷰 모델이 Review로 정의되어 있음
from .serializers import ReviewDetailSerializer, ReviewSerializer

from restaurants.models import Restaurant


class ReviewListCreateView(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Review.objects.filter(restaurant_id=restaurant_id).order_by('-created_at')

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_id')
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404('해당 식당이 존재하지 않습니다.')

        user = self.request.user
        serializer.save(restaurant=restaurant, user=user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, user=self.request.user)
        return review

