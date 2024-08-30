from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from blog import cb_views, views

app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # CBV Blog
    path('', cb_views.BlogListView.as_view(), name='list'),
    path('<int:blog_pk>/', cb_views.BlogDetailView.as_view(), name='detail'),
    path('create/', cb_views.BlogCreateView.as_view(), name='create'),
    path('<int:pk>/update/', cb_views.BlogUpdateView.as_view(), name='update'),
    # path('<int:pk>/update/', views.blog_update, name='update'),
    path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='delete'),
    path('comment/create/<int:blog_pk>/', cb_views.CommentCreateView.as_view(), name='comment_create'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)