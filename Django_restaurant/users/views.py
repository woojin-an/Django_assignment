from rest_framework import viewsets
from django.contrib.auth.views import LogoutView
from .models import User  # 가정: 사용자 모델이 User로 정의되어 있음
# from serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        # 회원가입 처리 로직
        pass

    def list(self, request):
        # 사용자 목록 조회 로직
        pass

    def retrieve(self, request, pk=None):
        # 특정 사용자 조회 로직
        pass


class UserLoginView(viewsets.ViewSet):
    def create(self, request):
        # 로그인 처리 로직
        pass


class UserSignupView(viewsets.ViewSet):
    def create(self, request):
        # 회원가입 처리 로직
        pass


class UserDetailView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # 사용자 프로필 조회 로직
        pass
