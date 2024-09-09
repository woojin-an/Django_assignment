from django.urls import path

from restaurants import views
from rest_framework import routers

app_name = 'restaurants'

router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant-list')

urlpatterns = [
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
]
