from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginAPIView,
    LogoutAPIView,
    MeAPIView,
    UserListAPIView,
)

urlpatterns = [

    # Authentication
    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),

    # Users
    path(
        "users/",
        UserListAPIView.as_view(),
        name="user-list",
    ),

    path(
    "me/",
    MeAPIView.as_view(),
    name="me",
    ),

    path(
    "logout/",
    LogoutAPIView.as_view(),
    name="logout",
    ),

]