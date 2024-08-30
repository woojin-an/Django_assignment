"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.views import View
from django.views.generic import TemplateView, RedirectView

from blog import views, cb_views
from django.urls import include
from member import views as member_views


# class AboutView(TemplateView):
#     template_name = 'about.html'
#
#
# class TestView(View):
#     def get(self, request):
#         return render(request, 'test_get.html')
#
#     def post(self, request):
#         return render(request, 'test_post.html')


urlpatterns = [
    path('admin/', admin.site.urls),

    # FBV auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),

    # CBV (Class Based View)
    # path('about', AboutView.as_view(), name='about'),
    # path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    # # path('redirect2/', lambda req: redirect('about')),
    # path('test/', TestView.as_view(), name='test'),

    # url include
    path('', include('blog.urls')),
    path('fb/', include('blog.fbv_urls')),

    # summernote
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)