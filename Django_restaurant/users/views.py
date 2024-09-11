from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, viewsets
from django.contrib.auth.views import LogoutView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserDetailSerializer, UserSerializer

User = get_user_model()


class UserSignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserLoginView(APIView):

    def post(self, request, *args, **kwargs):
        # 시리얼라이저로 유저 정보를 보냄
        serializer = UserSerializer(data=request.data)

        # 시리얼라이저로 유효하지 않다면
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 유효하다면 그 검증된 데이터(메일,암호) 가져옴
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        # 해당 이메일과 암호로 요청보냄
        user = authenticate(request, email=email, password=password)

        # 유저가 없다면 HTTP400
        if user is None:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 유저가 있다면 로그인
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user