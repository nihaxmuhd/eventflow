from django.urls import path

from .views import (
    HouseLeaderboardAPIView,
    StudentLeaderboardAPIView,
)

urlpatterns = [

    path(
        "houses/",
        HouseLeaderboardAPIView.as_view(),
        name="house-leaderboard",
    ),

    path(
        "students/",
        StudentLeaderboardAPIView.as_view(),
        name="student-leaderboard",
    ),

]