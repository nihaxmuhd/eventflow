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
    UserCreateSerializer,
)

from .services import (
    login_user,
    logout_user,
)


class UserListAPIView(ListAPIView):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        current_user = self.request.user

        if (
            current_user.role
            == User.Roles.SUPER_ADMIN
        ):
            return User.objects.all()

        return User.objects.filter(
            school=current_user.school
        )


@extend_schema(
    request=LoginSerializer,
)
class LoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

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

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

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


@extend_schema(
    request=UserCreateSerializer,
    responses=UserSerializer,
)
class UserCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        current_user = request.user

        serializer = UserCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        role = serializer.validated_data["role"]

        # SUPER ADMIN
        if (
            current_user.role
            == User.Roles.SUPER_ADMIN
        ):
            pass

        # ADMIN
        elif (
            current_user.role
            == User.Roles.ADMIN
        ):

            if role not in [
                User.Roles.MANAGER,
                User.Roles.TEAM_LEADER,
            ]:

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Admins can only "
                            "create Managers "
                            "and Team Leaders"
                        ),
                    },
                    status=403,
                )

        else:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Permission denied"
                    ),
                },
                status=403,
            )

        # ADMIN cannot create users in other schools
        if (
            current_user.role
            == User.Roles.ADMIN
        ):
            serializer.validated_data[
                "school"
            ] = current_user.school

        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": (
                    "User created successfully"
                ),
                "data": UserSerializer(
                    user,
                    context={
                        "request": request
                    },
                ).data,
            },
            status=201,
        )