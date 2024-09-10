from rest_framework import viewsets
from .models import Review  # 가정: 리뷰 모델이 Review로 정의되어 있음
# from serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.all()
    # serializer_class = ReviewSerializer
    pass