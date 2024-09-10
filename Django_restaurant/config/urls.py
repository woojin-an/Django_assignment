from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # users 앱의 URL 매핑
    path('reviews/', include('reviews.urls')),  # reviews 앱의 URL 매핑
    path('api/', include('restaurants.urls')),  # restaurants 앱의 URL 매핑
]
