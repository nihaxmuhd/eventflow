from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    UserSerializer,
)
from .services import (
    login_user,
    logout_user,
)
class UserListAPIView(ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]


@extend_schema(
    request=LoginSerializer,
)
class LoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = login_user(
            login=serializer.validated_data["login"],
            password=serializer.validated_data["password"],
        )

        user = result["user"]

        user_data = UserSerializer(
            user,
            context={"request": request},
        ).data

        return Response(
            {
                "success": True,
                "message": "Login successful",
                "data": {
                    "access": result["access"],
                    "refresh": result["refresh"],
                    "user": user_data,
                },
            },
            status=status.HTTP_200_OK,
        )


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(
            request.user,
            context={"request": request},
        )

        return Response(
            {
                "success": True,
                "message": "User fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logout_user(
            serializer.validated_data["refresh"]
        )

        return Response(
            {
                "success": True,
                "message": "Logout successful",
            },
            status=status.HTTP_200_OK,
        )